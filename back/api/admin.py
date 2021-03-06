from django.contrib.gis import admin

from .models import (
    Copyright,
    Document,
    Format,
    Identity,
    Metadata,
    MetadataContact,
    Order,
    OrderItem,
    Pricing,
    Product,
    ProductFormat)


class MetadataContactInline(admin.TabularInline):
    model = MetadataContact
    extra = 1


class MetadataAdmin(admin.ModelAdmin):
    inlines = [MetadataContactInline]
    search_fields = ['name', 'id_name']


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['label']


class IdentityAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'company_name']


admin.site.register(Copyright)
admin.site.register(Document)
admin.site.register(Format)
admin.site.register(Identity, IdentityAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(MetadataContact)
admin.site.register(Order, admin.OSMGeoAdmin)
admin.site.register(OrderItem)
admin.site.register(Pricing)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductFormat)
