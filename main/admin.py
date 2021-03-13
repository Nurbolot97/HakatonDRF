from django.contrib import admin
from django import forms
from .models import *
from django.forms import ModelForm, ValidationError, ModelChoiceField




class WheelAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='wheels'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EngineAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='engines'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DisplayAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='displays'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Category)
admin.site.register(Wheel, WheelAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(Display, DisplayAdmin)






