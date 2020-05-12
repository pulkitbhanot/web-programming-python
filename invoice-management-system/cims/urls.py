"""cims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    # url for logging into the system
    path("login", views.login_view, name="login"),
    # url for logging out
    path("logout", views.logout_view, name="logout"),
    path("register_account", views.new_user_register_view, name="register_account"),
    # url for registerig a user
    path("register", views.register_view, name="register"),
    # url for creating a new invoice
    path("new_invoice", views.new_invoice, name="new_invoice"),
    # url for submitting the invoice details for an invoice
    path("create_invoice", views.create_invoice, name="create_invoice"),
    # url for linked_users a user
    path("linked_users", views.linked_users, name="linked_users"),
    # AJAX url for unlinked userlist
    path("lookup_unlinked_users", views.lookup_unlinked_users, name="lookup_unlinked_users"),
    # AJAX url for linking userlist
    path("add_customer_linking", views.add_customer_linking, name="add_customer_linking"),
    # url for accessing all the linked customer invoices
    path("customer_linked_invoices/<int:cust_id>", views.customer_linked_invoices, name="customer_linked_invoices"),
    # url for accessing invoice details of a specific invoice
    path("invoice_details/<int:invoice_id>", views.invoice_details, name="invoice_details"),
    # url for accessing order details of a specific order
    path("download_file/<int:item_id>", views.download_file, name="download_file"),
    # url for adding a note to an invoice
    path("post_note", views.post_note, name="post_note"),
    # url for adding a note to an invoice
    path("update_invoice_status/<int:invoice_id>/<str:state_id>", views.update_invoice_status,
         name="update_invoice_status"),

]

urlpatterns += static(settings.MEDIA_URL)
