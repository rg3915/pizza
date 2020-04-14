# -*- Mode: Python; coding: utf-8 -*-
from django.conf.urls import *
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    pedido
)

app_name = 'core'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^resumo-do-pedido/$', OrderSummaryView.as_view(), name='order-summary'),
    url(r'^produto/(?P<slug>[\w-]+)/$', ItemDetailView.as_view(), name='product'),
    url(r'^add-to-cart/(?P<slug>[\w-]+)/$', add_to_cart, name='add-to-cart'),
    url(r'^add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    url(r'^remove-from-cart/(?P<slug>[\w-]+)/$', remove_from_cart, name='remove-from-cart'),
    url(r'^remove-item-from-cart/(?P<slug>[\w-]+)/$', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    url(r'^pagamento/(?P<payment_option>[-\w]+)/$', PaymentView.as_view(), name='payment'),
    url(r'^request-refund/$', RequestRefundView.as_view(), name='request-refund'),
    url(r'^pedido/(?P<id>[-\w]+)/$',pedido, name="pedido"),
]
