from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import django
import datetime
import os
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from .models import Address, ExtendedUser, InvoiceState, Invoice, InvoiceNote, InvoiceLineItem, InvoiceLineItemNote, \
    SupplierCustomerRelation

import mimetypes
from django.urls import reverse
from django.shortcuts import redirect


# Default root to the site, if the user is not logged in the system.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "cims/login.html", {"message": None})
    else:
        if request.session['accounttype'] == 'Supplier':
            return_obj = get_all_supplier_invoice(request.user.id)
        else:
            return_obj = get_all_cusotomer_invoice(request.user.id)
        return render(request, "cims/invoices.html", {"message": None,
                                                      'invoice_list': return_obj['invoice_list'],
                                                      'pending_invoices': return_obj['pending_invoices'],
                                                      'pending_invoice_amount': str(
                                                          return_obj['pending_invoice_amount'])})


# view to be rendered post login with a verified username/password, it sets up the account type to be used for the rest of the session
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    if 'accounttype' not in request.POST:
        return render(request, "cims/login.html",
                      {"reason": 'Please select the Account type to login into the system'})

    accounttype = request.POST["accounttype"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        if accounttype == 'Supplier' and not user.extendeduser.supplier:
            return render(request, "cims/login.html",
                          {"reason": 'User doesnot have supplier account, please contact admin for upgrade'})
        elif accounttype == 'Customer' and not user.extendeduser.customer:
            return render(request, "cims/login.html",
                          {"reason": 'User doesnot have customer account, please contact admin for upgrade'})

        login(request, user)
        request.session['accounttype'] = accounttype
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cims/login.html", {"message": "Invalid credentials."})


# view to be rendered for new user registration
def new_user_register_view(request):
    return render(request, "cims/register.html")


# view to be rendered post logout
def logout_view(request):
    logout(request)
    return render(request, "cims/login.html", {"message": "Logged out."})


# view to register a user based on post parameters passed in the request.
def register_view(request):
    username = request.POST["username"]
    email = request.POST["email"]
    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]
    password = request.POST["password"]

    try:
        user = User.objects.create_user(username, email=email, password=password, first_name=firstname,
                                        last_name=lastname)
        Address.objects.create(address1=request.POST["address-line1"], address2=request.POST["address-line2"],
                               city=request.POST["city"], state=request.POST["region"],
                               country=request.POST["country"], user=user, zipcode=request.POST["postal-code"])

        user.extendeduser.businessName = request.POST["businessname"]
        if 'supplieraccount' in request.POST:
            user.extendeduser.supplier = True
        if 'customeraccount' in request.POST:
            user.extendeduser.customer = True
        user.extendeduser.save()
        return render(request, "cims/login.html", {"message": f"Account successfaully created for {username}"})

    except IntegrityError as e:
        return render(request, "cims/register.html",
                      {"error_message": f"Username {username} already has an account. Please login"})


# view to return the information required for creating a new invoice, it returns a list of linked users to make it easiers for creation of an invoice
def new_invoice(request):
    settled_invoice_state = InvoiceState.objects.get(name='Settled')
    returnlist = []
    total_pending_invoices = 0
    total_pending_invoice_amount = 0
    get_linked_cusotomers(request, returnlist, settled_invoice_state, total_pending_invoice_amount,
                          total_pending_invoices)

    return render(request, "cims/create_invoice.html", {"linked_users": returnlist})


# view to return a list of linked customers
def linked_users(request):
    returnlist = []
    total_pending_invoices = 0
    total_pending_invoice_amount = 0

    settled_invoice_state = InvoiceState.objects.get(name='Settled')
    total_pending_invoice_amount, total_pending_invoices = get_linked_cusotomers(request, returnlist,
                                                                                 settled_invoice_state,
                                                                                 total_pending_invoice_amount,
                                                                                 total_pending_invoices)

    return render(request, "cims/users.html",
                  {"message": None, "linked_users": returnlist, 'pending_invoice_count': total_pending_invoices,
                   'pending_invoice_amount': total_pending_invoice_amount})


# api to return the linked customer information including number of invoices, amount pending on invoices
def get_linked_cusotomers(request, returnlist, settled_invoice_state, total_pending_invoice_amount,
                          total_pending_invoices):
    # process each customer
    for linked_customer in SupplierCustomerRelation.objects.filter(supplier=request.user.id).all():
        address = Address.objects.filter(user=linked_customer.customer.id).get()
        unsettled_invoice = {'user_id': linked_customer.customer.id, 'username': linked_customer.customer.username,
                             'first_name': linked_customer.customer.first_name,
                             'last_name': linked_customer.customer.last_name,
                             'bussiness_name': linked_customer.customer.extendeduser.businessName,
                             'address1': address.address1, 'address2': address.address2,
                             'city': address.city, 'state': address.state, 'country': address.country,
                             'pending_invoices': 0, 'amount_due': str(0.00)}
        returnlist.append(unsettled_invoice)
        pending_invoices = Invoice.objects.filter(supplier=request.user.id,
                                                  customer=linked_customer.customer.id).exclude(
            invoiceState=settled_invoice_state.id).all()
        pending_invoice_amt = 0.00
        pending_invocie_count = 0
        # process all the pending invoices
        for pending_invoice in pending_invoices:
            pending_invocie_count += 1
            total_pending_invoices += 1
            pending_invoice_amt += float(pending_invoice.invoiceAmount)
            total_pending_invoice_amount += pending_invoice.invoiceAmount
        unsettled_invoice['pending_invoices'] = pending_invocie_count
        unsettled_invoice['amount_due'] = str(pending_invoice_amt)
    return total_pending_invoice_amount, total_pending_invoices


# view to return a JSON response of the unlinked users in the system
def lookup_unlinked_users(request):
    search_string = request.POST["search_string"]
    unlinked_users = ExtendedUser.objects.filter(businessName__contains=search_string).exclude(
        user_id__in=SupplierCustomerRelation.objects.filter(supplier=request.user.id).values_list('customer',
                                                                                                  flat=True)).all()
    returnList = []
    for unlinked_user in unlinked_users:
        if (unlinked_user.user.id != request.user.id and unlinked_user.customer):
            address = Address.objects.filter(user=unlinked_user.user.id).get()
            returnList.append({'user_id': unlinked_user.user.id, 'business_name': unlinked_user.businessName,
                               "user_email": unlinked_user.user.email,
                               'user_address': f'{address.state},{address.country}'})

    return JsonResponse(json.dumps({"status": 'success',
                                    "user_list": returnList}, cls=DjangoJSONEncoder), safe=False)


# link customers to the given supplier
def add_customer_linking(request):
    if 'user_list' in request.POST:
        users = request.POST["user_list"]
        user_array = users[1:].split(',')
        for user_id in user_array:
            try:
                supplier = User.objects.get(id=request.user.id)
                customer = User.objects.get(id=user_id)

                SupplierCustomerRelation.objects.create(supplier=supplier, customer=customer)
            except IntegrityError as e:
                print(e)
                return_dict = {'status': 'error', 'message': 'Relation already exists with the selected customers'}
                return JsonResponse(json.dumps(return_dict, cls=DjangoJSONEncoder), safe=False)

    return_dict = {'status': 'success'}
    return JsonResponse(json.dumps(return_dict, cls=DjangoJSONEncoder), safe=False)


# view to return all the invoices between the logged in user as supplier and the customer
def customer_linked_invoices(request, cust_id):
    customer = User.objects.get(id=cust_id)
    supplier = User.objects.get(id=request.user.id)
    invoice_list = Invoice.objects.filter(supplier=supplier).filter(customer=customer).all()
    return_obj = process_invoices(invoice_list)
    return render(request, "cims/invoices.html", {"message": None,
                                                  'invoice_list': return_obj['invoice_list'],
                                                  'pending_invoices': return_obj['pending_invoices'],
                                                  'pending_invoice_amount': str(
                                                      return_obj['pending_invoice_amount']), 'cust_id': cust_id,
                                                  'cust_business_name': customer.extendeduser.businessName,
                                                  'cust_email': customer.username})


# api to returns a list of invoice items looking them up across multiple elements the UI
def get_invoice_item_list(request):
    return_list = []
    for i in range(0, int(request.POST['row_count'])):
        f1 = request.FILES.get('inputgroupfile' + str(i), None)
        return_list.append(
            {'description': request.POST['description' + str(i)], 'price': request.POST['price' + str(i)], 'file': f1})

    return return_list


# api to return total invoice price across different items in the invoice
def get_invoice_amount(input_invoice_item_list):
    total = 0.00
    for invoice_item in input_invoice_item_list:
        total += float(invoice_item['price'])
    return total


# api to return a list of invoices for the logger in user
def get_all_cusotomer_invoice(id):
    customer = User.objects.get(id=id)
    invoice_list = Invoice.objects.filter(customer=customer).all()
    return process_invoices(invoice_list)


# api to go over a list of invoices and create count of pending invoices and amount across pending invoices
def process_invoices(invoice_list):
    return_list = []
    pending_invoices = 0
    pending_invoice_amount = 0.00
    for invoice in invoice_list:
        return_list.append(get_invoice_info(invoice))
        if (invoice.invoiceState.name == 'Pending'):
            pending_invoices += 1
            pending_invoice_amount += float(invoice.invoiceAmount)
    return {'invoice_list': return_list, 'pending_invoices': pending_invoices,
            'pending_invoice_amount': str(pending_invoice_amount)}


# api to return a list of invoices created by the currently logged in user
def get_all_supplier_invoice(id):
    supplier = User.objects.get(id=id)
    invoice_list = Invoice.objects.filter(supplier=supplier).all()
    return process_invoices(invoice_list)


# api to return an invoice information as a python dictionary
def get_invoice_info(invoice):
    overdue = False
    if invoice.invoiceDueDate <= datetime.datetime.now().date() and invoice.invoiceState.name == 'Pending':
        overdue = True
    invoice_obj = {'id': invoice.id, 'created_date': invoice.createdTime, 'item_count': invoice.invoiceItemCount,
                   'invoice_state': invoice.invoiceState.name, 'invoice_amount': str(invoice.invoiceAmount),
                   'due_date': invoice.invoiceDueDate, 'description': invoice.description,
                   'update_time': invoice.lastUpdatedTime, 'business_name': invoice.customer.extendeduser.businessName,
                   'customer_id': invoice.customer.id, 'overdue': overdue,
                   'supplier_name': invoice.supplier.extendeduser.businessName, 'supplier_id': invoice.supplier.id}
    inv_line_items = InvoiceLineItem.objects.filter(invoice=invoice).all()
    item_list = []
    invoice_note_list = []
    invoice_obj['item_list'] = item_list
    invoice_obj['item_notes'] = invoice_note_list
    for invoice_line_item in inv_line_items:
        item_list.append(
            {'id': invoice_line_item.id, 'state': invoice_line_item.invoiceLineItemStatus.name,
             'price': invoice_line_item.lineItemPrice,
             'description': invoice_line_item.description, 'no_file': invoice_line_item.document == None})
    invoice_notes = InvoiceNote.objects.filter(invoice=invoice).order_by("createdTime").all()
    for invoice_note in invoice_notes:
        invoice_note_list.append({'id': invoice_note.id, 'description': invoice_note.description,
                                  'createdTime': invoice_note.createdTime, 'sender_id': invoice_note.sender_id,
                                  'sender_username': invoice_note.sender.username})
    return invoice_obj


# view to create a new invoice in the site
def create_invoice(request):
    print(request.POST['row_count'])
    input_invoice_item_list = get_invoice_item_list(request)

    invoice_state = InvoiceState.objects.filter(name='Pending').get()
    invoiceAmount = get_invoice_amount(input_invoice_item_list)
    invoice = Invoice.objects.create(description=request.POST['description'], createdTime=django.utils.timezone.now(),
                                     lastUpdatedTime=django.utils.timezone.now(), invoiceDueDate=request.POST['date'],
                                     invoiceState=invoice_state, invoiceItemCount=len(input_invoice_item_list),
                                     invoiceAmount=invoiceAmount, supplier=User.objects.get(id=request.user.id),
                                     customer=User.objects.get(id=request.POST['linked_customer']))
    if (len(input_invoice_item_list) > 0):
        for invoice_item in input_invoice_item_list:
            InvoiceLineItem.objects.create(lineItemPrice=invoice_item['price'], description=invoice_item['description'],
                                           invoiceLineItemStatus=invoice_state, invoice=invoice,
                                           document=invoice_item['file'])

    if 'note' in request.POST:
        sender = User.objects.get(id=request.user.id)
        InvoiceNote.objects.create(createdTime=django.utils.timezone.now(), description=request.POST['note'],
                                   invoice=invoice, sender=sender)

    return_obj = get_all_supplier_invoice(request.user.id)
    return render(request, "cims/invoices.html",
                  {"message": f'Invoice successfully created {invoice.id}', 'invoice_list': return_obj['invoice_list'],
                   'pending_invoices': return_obj['pending_invoices'],
                   'pending_invoice_amount': str(return_obj['pending_invoice_amount'])})


# view to get details of a specific invoice in the system
def invoice_details(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    invoice_obj = get_invoice_info(invoice)
    return render(request, "cims/invoice-details.html", {"message": None, 'invoice': invoice_obj})


# view to download a file linked to an invoice item id
def download_file(request, item_id):
    invoice_line_item = InvoiceLineItem.objects.get(id=item_id)
    print(invoice_line_item.document.path)
    wrapper = FileWrapper(open(invoice_line_item.document.path, 'rb'))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(invoice_line_item.document.path)[0])
    response['Content-Length'] = os.path.getsize(invoice_line_item.document.path)
    response['Content-Disposition'] = "attachment; filename=" + invoice_line_item.document.path
    return response


# view to post a note against an existing invoice
def post_note(request):
    invoice_id = request.POST['invoice_id']
    note = request.POST['message']

    invoice = Invoice.objects.get(id=invoice_id)
    sender = User.objects.get(id=request.user.id)
    InvoiceNote.objects.create(createdTime=django.utils.timezone.now(), description=note,
                               invoice=invoice, sender=sender)
    return redirect(reverse('invoice_details', kwargs={'invoice_id': invoice_id}))


# view to update the status of an invoice
def update_invoice_status(request, invoice_id, state_id):
    invoice = Invoice.objects.get(id=invoice_id)
    state = InvoiceState.objects.get(name=state_id)
    invoice.invoiceState = state
    invoice.save()
    return redirect(reverse('invoice_details', kwargs={'invoice_id': invoice_id}))
