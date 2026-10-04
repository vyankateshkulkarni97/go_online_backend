from django.urls import path

from .views import (
    UserViewSet,
    RegisterViewSet,
    UserProfileViewSet,
    LocationViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductVariantViewSet,
    StoreViewSet,
    StoreInventoryViewSet,
    CartViewSet,
    CartItemViewSet,
    OrderViewSet,
    OrderItemViewSet,
    PaymentViewSet,
    DeliveryPartnerViewSet,
    DeliveryViewSet,
    ProductReviewViewSet,
    CouponViewSet,
)


urlpatterns = [

    path(
        "users/",
        UserViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "register/",
        RegisterViewSet.as_view({
            "post": "create",
        }),
    ),

    path(
        "profiles/",
        UserProfileViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "locations/",
        LocationViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "categories/",
        CategoryViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "subcategories/",
        SubCategoryViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "brands/",
        BrandViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "products/",
        ProductViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "product-images/",
        ProductImageViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "product-variants/",
        ProductVariantViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "stores/",
        StoreViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "inventory/",
        StoreInventoryViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "cart/",
        CartViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "cart-items/",
        CartItemViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "orders/",
        OrderViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "order-items/",
        OrderItemViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "payments/",
        PaymentViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "delivery-partners/",
        DeliveryPartnerViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "deliveries/",
        DeliveryViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "reviews/",
        ProductReviewViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),

    path(
        "coupons/",
        CouponViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),
]
