import os
import re
import csv
import time
from io import BytesIO
from pathlib import Path

import requests
import django
from PIL import Image, UnidentifiedImageError
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goonline.settings")
django.setup()

from go_online.models import Product, ProductImage

# Openverse image API
API_URL = "https://api.openverse.org/v1/images/"

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "media" / "products"
MANIFEST = IMAGE_DIR / "image_sources.csv"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# False: preserve existing primary images.
# True: replace existing primary images with new results.
REPLACE_EXISTING = False

# Delay between product searches to reduce rate limits.
SEARCH_DELAY = 3

HEADERS = {
    "User-Agent": "GoOnlineDemoStore/1.0 (product image downloader)",
    "Accept": "application/json",
}

CSV_FIELDS = [
    "sku",
    "product_name",
    "image_title",
    "creator",
    "creator_url",
    "license",
    "license_version",
    "license_url",
    "source_page_url",
    "direct_image_url",
    "provider",
    "local_image",
    "status",
]


def request_with_retries(url, params=None):
    """Retry rate limits and temporary server errors."""
    for attempt in range(5):
        try:
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=30,
            )

            if response.status_code == 429 or response.status_code >= 500:
                status = response.status_code
                response.close()

                wait = min(5 * (attempt + 1), 30)
                print(f"HTTP {status}; retrying in {wait}s")
                time.sleep(wait)
                continue

            response.raise_for_status()
            return response

        except requests.RequestException:
            if attempt == 4:
                raise

            time.sleep(min(5 * (attempt + 1), 30))

    raise RuntimeError("Request failed after 5 attempts")


def search_images(product):
    """Search using the actual database product name."""
    response = request_with_retries(
        API_URL,
        params={
            "q": product.name,
            "page": 1,
            "page_size": 20,
            "license_type": "commercial",
            "mature": "false",
            "filter_dead": "true",
        },
    )

    try:
        return response.json().get("results", [])
    finally:
        response.close()


def choose_candidate(results, product_name):
    """Choose the result with the strongest name/title/tag match."""
    words = {
        word.lower()
        for word in re.findall(r"[a-zA-Z0-9]+", product_name)
        if len(word) > 2
    }

    candidates = []

    for item in results:
        text = (item.get("title") or "").lower()

        tags = item.get("tags") or []
        for tag in tags:
            if isinstance(tag, dict):
                text += " " + tag.get("name", "").lower()
            else:
                text += " " + str(tag).lower()

        score = sum(word in text for word in words)

        if score == 0:
            continue

        if not item.get("url") and not item.get("thumbnail"):
            continue

        candidates.append((score, item))

    if not candidates:
        return None

    candidates.sort(key=lambda pair: pair[0], reverse=True)
    return candidates[0][1]


def download_and_convert(item):
    """Download an image, validate it, and convert it to JPEG."""
    urls = list(dict.fromkeys(
        url for url in [item.get("url"), item.get("thumbnail")] if url
    ))

    for url in urls:
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=30,
            )

            try:
                response.raise_for_status()

                content_type = response.headers.get(
                    "Content-Type", ""
                ).lower()

                if not content_type.startswith("image/"):
                    continue

                if len(response.content) > 15 * 1024 * 1024:
                    print("Image exceeds 15 MB; trying another URL")
                    continue

                with Image.open(BytesIO(response.content)) as image:
                    image.verify()

                with Image.open(BytesIO(response.content)) as image:
                    image = image.convert("RGB")
                    output = BytesIO()
                    image.save(output, format="JPEG", quality=85)
                    return output.getvalue()

            finally:
                response.close()

        except (
            requests.RequestException,
            UnidentifiedImageError,
            OSError,
            ValueError,
        ) as error:
            print(f"Image download failed: {error}")

    return None


def save_image(product, content):
    """Save a JPEG through Django's ImageField."""
    image_record = product.images.filter(is_primary=True).first()

    if image_record is None:
        image_record = product.images.first()

    filename = f"{re.sub(r'[^A-Za-z0-9_-]', '_', product.sku)}.jpg"

    if image_record is not None:
        if not REPLACE_EXISTING and image_record.image:
            return image_record, False

        image_record.image.save(
            filename,
            ContentFile(content),
            save=False,
        )
        image_record.is_primary = True
        image_record.display_order = 0
        image_record.save()

    else:
        image_record = ProductImage(
            product=product,
            is_primary=True,
            display_order=0,
        )
        image_record.image.save(
            filename,
            ContentFile(content),
            save=True,
        )

    product.images.exclude(pk=image_record.pk).filter(
        is_primary=True
    ).update(is_primary=False)

    return image_record, True


def write_manifest(product, item, image_record, status):
    """Record original source and license links in a CSV file."""
    new_file = not MANIFEST.exists() or MANIFEST.stat().st_size == 0

    with MANIFEST.open("a", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)

        if new_file:
            writer.writeheader()

        writer.writerow({
            "sku": product.sku,
            "product_name": product.name,
            "image_title": item.get("title", ""),
            "creator": item.get("creator", ""),
            "creator_url": item.get("creator_url", ""),
            "license": item.get("license", ""),
            "license_version": item.get("license_version", ""),
            "license_url": item.get("license_url", ""),
            "source_page_url": item.get("foreign_landing_url", ""),
            "direct_image_url": item.get("url", ""),
            "provider": item.get("provider", ""),
            "local_image": image_record.image.name if image_record else "",
            "status": status,
        })


def process_product(product):
    sku = product.sku
    print(f"\nProcessing: {product.name} [{sku}]")

    existing = product.images.filter(is_primary=True).first()

    if existing and existing.image and not REPLACE_EXISTING:
        print(f"SKIPPED: Primary image already exists for {sku}")
        return "SKIPPED"

    results = search_images(product)
    item = choose_candidate(results, product.name)

    if not item:
        print(f"NO MATCH: {sku}")
        return "NO MATCH"

    content = download_and_convert(item)

    if not content:
        print(f"DOWNLOAD FAILED: {sku}")
        return "DOWNLOAD FAILED"

    # Save image and source details.
    image_record, changed = save_image(product, content)

    if not changed:
        print(f"SKIPPED: Existing image preserved for {sku}")
        return "SKIPPED"

    write_manifest(product, item, image_record, "SAVED")

    print(f"SAVED: {sku} -> {image_record.image.name}")
    print(f"Source page: {item.get('foreign_landing_url', '')}")
    print(f"Image URL: {item.get('url', '')}")
    print(f"License: {item.get('license_url', '')}")

    return "SAVED"


def main():
    # Processes all products in the database, not just 28 hardcoded SKUs.
    products = Product.objects.all().order_by("sku")

    print(f"Products found: {products.count()}")
    print(f"Image directory: {IMAGE_DIR}")
    print(f"Source manifest: {MANIFEST}")
    print(f"Replace existing images: {REPLACE_EXISTING}")

    totals = {
        "SAVED": 0,
        "SKIPPED": 0,
        "NO MATCH": 0,
        "DOWNLOAD FAILED": 0,
        "ERROR": 0,
    }

    for product in products.iterator():
        try:
            status = process_product(product)
            totals[status] = totals.get(status, 0) + 1

        except Exception as error:
            totals["ERROR"] += 1
            print(f"ERROR: {product.sku}: {error}")

        time.sleep(SEARCH_DELAY)

    print("\n========== SUMMARY ==========")
    for status, count in totals.items():
        print(f"{status}: {count}")

    print(f"\nImages: {IMAGE_DIR}")
    print(f"Source links: {MANIFEST}")


if __name__ == "__main__":
    main()