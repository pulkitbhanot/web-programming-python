from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.utils import IntegrityError
from django.shortcuts import render
from .models import CustomerOrder, OrderState, CustomerOrderLineItem, Category, Item, ItemAddOnPrice, AddOn, \
    CategoryAddOnPrice, \
    ItemSizePrice, ServingSize
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import itertools
import django
import ast

# variable to generate next id
newid = itertools.count()


# Default URL mapping that returns all the items currently added in user session.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    categoryList = []
    # iterate over all the categories in the system
    for db_category in Category.objects.all():
        category = {"id": db_category.id, "name": db_category.name, "items": []}
        for db_item in db_category.foodItems.all():
            item = {"id": db_item.id, "name": db_item.name, "category": db_item.category.name,
                    "category_id": db_item.category.id, "prices": []}
            category["items"].append(item)
            if db_item.itemprices:
                custom_add_ons = len(db_item.itemprices.all())
            for sizeprice in db_item.itemsizeprices.all():
                item['prices'].append({'id': sizeprice.id, 'name': sizeprice.size.name, 'price': sizeprice.price,
                                       'addon_limit': (
                                           custom_add_ons if custom_add_ons else sizeprice.addon_restrictions)})

        categoryList.append(category)
    # return response to the user
    context = {
        "user": request.user,
        "categories": categoryList,
        "item_count": request.session['item_count'],
        "total_price": str(round(request.session['total_price'], 2))
    }
    return render(request, "orders/home.html", context)


# Updates state of an order to the state id passed in the URL
def update_order(request, order_id, state_id):
    try:
        order = CustomerOrder.objects.get(pk=order_id)
        new_state = OrderState.objects.get(pk=state_id)
        order.orderState = new_state
        order.save()
        return_order = fetch_order_details(request, order_id)
    except CustomerOrder.DoesNotExist:
        raise Http404("Order does not exists.")
    context = {
        "order": return_order
    }
    return render(request, "orders/order-details.html", context)


# Looks up the order details based on the order id and returns it
def order(request, order_id):
    try:
        return_order = fetch_order_details(request, order_id)
    except CustomerOrder.DoesNotExist:
        raise Http404("Order does not exists.")

    context = {
        "order": return_order
    }
    return render(request, "orders/order-details.html", context)


# returns a dictionary of all the order and related items.
def fetch_order_details(request, order_id):
    # fetch the order
    order = CustomerOrder.objects.get(pk=order_id)
    db_user = User.objects.get(id=order.userId)
    # create the order object
    return_order = {'order_id': order.id, 'order_time': order.orderTime, 'order_state': order.orderState.name,
                    'item_count': order.itemCount, 'order_amount': order.orderAmount, 'items': [],
                    'username': db_user.username, 'first_name': db_user.first_name, 'last_name': db_user.last_name}
    # iterate over all the items
    for orderItem in order.orderitems.all():
        res = ast.literal_eval(orderItem.topping_list)
        return_order['items'].append(
            {'unique_item_id': orderItem.id, 'item_price': orderItem.perItemPrice,
             'item_count': orderItem.itemCount, 'item_name': orderItem.itemName,
             'topping_cost': orderItem.topping_cost, 'cat_name': orderItem.categoryName,
             'item_size_name': orderItem.itemSizeName, 'topping_list': res})
    return return_order


# Returns a list of orders by a user if the user is not a superuser, by all users if the user is a superuser
def order_history(request):
    return_order_list = []
    try:
        if request.user.is_superuser:
            orders = CustomerOrder.objects.order_by('-orderTime').all()
        else:
            orders = CustomerOrder.objects.filter(userId=request.user.id).order_by('-orderTime').all()

        for order in orders:
            return_order_list.append(
                {'order_id': order.id, 'order_time': order.orderTime, 'order_state': order.orderState.name,
                 'item_count': order.itemCount, 'order_amount': order.orderAmount})
    except CustomerOrder.DoesNotExist:
        raise Http404("Order does not exists.")

    context = {
        "order_list": return_order_list
    }
    return render(request, "orders/order-history.html", context)


# view to be rendered post login with a verified username/password
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # initialize key session elements
        request.session['cart'] = []
        request.session['item_count'] = 0
        request.session['total_price'] = 0.00
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


# view to be rendered post logout
def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


# view to be rendered for new user registration
def new_user_register_view(request):
    return render(request, "orders/register.html")


# view to be rendered when user tries to view the items in the cart
def view_cart(request):
    context = {
        "item_count": request.session['item_count'],
        "order_total": str(round(request.session['total_price'], 2)),
        "items": request.session['cart']
    }
    return render(request, "orders/cart.html", context)


# AJAX request handler for adding item with its toppings to the cart
def add_item_to_cart(request):
    item_id = request.POST["item_id"]
    cat_id = request.POST["cat_id"]
    price_id = request.POST["price_id"]

    topping_list = []
    topping_cost = 0.00
    # if the item has toppings
    if 'topping_list' in request.POST:
        toppings = request.POST["topping_list"]

        # validate the topping list for the item
        topping_array = toppings[1:].split(',')

        # lookup the item price
        db_item_price = ItemSizePrice.objects.get(pk=price_id)
        # return error if number of addons is greater then that allowed for the item
        if len(topping_array) > db_item_price.addon_restrictions:
            return JsonResponse(json.dumps({"status": 'error',
                                            'message': f'This item can only have upto {db_item_price.addon_restrictions} toppings'}),
                                safe=False)
        else:
            topping_cost = process_toppings(cat_id, item_id, topping_array, topping_cost, topping_list)

    if not 'cart' in request.session:
        request.session['cart'] = []
        request.session['item_count'] = 0
        request.session['total_price'] = 0.00

    return_dict = add_item_toppings_to_cart(cat_id, item_id, price_id, request, topping_cost, topping_list)
    return JsonResponse(json.dumps(return_dict, cls=DjangoJSONEncoder), safe=False)


# internal methos for processing a list of toppings for an item
def process_toppings(cat_id, item_id, topping_array, topping_cost, topping_list):
    for topping_id in topping_array:
        try:
            # item level addon takes priority
            add_on_price = ItemAddOnPrice.objects.filter(item=item_id).filter(addon=topping_id).get()
            if add_on_price:
                topping_list.append({'topping_id': add_on_price.addon.id, 'price': float(add_on_price.price),
                                     'topping_name': add_on_price.addon.name})
                topping_cost = topping_cost + float(add_on_price.price)
        except ItemAddOnPrice.DoesNotExist:
            print("ItemAddon price lookup failed, category addon price would be reattempted")
            # if addon id is not in item level override, lookup in category add on list
            try:
                add_on_price = CategoryAddOnPrice.objects.filter(category=cat_id).filter(addon=topping_id).get()
                if add_on_price:
                    topping_list.append(
                        {'topping_id': add_on_price.addon.id, 'price': float(add_on_price.price),
                         'topping_name': add_on_price.addon.name})
                    topping_cost = topping_cost + float(add_on_price.price)
            except CategoryAddOnPrice.DoesNotExist:
                print("CategoryAddOnPrice price lookup failed, something is wrong")
    return topping_cost


# internal api to add item and topping information to cart and update the total
def add_item_toppings_to_cart(cat_id, item_id, price_id, request, topping_cost, topping_list):
    db_item = Item.objects.get(pk=item_id)
    db_item_price = ItemSizePrice.objects.get(pk=price_id)
    db_category = Category.objects.get(pk=cat_id)
    menu_item = {'unique_item_id': str(next(newid)), 'item_id': item_id, 'cat_id': cat_id, 'cat_name': db_category.name,
                 'price_id': price_id,
                 'item_name': db_item.name,
                 'item_size_name': db_item_price.size.name, 'item_price': float(db_item_price.price),
                 'topping_list': topping_list, 'topping_cost': topping_cost}
    request.session['cart'].append(menu_item)
    request.session['item_count'] += 1
    request.session['total_price'] = request.session['total_price'] + float(db_item_price.price) + topping_cost
    return_dict = {"status": 'success', "item_count": str(request.session['item_count']),
                   "total_price": str(round(request.session['total_price'], 2))}
    return return_dict


# AJAX api to return a list of toppings for an item.Currently an item can have item level topping and a category level topping
def topping_list_for_item(request):
    item_id = request.POST["item_id"]
    cat_id = request.POST["cat_id"]
    price_id = request.POST["price_id"]

    initialize_session(request)

    db_item = Item.objects.get(pk=item_id)
    item_toppings = db_item.itemprices.all()
    topping_list = []
    # Process for item level topping
    if item_toppings:
        for topping in item_toppings:
            topping_list.append({'item_id': item_id, 'item_name': db_item.name, 'price_id': price_id, 'cat_id': cat_id,
                                 'topping_id': topping.addon.id, 'topping_name': topping.addon.name,
                                 'topping_price': topping.price})
    else:
        # Process for category level topping
        db_category = Category.objects.get(pk=cat_id)
        item_toppings = db_category.categoryprices.all()
        for topping in item_toppings:
            topping_list.append({'item_id': item_id, 'item_name': db_item.name, 'price_id': price_id, 'cat_id': cat_id,
                                 'topping_id': topping.addon.id, 'topping_name': topping.addon.name,
                                 'topping_price': topping.price})
    return JsonResponse(json.dumps(topping_list, cls=DjangoJSONEncoder), safe=False)


# Add default values for session variables
def initialize_session(request):
    if not 'cart' in request.session:
        request.session['cart'] = []
        request.session['item_count'] = 0
        request.session['total_price'] = 0.00


# AJAX api to delete item
def delete_item(request):
    item_id = request.POST["item_id"]
    cat_id = request.POST["cat_id"]
    item_unique_id = request.POST["item_unique_id"]
    for idx, val in enumerate(request.session['cart']):
        if item_unique_id == val['unique_item_id']:
            request.session['cart'].pop(idx)
            break

    recomputetotal(request)
    return_dict = {"status": 'success', "item_count": str(request.session['item_count']),
                   "total_price": str(round(request.session['total_price'], 2))}
    return JsonResponse(json.dumps(return_dict, cls=DjangoJSONEncoder), safe=False)


# AJAX api to clear cart
def clear_cart(request):
    request.session['cart'] = []
    request.session['item_count'] = 0
    request.session['total_price'] = 0.00
    return_dict = {"status": 'success', "item_count": str(request.session['item_count']),
                   "total_price": str(round(request.session['total_price'], 2))}
    return JsonResponse(json.dumps(return_dict, cls=DjangoJSONEncoder), safe=False)


# AJAX api to create an order
def place_order(request):
    # lookup default order state
    orderstate = OrderState.objects.filter(name='Created').get()
    # create order
    db_order = CustomerOrder.objects.create(itemCount=request.session['item_count'],
                                            orderAmount=request.session['total_price'],
                                            orderTime=django.utils.timezone.now(), orderState=orderstate,
                                            userId=request.user.id)

    # create all the lineitems for the order
    for idx, val in enumerate(request.session['cart']):
        db_order_item = CustomerOrderLineItem.objects.create(itemCount=1, perItemPrice=val['item_price'],
                                                             topping_cost=val['topping_cost'],
                                                             itemName=val['item_name'], categoryName=val['cat_name'],
                                                             itemSizeName=val['item_size_name'],
                                                             topping_list=val['topping_list'], order=db_order)
    request.session['cart'] = []
    request.session['item_count'] = 0
    request.session['total_price'] = 0.00
    return_dict = {"status": 'success', "order_id": db_order.id, "item_count": str(request.session['item_count']),
                   "total_price": str(round(request.session['total_price'], 2))}

    return JsonResponse(json.dumps(return_dict, cls=DjangoJSONEncoder), safe=False)


# method to recompute total of the cart post addition/deleteion of items
def recomputetotal(request):
    total = 0.0
    item_count = 0

    for idx, val in enumerate(request.session['cart']):
        total = total + val['topping_cost'] + val['item_price']
        item_count += 1
    request.session['item_count'] = item_count
    request.session['total_price'] = total


# view to register a user based on post parameters passed in the request.
def register_view(request):
    username = request.POST["username"]
    email = request.POST["email"]
    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]
    password = request.POST["password"]

    try:
        User.objects.create_user(username, email=email, password=password, first_name=firstname,
                                 last_name=lastname)
    except IntegrityError:
        return render(request, "orders/register.html",
                      {"error_message": f"Username {username} already has an account. Please login"})

    return render(request, "orders/login.html", {"message": f"Account successfaully created for {username}"})
