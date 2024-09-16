from django.contrib import admin,messages
from .models import Category, Product, Stock, MostSoldProduct
from django.db import IntegrityError

def check_integrity(modeladmin, request, queryset):
    try:
        for obj in queryset:
            # Example check: Stock's category must match the product's category
            if isinstance(obj, Stock) and obj.category != obj.product.category:
                raise IntegrityError("Stock's category must match the product's category.")
    except IntegrityError as e:
        modeladmin.message_user(request, f"Integrity check failed: {e}", level='error')


check_integrity.short_description = "Check integrity of selected items"

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')
    search_fields = ('name',)
    list_filter = ('category',)
    readonly_fields = ('image',)  # If you want to make image field read-only in admin
    actions = [check_integrity]

# Register the Stock model
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'quantity')
    list_filter = ('category',)
    search_fields = ('product__name',)
    actions = [check_integrity]

# Register the MostSoldProduct model
@admin.register(MostSoldProduct)
class MostSoldProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'month', 'rank')
    list_filter = ('month',)
    search_fields = ('product__name',)
    ordering = ('-month', 'rank')

    def save_model(self, request, obj, form, change):
        # Check if the product exists before saving
        if not Product.objects.filter(id=obj.product_id).exists():
            messages.error(request, "The selected product does not exist.")
            return
        super().save_model(request, obj, form, change)
