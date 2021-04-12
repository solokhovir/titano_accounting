from django.contrib import admin

from .models import Persons, Points, Product, Detail, Materials, Color, Unit, Supplier, TranType


class TransactionsAdmin(admin.ModelAdmin):
    list_display = (
    'surname',
    'point_name',
    'product_name',
    'detail_name',
    'material_name',
    'color_name',
    'unit_name',
    'supplier_name',
    'type')


admin.site.register(Persons)
admin.site.register(Points)
admin.site.register(Product)
admin.site.register(Detail)
admin.site.register(Materials)
admin.site.register(Color)
admin.site.register(Unit)
admin.site.register(Supplier)
admin.site.register(TranType)
