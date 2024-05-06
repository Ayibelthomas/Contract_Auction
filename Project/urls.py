"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from mpr import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login),
    path('about/',views.about),
    path('contact/',views.contact),
    path('seller_reg/',views.seller_reg),
    path('customer_reg/',views.customer_reg),
    #seller
    path('seller_dash/',views.seller_dash),
    path('seller_profile/',views.seller_profile),
    path('seller_view_bids/',views.seller_view_bids),
    path('enterPrice/',views.enterPrice),
    path('viewAmountsbided/',views.viewAmountsbided),
    path('seller_update_profile/',views.seller_update_profile),
    path('view_online_auctionreq_seller/',views.view_online_auctionreq_seller),
    path('auction_room_seller/',views.auction_room_seller),
   


    #customer
    path('customer_dash/',views.customer_dash),
    path('addProducts/',views.addProducts),
    path('viewProductStatus/',views.viewProductStatus),
    path('customer_profile/',views.customer_profile),
    path('viewallbided_ofaproduct/',views.viewallbided_ofaproduct),
    path('bidAccept/',views.bidAccept),
    path('bidReject/',views.bidReject),
    path('viewAcceptedBid/',views.viewAcceptedBid),
    path('cust_update_profile/',views.cust_update_profile),
    path('online_auction_regi/',views.online_auction_regi),
    path('view_online_auctionreq/',views.view_online_auctionreq , name="view_online_auctionreq"),
    path('auction_room/',views.auction_room),
    path('auction_room_started/<int:pid>/', views.auction_room_started, name='auction_room_started'),

    #admin
    path('admin_dash/',views.admin_dash),
    path('admin_view_seller/',views.admin_view_seller),
    path('admin_view_customer/',views.admin_view_customer),

    path('admin_aprv_seller/',views.admin_aprv_seller),
    path('admin_reject_single_seller/',views.admin_reject_single_seller),
    path('admin_approve_single_seller/',views.admin_approve_single_seller),

    path('admin_aprv_customer/',views.admin_aprv_customer),
    path('admin_approve_single_customer/',views.admin_approve_single_customer),
    path('admin_reject_single_customer/',views.admin_reject_single_customer),

    path('admin_delete_cust/',views.admin_delete_cust),
    path('admin_delete_seller/',views.admin_delete_seller),
    path('view_liveauctionreq/',views.view_liveauctionreq),
    path('admin_approve_single_request/',views.admin_approve_single_request),
    path('admin_reject_single_request/',views.admin_reject_single_request),

     

#chat
path('chat/',views.chat),
path('reply/',views.reply),


]
