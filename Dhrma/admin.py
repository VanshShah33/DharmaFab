from django.contrib import admin

from .models import Company, Contact, Gallery, Inquiry, Manufacturing, Newsletter, Product


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline')
    search_fields = ('name', 'tagline', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'category', 'description')


@admin.register(Manufacturing)
class ManufacturingAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'quantity', 'is_read', 'created_at')
    list_filter = ('subject', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company', 'message')
    readonly_fields = ('created_at',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'fabric_name', 'email', 'phone', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'fabric_name', 'email', 'phone', 'company', 'message')
    readonly_fields = ('created_at',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)
