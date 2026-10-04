from rest_framework import serializers
# from django.contrib.auth import get_user_model

from .models import User

from .models import (
    User,
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

# User = get_user_model()


# ============================================================
# USER
# ============================================================

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


# =========================================================
# USER SERIALIZER
# =========================================================

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "is_phone_verified",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "role",
            "is_phone_verified",
            "created_at",
            "updated_at",
        ]


# =========================================================
# REGISTER SERIALIZER
# =========================================================



User = get_user_model()


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150
    )

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    first_name = serializers.CharField(
        max_length=150
    )

    last_name = serializers.CharField(
        max_length=150
    )

    phone = serializers.CharField(
        max_length=15
    )


    def validate(self, data):

        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")

        # Username check
        if User.objects.filter(
            username=username
        ).exists():

            raise serializers.ValidationError({
                "username": "Username already exists."
            })


        # Email check
        if User.objects.filter(
            email=email
        ).exists():

            raise serializers.ValidationError({
                "email": "Email already exists."
            })


        # Phone check
        if User.objects.filter(
            phone=phone
        ).exists():

            raise serializers.ValidationError({
                "phone": "Phone number already exists."
            })


        return data


    def create_user(self):

        username = self.validated_data["username"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        phone = self.validated_data["phone"]


        # Create user manually
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,

            # New users are customers
            role=User.Role.CUSTOMER,

            # Phone is not verified initially
            is_phone_verified=False,

            # Activate account
            is_active=True,
        )


        # Hash password manually
        user.set_password(password)

        # Save user
        user.save()

        return user


        
# ============================================================
# PROFILE
# ============================================================

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ["user"]


# ============================================================
# LOCATION
# ============================================================

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
        read_only_fields = ["user"]


# ============================================================
# CATEGORY
# ============================================================

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = "__all__"


# ============================================================
# BRAND
# ============================================================

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


# ============================================================
# PRODUCT
# ============================================================

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "subcategory",
            "brand",
            "name",
            "slug",
            "sku",
            "description",
            "mrp",
            "selling_price",
            "unit",
            "weight",
            "tax_percentage",
            "is_active",
            "is_featured",
            "images",
            "variants",
            "created_at",
            "updated_at",
        ]


# ============================================================
# STORE
# ============================================================

class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = "__all__"


class StoreInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreInventory
        fields = "__all__"


# ============================================================
# CART
# ============================================================

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["cart"]


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user"]


# ============================================================
# ORDER
# ============================================================

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["order"]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "store",
            "address",
            "order_number",
            "status",
            "subtotal",
            "delivery_fee",
            "discount",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "user",
            "order_number",
            "status",
        ]


# ============================================================
# PAYMENT
# ============================================================

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


# ============================================================
# DELIVERY
# ============================================================

class DeliveryPartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryPartner
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = "__all__"


# ============================================================
# REVIEW
# ============================================================

class ProductReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReview
        fields = "__all__"

        read_only_fields = [
            "user",
        ]

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value


# ============================================================
# COUPON
# ============================================================

class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = "__all__"



