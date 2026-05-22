from django.contrib import admin

from .models import (
    Category,
    NewsletterSubscriber,
    Order,
    OrderItem,
    PasswordResetCode,
    Product,
    Rating,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at", "updated_at")
    list_filter = ("category", "is_popular", "is_sale")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "created_at", "updated_at")
    search_fields = ("email", "full_name")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "score", "created_at", "updated_at")
    list_filter = ("score",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "email", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("customer_name", "email", "phone")
    inlines = [OrderItemInline]


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "is_used", "created_at", "updated_at")
