from rest_framework.routers import DefaultRouter

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


router = DefaultRouter()

router.register(
    r"users",
    UserViewSet,
    basename="users"
)

router.register(
    r"register",
    RegisterViewSet,
    basename="register"
)

router.register(
    r"profiles",
    UserProfileViewSet,
    basename="profiles"
)

router.register(
    r"locations",
    LocationViewSet,
    basename="locations"
)

router.register(
    r"categories",
    CategoryViewSet,
    basename="categories"
)

router.register(
    r"subcategories",
    SubCategoryViewSet,
    basename="subcategories"
)

router.register(
    r"brands",
    BrandViewSet,
    basename="brands"
)

router.register(
    r"products",
    ProductViewSet,
    basename="products"
)

router.register(
    r"product-images",
    ProductImageViewSet,
    basename="product-images"
)

router.register(
    r"product-variants",
    ProductVariantViewSet,
    basename="product-variants"
)

router.register(
    r"stores",
    StoreViewSet,
    basename="stores"
)

router.register(
    r"inventory",
    StoreInventoryViewSet,
    basename="inventory"
)

router.register(
    r"cart",
    CartViewSet,
    basename="cart"
)

router.register(
    r"cart-items",
    CartItemViewSet,
    basename="cart-items"
)

router.register(
    r"orders",
    OrderViewSet,
    basename="orders"
)

router.register(
    r"order-items",
    OrderItemViewSet,
    basename="order-items"
)

router.register(
    r"payments",
    PaymentViewSet,
    basename="payments"
)

router.register(
    r"delivery-partners",
    DeliveryPartnerViewSet,
    basename="delivery-partners"
)

router.register(
    r"deliveries",
    DeliveryViewSet,
    basename="deliveries"
)

router.register(
    r"reviews",
    ProductReviewViewSet,
    basename="reviews"
)

router.register(
    r"coupons",
    CouponViewSet,
    basename="coupons"
)


urlpatterns = router.urls