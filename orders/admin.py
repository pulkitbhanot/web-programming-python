from django.contrib import admin

from orders.models import CustomerOrder, CustomerOrderLineItem, OrderState, Category, Item, ItemAddOnPrice, AddOn, CategoryAddOnPrice, ItemSizePrice, ServingSize

# Register your models here.

admin.site.register(CustomerOrder)
admin.site.register(OrderState)
admin.site.register(CustomerOrderLineItem)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemAddOnPrice)
admin.site.register(AddOn)
admin.site.register(CategoryAddOnPrice)
admin.site.register(ItemSizePrice)
admin.site.register(ServingSize)
