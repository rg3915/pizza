# -*- Mode: Python; coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Item, Categoria, Adicional, Tamanho, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile
from django import forms

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'ATUALIZAR PEDIDOS PARA PAGAMENTOS EFETUADOS'


class SomeForm(forms.ModelForm):
  picked = forms.ModelMultipleChoiceField(queryset=Adicional.objects.all())

  def __init__(self,*args,**kwargs):
    if 'instance' in kwargs:
      initial = kwargs.setdefault('initial',{})
      initial['picked'] = kwargs['instance'].picked.values_list('pk',flat=True)
    super(SomeForm,self).__init__(*args,**kwargs)

  def save(self,*args,**kwargs):
    instance = super(SomeForm,self).save(*args,**kwargs)
    instance.picked = self.cleaned_data['picked']
    return instance
    
# class AdicionalInline(admin.StackedInline):
#     model = Adicional
#     extra = 3

class ItemAdmin(admin.ModelAdmin):
    inlines = [
    #AdicionalInline,
    ]
    list_display = ['title', 'ativacao',]
    list_editable =['ativacao',]
    prepopulated_fields = {'slug' : ('title',)}
    save_on_top=True
class CategoriaAdmin(admin.ModelAdmin):
    pass
    prepopulated_fields = {'slug' : ('nome',)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_granted',
                    'refund_requested',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_granted',
                   'refund_requested']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class TamanhoAdmin(admin.ModelAdmin):
    pass

class AdicionalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Adicional, AdicionalAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Tamanho, TamanhoAdmin)
