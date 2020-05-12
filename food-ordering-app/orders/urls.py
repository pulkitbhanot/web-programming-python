from django.urls import path
from django.contrib import admin


from . import views

urlpatterns = [
    path("", views.index, name="index"), # default url mapping
    path("admin/", admin.site.urls), # url mapping for the admin site
    path("order/<int:order_id>", views.order, name="order"), # url for accessing order details of a specific order
    path("order_history", views.order_history, name="order_history"), # url for accessing all the order for a user or in the system
    path("login", views.login_view, name="login"), #url for logging into the system
    path("logout", views.logout_view, name="logout"), #url for logging out
    path("register_account", views.new_user_register_view, name="register_account"),
    path("register", views.register_view, name="register"), #url for registerig a user
    path("add_item", views.add_item_to_cart, name="add_item"), # url for adding an item
    path("topping_list", views.topping_list_for_item, name="topping_list"), # url for getting a list of toppings
    path("view_cart", views.view_cart, name="view_cart"), #  url for viewing all the items in the cart
    path("delete_item", views.delete_item, name="delete_item"), # url for deleting an item from the cart
    path("clear_cart", views.clear_cart, name="clear_cart"), # url for clearing the cart
    path("place_order", views.place_order, name="place_order"), # url for placing an order
    path("update_order/<int:order_id>/<int:state_id>", views.update_order, name="update_order") #url for updating state of an order in the system

]
