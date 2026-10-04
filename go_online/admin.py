from django.contrib import admin

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


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Location)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)

admin.site.register(Store)
admin.site.register(StoreInventory)

admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Payment)

admin.site.register(DeliveryPartner)
admin.site.register(Delivery)

admin.site.register(ProductReview)
admin.site.register(Coupon)