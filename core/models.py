# -*- Mode: Python; coding: utf-8 -*-
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import os
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

class Tamanho(models.Model):
    nome = models.CharField(u'Tamanho', max_length=40)

    def __unicode__(self):
        return self.nome
    class Meta:
        verbose_name = u'Tamanho'
        verbose_name_plural = u'TAMANHOS'




class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(u'Categoria', max_length=100)
    slug = models.SlugField()
    active = models.CharField(u'Active', blank=True, max_length=10)

    def __unicode__(self):
        return self.nome
    class Meta:
        verbose_name = u'Uma Categoria'
        verbose_name_plural = u'CATEGORIAS'
        ordering = ['id']

class Adicional(models.Model):
    adicional_nome =  models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return self.adicional_nome

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(u'Valor', max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    ativacao = models.BooleanField(u'Ativar/Desativar',default=True)
    slug = models.SlugField(null=True, default=None, max_length=300,
    unique=True, db_index=True)
    description = RichTextUploadingField(u'Descrição', blank=True) 
    image = models.ImageField(blank=True, null=True, upload_to='uploaded_images')
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    produtos = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    #adicional = models.ForeignKey(Adicional, on_delete=models.CASCADE, blank=True, null=True)
    picked = models.ManyToManyField(Adicional, blank=True, related_name='add_adicional')

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    class Meta:
        verbose_name = u'Um item'
        verbose_name_plural = u'ITEM'


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "({0},{1})".format(self.quantity,self.item.title)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    class Meta:
        verbose_name = u'Um item de Pedido'
        verbose_name_plural = u'ITEM DE PEDIDO'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(u'Código de referência', max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(u'Em Processo', default=False)
    being_delivered = models.BooleanField(u'Saiu para Entrega', default=False)
    received = models.BooleanField(u'Entregue', default=False)
    refund_granted = models.BooleanField(u'Pagamento Efetuado', default=False)
    refund_requested = models.BooleanField(u'Pagamento Cancelado', default=False)
    
    
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', related_name='billing_pagamento', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)


    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return str(self.user.username)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    class Meta:
        verbose_name = u'Um Encomendas'
        verbose_name_plural = u'ENCOMENDAS'


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = u'Um Endereço'
        verbose_name_plural = u'ENDEREÇO'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = u'Um Pagamento'
        verbose_name_plural = u'PAGAMENTO'

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = u'Um Cupom'
        verbose_name_plural = u'CUPOM'

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = u'Um Reembolso'
        verbose_name_plural = u'REEMBOLSO'

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)        

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

        