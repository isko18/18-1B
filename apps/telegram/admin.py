from django.contrib import admin
from apps.telegram.models import UserBusiness, Business, UserCklient, Cklient
# Register your models here.

admin.site.register(UserBusiness)
admin.site.register(Business)
admin.site.register(UserCklient)
admin.site.register(Cklient)
