from django.shortcuts import render
from django.http import HttpResponse
from .models import *  # Import the Registration model
from django.db.models import Max,Min
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db.models import Q
from datetime import date as d, datetime as dt
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib import messages



def index(request):
    return render(request, "index.html")
def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Login.objects.get(view_email=email, view_password=password)
            if user is not None:
                if user.user_type == 'admin':
                    print('admin#####')
                    messages.info(request, 'Welcome to admin dashboard')
                    return redirect('/admin_dash')
                elif user.user_type == 'customer':
                    request.session['cid'] = user.id
                    request.session['cemail'] = user.view_email
                    request.session['type'] = user.user_type
                    print('cust#####')
                    messages.info(request, 'Welcome to customer dashboard')
                    return redirect('/customer_dash')
                elif user.user_type == 'seller':
                    request.session['sid'] = user.id
                    request.session['semail'] = user.view_email
                    request.session['type'] = user.user_type
                    print('seller#####')
                    messages.info(request, 'Welcome to seller dashboard')
                    return redirect('/seller_dash')
                else:
                    pass
            else:
                pass
        except Login.DoesNotExist:
                print("Login matching query does not exist. User not found.")
       
    return render(request, "login.html")
def about(request):
    return render(request, "about.html")
def contact(request):
    return render(request, "contact.html")

def seller_reg(request):
    if request.POST:
        sname = request.POST['sname']
        semail = request.POST['semail']
        password = request.POST['password']
        sphone = request.POST['sphone']
        pimage = request.POST['pimage']
        
        if Login.objects.filter(view_email=semail).exists():
            messages.info(request, 'Already registered')
            return redirect('/')
        else:
            seller_ = Login.objects.create(
                view_email=semail, view_password=password, user_type='seller', is_active=0)
            seller_.save()
            reg = Seller.objects.create(
                username=seller_, sname=sname, semail=semail, sphone=sphone,seller_pimage=pimage)
            reg.save()
            return redirect('/')
    return render(request, "seller_reg.html")
    

def customer_reg(request):
    if request.POST:
        cname = request.POST['cname']
        cemail = request.POST['cemail']
        password = request.POST['password']
        cphone = request.POST['cphone']
        pimage = request.POST['pimage']
        if Login.objects.filter(view_email=cemail).exists():
            messages.info(request, 'Already registered')
            return redirect('/')
        else:
            customer_ = Login.objects.create(
                view_email=cemail, view_password=password, user_type='customer', is_active=0)
            customer_.save()
            reg = Customer.objects.create(
                username=customer_, cname=cname, cemail=cemail, cphone=cphone,customer_pimage=pimage)
            reg.save()
            return redirect('/')
    return render(request, "customer_reg.html")   
 
#seller
def seller_dash(request):
    return render(request, "SELLER/seller_dash.html")


def seller_profile(request):
    id = request.session['sid']
    custreg = Seller.objects.get(username_id=id)
    id = custreg.id
    bid = BidTable.objects.filter(seller_id = id).count()
    Live_auction = onlineAuctionBidTable.objects.filter(uid = id).count()
    return render(request, 'SELLER/seller_profile.html', {"custreg": custreg,'bid':bid,'Live_auction':Live_auction})

def seller_view_bids(request):
    id = request.GET.get('id')
    products = Products.objects.all()
    # bid = BidTable.objects.get(id=id)
    return render(request, 'SELLER/seller_view_bids.html', {'products': products})



def seller_update_profile(request):
    sid = request.session['sid']
    sellreg = Seller.objects.filter(username_id=sid)
    if request.POST:
        sellobj = Seller.objects.get(username_id=sid)
        sellobj.sname = request.POST['sname']
        sellobj.sphone = request.POST['sphone']
        sellobj.seller_pimage = request.POST['pimage']
        sellobj.save()
        messages.info(request, 'Profile updated')
        return redirect('/seller_profile')
    return render(request, 'SELLER/seller_update_profile.html', {"sellreg": sellreg})


def enterPrice(request):
    id = request.GET.get('cid')
    sid = request.session['sid']
    coid = BidTable.objects.filter(id=id)
    print("===================================================================================================================================")
    logid = Login.objects.get(id=sid)
    logemail = logid.view_email
    print(logemail)
    print(sid)
    print(coid)
    user = Seller.objects.get(semail=logemail)
    userid = user.id
    print(userid)
    products = Products.objects.get(id=id)
    customer_id = products.productSeller_id

    bids_amounts = BidTable.objects.filter(product_id=id)
    if request.POST:
        bidAmount = request.POST['bidAmount']
        
        # Check if the bid amount already exists for the product
        existing_bid = BidTable.objects.filter(product_id=id, bidAmount=bidAmount).exists()
        if not existing_bid:
            reg = BidTable.objects.create(
                bidAmount=bidAmount, product_id=id, customer_id=customer_id, seller_id=sid)
            reg.save()
            messages.info(
                request, 'Amount entered successfully')
            return redirect('/seller_view_bids')
        else:
            messages.error(
                request, 'Bid amount already exists for this product.')
    
    return render(request, 'SELLER/enterPrice.html', {'products': products, 'bids_amounts': bids_amounts})

def viewAmountsbided(request):
    sid = request.session.get('sid')

    if sid is None:
        # Handle the absence of 'sid', perhaps redirect or show an error message
        return HttpResponse("Seller ID not found in session.")

    print(sid)
    
    bids = BidTable.objects.filter(seller_id=sid)
    
    # Initialize an empty list to store tuples of (bid, product)
    bids_and_products = []

    # Loop through each bid and get the associated product
    for bid in bids:
        # Access the related product through the ForeignKey relationship
        product_id = bid.product_id
        product = Products.objects.get(id=product_id)

        # Append a tuple of (bid, product) to the bids_and_products list
        bids_and_products.append((bid, product))

    return render(request, 'SELLER/viewAmountsbided.html', {'bids_and_products': bids_and_products})
    #payment?pid={{ products.id }}
#customer
def customer_dash(request):
    return render(request, "CUSTOMER/customer_dash.html")
    
def customer_profile(request):
    cid = request.session['cid']
    customer = Customer.objects.get(username__id = cid)
    id = customer.id
    Contract = Products.objects.filter(productSeller_id = id).count()
    Live_auction = onlineAuctionBidTable.objects.filter(artistid = id).count()
    return render(request, 'CUSTOMER/customer_profile.html', {'customer':customer,'Contract':Contract,'Live_auction':Live_auction})

def cust_update_profile(request):
    cid = request.session['cid']
    custreg = Customer.objects.filter(username_id=cid)
    if request.POST:
        custobj = Customer.objects.get(username_id=cid)
        custobj.cname = request.POST['cname']
        custobj.cphone = request.POST['cphone']
        custobj.customer_pimage = request.POST['pimage']
        
        custobj.save()
        messages.info(request, 'Profile updated')
        return redirect('/customer_profile')
    return render(request, 'CUSTOMER/cust_update_profile.html', {"custreg": custreg})


def addProducts(request):
    cid = request.session['cid']
    productSeller = Customer.objects.get(username=cid)
    if request.POST:
        pname = request.POST['pname']
        pcategory = request.POST['pcategory']
        pdetails = request.POST['pdetails']
        pemail = request.POST['pemail']
        bidDate = request.POST['bidDate']
        price = request.POST['price']

        reg = Products.objects.create(
            productSeller=productSeller, pname=pname, pcategory=pcategory, pdetails=pdetails, bidDate=bidDate, pemail=pemail,price=price)
        reg.save()
        messages.info(
            request, 'New Contract Added')
        return redirect('/viewProductStatus')
    return render(request, 'CUSTOMER/addProducts.html')
    
def viewProductStatus(request):
    cid = request.session['cid']
    customer = Customer.objects.get(username__id = cid)
    id =customer.id
    onl_count=onlineAuction.objects.filter(productSeller_id = id).count()
    products = Products.objects.filter(productSeller_id = id)
    bid = BidTable.objects.filter(customer_id =id )
    if bid.exists():
            bids_and_products = zip(bid, products)
            return render(request, 'CUSTOMER/viewProductStatus.html', {'bids_and_products': bids_and_products,'onl_count': onl_count})
    return render(request, 'CUSTOMER/viewProductStatus.html', {'products': products,'onl_count': onl_count})

def viewallbided_ofaproduct(request):
    pid = request.GET['pid']
    product = Products.objects.get(id = pid)
    bids = BidTable.objects.filter(product_id = pid)
    return render(request, 'CUSTOMER/viewallbided_ofaproduct.html', {'bids':bids,'product':product})

from django.shortcuts import render, get_object_or_404
from .models import Products, BidTable
def viewAcceptedBid(request):
    pid = request.GET['pid']
    product = Products.objects.get(id=pid)
    bids = BidTable.objects.filter(product_id=pid)
    
    bids_and_seller = []
    for bid in bids:
        seller_id = bid.seller_id
        seller = Seller.objects.get(username__id = seller_id)
        bids_and_seller.append((bid, seller))
    
    return render(request, 'CUSTOMER/viewAcceptedBid.html', {'bids_and_seller': bids_and_seller, 'product': product})

from django.shortcuts import render, get_object_or_404
from .models import Products, BidTable

def bidAccept(request):
    pid = request.GET.get('pid')
    bid_id = request.GET.get('bid_id')

    # Update Products model
    product = get_object_or_404(Products, id=pid)
    product.productBidstatus = "Accepted"
    product.save()

    # Update BidTable model
    BidTable.objects.filter(product_id=pid).update(bidstatus="Rejected")

    bid = get_object_or_404(BidTable, id=bid_id)
    bid.bidstatus = "Accepted"
    bid.save()
    return redirect('/customer_dash')
    return render(request, 'CUSTOMER/bidAccept.html')

def bidReject(request):
    pid = request.GET.get('pid')
    bid_id = request.GET.get('bid_id')
    bid_object = BidTable.objects.get(id=bid_id)
    bid_object.bidstatus = "Rejected"
    bid_object.save()

    return redirect('/customer_dash')
    return render(request,'CUSTOMER/bidReject.html')

#admin
def admin_dash(request):
    row_count2 = Login.objects.count()
    row_count3 = Products.objects.count()
    row_count4 = BidTable.objects.count()
    row_count5 = onlineAuction.objects.filter(productBidstatus="requested").count()
    product =Products.objects.all()
    bid = BidTable.objects.all()
    return render(request,"ADMIN/admin_dash.html",{'row_count2':row_count2,'row_count3':row_count3,'row_count4':row_count4,'row_count5':row_count5,'product':product,'bid':bid})

def admin_view_seller(request):
    seller = Seller.objects.all()
    return render(request, 'ADMIN/admin_view_seller.html', {'seller': seller})

def admin_view_customer(request):
    cust = Customer.objects.all()
    return render(request, 'ADMIN/admin_view_customer.html', {'cust': cust})

def admin_aprv_seller(request):
    seller_list = Seller.objects.filter(
        username__is_active=0, s_status='pending')
    return render(request, 'ADMIN/admin_aprv_seller.html', {"seller_list": seller_list})


def admin_approve_single_seller(request):
    sid = request.GET.get('sid')
    seller = Seller.objects.get(id=sid)
    slog = seller.username.id
    sellerreg = Seller.objects.filter(id=sid).update(s_status="Approved")
    username = Login.objects.filter(id=slog).update(is_active=1)
    messages.info(request, "Approved!!!")
    return redirect("/admin_aprv_seller")


def admin_reject_single_seller(request):
    sid = request.GET.get('sid')
    seller = Seller.objects.get(id=sid)
    slog = seller.username.id
    sellerreg = Seller.objects.filter(id=sid).update(s_status="Rejected")
    username = Login.objects.filter(id=slog).delete()
    messages.info(request, "Rejected!!!")
    return redirect("/admin_aprv_seller")

def admin_aprv_customer(request):
    customer_list = Customer.objects.filter(
        username__is_active=0, c_status='pending')
    return render(request, 'ADMIN/admin_aprv_customer.html', {"customer_list": customer_list})


def admin_approve_single_customer(request):
    cid = request.GET.get('cid')
    cust = Customer.objects.get(id=cid)
    clog = cust.username.id
    custreg = Customer.objects.filter(id=cid).update(c_status="Approved")
    username = Login.objects.filter(id=clog).update(is_active=1)
    messages.info(request, "Approved!!!")
    return redirect("/admin_aprv_customer")


def admin_reject_single_customer(request):
    cid = request.GET.get('cid')
    cust = Customer.objects.get(id=cid)
    clog = cust.username.id
    custreg = Customer.objects.filter(id=cid).update(c_status="Rejected")
    username = Login.objects.filter(id=clog).delete()
    messages.info(request, "Rejected!!!")
    return redirect("/admin_aprv_seller")

def admin_delete_cust(request):
    cid = request.GET.get('cid')
    cust = Customer.objects.get(username_id = cid)
    cust_id = cust.id
    co = onlineAuctionBidTable.objects.filter(artistid = cust_id).delete()
    
    coderreg = Login.objects.get(id=cid).delete()
    #coderreg = Customer.objects.filter(id=cid).delete()
    coder_reg = BidTable.objects.filter(customer_id = cust_id).delete()
    

    messages.info(request, 'Customer Deleted!!')
    return redirect('/admin_view_customer')




def admin_delete_seller(request):
    sid = request.GET.get('sid')
    seller = Seller.objects.all()
    bids = BidTable.objects.filter(seller_id = sid)
    for bid in bids:
        if bid.bidstatus == "Accepted":
            pid = bid.product_id
            product = get_object_or_404(Products, id=pid)
            product.productBidstatus = "pending"
            product.save()
        
    sellerreg = Login.objects.get(id=sid).delete()
    #seller_reg = Seller.objects.get(username_id = sid).delete()

    seller_r_eg = BidTable.objects.filter(seller_id = sid).delete()
    messages.info(request, 'Seller Deleted!!')
    return redirect('/admin_view_seller')


# chat


def chat(request):
    uid = request.session["sid"]
    pid = request.GET["id"]
    p = Products.objects.get(id =pid)
    id = p.productSeller_id
    # Artists
    name=""
    artistData = Customer.objects.get(id =id)
    
    getChatData = Chat.objects.filter(Q(uid__username=uid) & Q(artistid=id))
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = Seller.objects.get(username__id=uid)
    if id:
        artistid = Customer.objects.get(id=id)
        name=artistid.cname
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(uid=userid,message=message,artistid=artistid,time=formatted_time,utype="seller")
        sendMsg.save()
    return render(request,"SELLER/chat.html",{"artistData": artistData, "getChatData": getChatData,"artistid":name})


def reply(request):
    uid = request.session["cid"]
    sid = request.GET["id"]
    print(uid)
    id = sid
    name=""
    userData = Seller.objects.get(id =id)
    
    getChatData = Chat.objects.filter(Q(artistid__username=uid) & Q(uid=id))
    print(getChatData)
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    artistid = Customer.objects.get(username=uid)
    if id:
        userid = Seller.objects.get(id=id)
        name=userid.sname
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(uid=userid,message=message,artistid=artistid,time=formatted_time,utype="customer")
        sendMsg.save()
    return render(request,"CUSTOMER/chat.html",{"userData": userData, "getChatData": getChatData,"userid":name ,"id":id})



#online auction
#customer

def online_auction_regi(request):
    cid = request.session['cid']
    productSeller = Customer.objects.get(username=cid)
    if request.POST:
        pname = request.POST['pname']
        pcategory = request.POST['pcategory']
        pdetails = request.POST['pdetails']
        pemail = request.POST['pemail']
        bidDate = request.POST['bidDate']
        bidTime = request.POST['bidTime']
        ampm = request.POST['ampmSelect']
        price = request.POST['price']

        reg = onlineAuction.objects.create(
            productSeller=productSeller, pname=pname, pcategory=pcategory, pdetails=pdetails, bidDate=bidDate, pemail=pemail,price=price,bidTime=bidTime,ampm=ampm)
        reg.save()
        messages.info(
            request, 'New Contract Request Submited')
        return redirect('/viewProductStatus')
    return render(request, 'CUSTOMER/online_auction_regi.html')




    #admin
def view_liveauctionreq(request):
    req = onlineAuction.objects.all()
     
    return render(request, 'ADMIN/view_liveauctionreq.html',{'req':req})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import onlineAuction

def admin_approve_single_request(request):
    pid = request.GET.get('pid')
    online_a = get_object_or_404(onlineAuction, id=pid)
    online_a.productBidstatus = "Approved"
    online_a.save()
    messages.info(request, "Approved!!!")
    return redirect("/view_liveauctionreq")

def admin_reject_single_request(request):
    pid = request.GET.get('pid')
    online_a = get_object_or_404(onlineAuction, id=pid)
    online_a.productBidstatus = "Rejected"
    online_a.save()
    messages.info(request, "Rejected!!!")
    return redirect("/view_liveauctionreq")

from datetime import datetime
def view_online_auctionreq(request):
    cid = request.session['cid']
    customer = Customer.objects.get(username__id = cid)
    id = customer.id
    
    online_a=onlineAuction.objects.filter(productSeller_id = id)
    current_date = date.today()
    current_time = datetime.now().strftime("%H:%M")
    onlinnebid = onlineAuctionBidTable.objects.filter(artistid = id)
   
    return render(request, 'CUSTOMER/view_online_auctionreq.html', {'online_a': online_a,'current_date':current_date,'current_time':current_time,'onlinnebid':onlinnebid})
def view_online_auctionreq_seller(request):
    sid = request.session['sid']
    seller = Seller.objects.get(username__id = sid)
    id = seller.id
    online_a=onlineAuction.objects.all()
    current_date = date.today()
    onlinnebid = onlineAuctionBidTable.objects.filter(uid = id)
    return render(request, 'SELLER/view_online_auctionreq_seller.html', {'online_a': online_a,'current_date':current_date,'onlinnebid':onlinnebid})

def auction_room(request):
    cid = request.session['cid']
    pid = request.GET['pid']
    customer = Customer.objects.get(username__id = cid)
    product = onlineAuction.objects.get(id =pid)
    print(customer.cname)
    if 'start' in request.POST:
            message = request.POST['start']
            online_a = get_object_or_404(onlineAuction, id=pid)
            online_a.productBidstatus = "Started"
            online_a.save()
            request.session['pid'] = pid
            return redirect("auction_room_started", pid=pid)

            
    return render(request, 'CUSTOMER/auction_room.html', {'customer':customer,'product':product})


def auction_room_started(request,pid):
    cid = request.session['cid']
    customer = Customer.objects.get(username__id = cid)
    product = onlineAuction.objects.get(id =pid)
    pname =product.pname
            
    if 'end' in request.POST:
                message = request.POST['end']
                online_a = get_object_or_404(onlineAuction, id=pid)
                online_a.productBidstatus = "Ended"
                online_a.save()
                return redirect("view_online_auctionreq")

   
    
    getChatData_all= auctionroom.objects.filter(pid=pid)

    if request.POST:
        message = request.POST["submit"]
        bid =auctionroom.objects.get(id = message)
        bidamount =bid.bid
        date =bid.date
        time = bid.time
        sid=bid.uid_id
        seller =Seller.objects.get(id = sid)
        cid =customer.id
        semail = seller.semail
        sname = seller.sname
        sphone = seller.sphone
        cemail = customer.cemail
        cname = customer.cname
        cphone = customer.cphone

        sendMsg = onlineAuctionBidTable.objects.create(uid=sid,bid=bidamount,artistid=cid,date = date,time = time, pid =pid, sname =sname, cname = cname, semail = semail, cemail=cemail, sphone = sphone,cphone = cphone,pname=pname)
        sendMsg.save()
        dele_te = auctionroom.objects.filter(pid = pid).delete()
        online_a = get_object_or_404(onlineAuction, id=pid)
        online_a.productBidstatus = "Completed"
        online_a.save()
        return redirect("view_online_auctionreq")

    return render(request, 'CUSTOMER/auction_room_started.html', {'customer':customer,'product':product,'getChatData_all':getChatData_all})

def auction_room_seller(request):
    sid = request.session['sid']
    pid = request.GET['pid']
    seller = Seller.objects.get(username__id = sid)
    product = onlineAuction.objects.get(id =pid)
    print(seller.sname)
    
    p = onlineAuction.objects.get(id =pid)
    id = p.productSeller_id
    # Artists
    name=""
    artistData = Customer.objects.get(id =id)
    getChatData_all= auctionroom.objects.filter(pid=pid)
    getChatData = auctionroom.objects.filter(Q(uid__username=sid) & Q(pid=pid))

    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = Seller.objects.get(username__id=sid)
    if id:
        artistid = Customer.objects.get(id=id)
        name=artistid.cname
    if request.POST:
        message = request.POST["bidamount"]
        sendMsg = auctionroom.objects.create(uid=userid,bid=message,artistid=artistid,time=formatted_time,utype="seller",pid=pid)
        sendMsg.save()

    return render(request, 'SELLER/auction_room_seller.html', {'seller':seller,'product':product,"artistData": artistData, "getChatData": getChatData,"artistid":name,"getChatData_all":getChatData_all})
