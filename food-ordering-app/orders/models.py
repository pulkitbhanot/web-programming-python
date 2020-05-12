from django.db import models


# Model for Category object.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} - {self.name}"


# Model for Item object.
class Item(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="foodItems")

    def __str__(self):
        return f"{self.id} - {self.category} - {self.name}"


# Model for ServingSize object.
class ServingSize(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} - {self.name}"


# Model for Topping object.
class AddOn(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} - {self.name}"


# Model for representing category to addon prices. E,g for Pizzas
class CategoryAddOnPrice(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categoryprices")
    addon = models.ForeignKey(AddOn, on_delete=models.CASCADE, related_name="cataddonprices")

    class Meta:
        unique_together = (('category', 'addon'),)

    def __str__(self):
        return f"{self.id} - {self.category} - {self.addon} - ({self.price}) "


# Model for storing Item and the sizes it supports
class ItemSizePrice(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="itemsizeprices")
    size = models.ForeignKey(ServingSize, on_delete=models.CASCADE, related_name="sizeprices")
    addon_restrictions = models.IntegerField()

    class Meta:
        unique_together = (('item', 'size'),)

    def __str__(self):
        return f"{self.id} - {self.item} - {self.size} - ({self.price}) "


# Model for representing category to item prices. E,g for Steak + Cheese subs where toppings are paid
class ItemAddOnPrice(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="itemprices")
    addon = models.ForeignKey(AddOn, on_delete=models.CASCADE, related_name="itemaddonprices")

    class Meta:
        unique_together = (('item', 'addon'),)

    def __str__(self):
        return f"{self.id} - {self.item} - {self.addon} - ({self.price}) "


# Model for storing Order state
class OrderState(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} - {self.name}"


# Model for storing all the orders in the system
class CustomerOrder(models.Model):
    itemCount = models.IntegerField()
    orderAmount = models.DecimalField(max_digits=5, decimal_places=2)
    orderTime = models.DateTimeField()
    orderState = models.ForeignKey(OrderState, on_delete=models.CASCADE, related_name="orderstates")
    userId = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.id} - {self.itemCount} - {self.orderTime} - {self.orderState} - ({self.orderAmount})"


# Model for storing items that were ordered as part of an orderin the system
class CustomerOrderLineItem(models.Model):
    itemCount = models.IntegerField()
    perItemPrice = models.DecimalField(max_digits=5, decimal_places=2)
    topping_cost = models.DecimalField(max_digits=5, decimal_places=2)
    itemName = models.CharField(max_length=64)
    categoryName = models.CharField(max_length=64)
    itemSizeName = models.CharField(max_length=64)
    topping_list = models.CharField(max_length=500)
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name="orderitems")

    def __str__(self):
        return f"{self.itemName} - {self.itemCount} - ({self.perItemPrice})"
