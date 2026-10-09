from rest_framework import viewsets , status
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import (
    UserProfile,
    Location,
    Category,
    SubCategory,
    Brand,
    Product,
    ProductImage,
    ProductVariant,
    Store,
    StoreInventory,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    DeliveryPartner,
    Delivery,
    ProductReview,
    Coupon,
)

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    LocationSerializer,
    CategorySerializer,
    SubCategorySerializer,
    BrandSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductVariantSerializer,
    StoreSerializer,
    StoreInventorySerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    PaymentSerializer,
    DeliveryPartnerSerializer,
    DeliverySerializer,
    ProductReviewSerializer,
    CouponSerializer,
)


User = get_user_model()


# ============================================================
# USER
# ============================================================

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_staff:
            return User.objects.all()

        return User.objects.filter(
            id=self.request.user.id
        )


class RegisterViewSet(viewsets.GenericViewSet):

    serializer_class = RegisterSerializer

    permission_classes = [
        AllowAny
    ]


    def create(self, request):

        # -----------------------------------------
        # Validate request
        # -----------------------------------------

        serializer = self.get_serializer(
            data=request.data
        )


        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Registration failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            # -----------------------------------------
            # Custom user creation
            # -----------------------------------------

            user = serializer.create_user()


            # -----------------------------------------
            # Response data
            # -----------------------------------------

            user_data = UserSerializer(
                user
            ).data


            return Response(
                {
                    "success": True,
                    "message": "Registration successful.",
                    "data": user_data,
                },
                status=status.HTTP_201_CREATED
            )


        except Exception as error:

            print(
                "Registration Error:",
                str(error)
            )


            return Response(
                {
                    "success": False,
                    "message": "Unable to create account.",
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




# ============================================================
# PROFILE
# ============================================================

class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return UserProfile.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ============================================================
# LOCATION
# ============================================================

class LocationViewSet(viewsets.ModelViewSet):

    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Location.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ============================================================
# CATEGORY
# ============================================================

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # permission_classes = [IsAuthenticated]


# ============================================================
# SUB CATEGORY
# ============================================================

class SubCategoryViewSet(viewsets.ModelViewSet):

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    # permission_classes = [IsAuthenticated]


# ============================================================
# BRAND
# ============================================================

class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# PRODUCT
# ============================================================


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Product, Category
from .serializers import ProductSerializer



from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.select_related(
            "category", "subcategory", "brand"
        ).prefetch_related("images", "variants")

        category = self.request.query_params.get("category")
        brand = self.request.query_params.get("brand")
        search = self.request.query_params.get("search")

        if category:
            category = category.strip()

            if category.isdigit():
                queryset = queryset.filter(
                    category_id=int(category)
                )
            else:
                queryset = queryset.filter(
                    category__slug__iexact=category
                )

        if brand:
            brand = brand.strip()

            if brand.isdigit():
                queryset = queryset.filter(brand_id=int(brand))
            else:
                queryset = queryset.filter(
                    brand__slug__iexact=brand
                )

        if search:
            queryset = queryset.filter(
                name__icontains=search.strip()
            )

        return queryset


# ============================================================
# PRODUCT IMAGE
# ============================================================

class ProductImageViewSet(viewsets.ModelViewSet):

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# PRODUCT VARIANT
# ============================================================

class ProductVariantViewSet(viewsets.ModelViewSet):

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# STORE
# ============================================================

class StoreViewSet(viewsets.ModelViewSet):

    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# STORE INVENTORY
# ============================================================

class StoreInventoryViewSet(viewsets.ModelViewSet):

    queryset = StoreInventory.objects.all()
    serializer_class = StoreInventorySerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = StoreInventory.objects.all()

        store = self.request.query_params.get(
            "store"
        )

        product = self.request.query_params.get(
            "product"
        )

        if store:
            queryset = queryset.filter(
                store_id=store
            )

        if product:
            queryset = queryset.filter(
                product_id=product
            )

        return queryset


# ============================================================
# CART
# ============================================================

class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Cart.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


class CartItemViewSet(viewsets.ModelViewSet):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return CartItem.objects.filter(
            cart__user=self.request.user
        )

    def perform_create(self, serializer):

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        serializer.save(
            cart=cart,
            price=serializer.validated_data[
                "product"
            ].selling_price
        )


# ============================================================
# ORDER
# ============================================================

class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        import uuid

        serializer.save(
            user=self.request.user,
            order_number=f"QK-{uuid.uuid4().hex[:10].upper()}"
        )


# ============================================================
# ORDER ITEM
# ============================================================

class OrderItemViewSet(viewsets.ModelViewSet):

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return OrderItem.objects.filter(
            order__user=self.request.user
        )


# ============================================================
# PAYMENT
# ============================================================

class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_staff:
            return Payment.objects.all()

        return Payment.objects.filter(
            order__user=self.request.user
        )


# ============================================================
# DELIVERY PARTNER
# ============================================================

class DeliveryPartnerViewSet(viewsets.ModelViewSet):

    serializer_class = DeliveryPartnerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_staff:
            return DeliveryPartner.objects.all()

        return DeliveryPartner.objects.filter(
            user=self.request.user
        )


# ============================================================
# DELIVERY
# ============================================================

class DeliveryViewSet(viewsets.ModelViewSet):

    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_staff:
            return Delivery.objects.all()

        return Delivery.objects.filter(
            delivery_partner__user=self.request.user
        )


# ============================================================
# REVIEW
# ============================================================

class ProductReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return ProductReview.objects.all()

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ============================================================
# COUPON
# ============================================================

class CouponViewSet(viewsets.ModelViewSet):

    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    permission_classes = [IsAuthenticated]


