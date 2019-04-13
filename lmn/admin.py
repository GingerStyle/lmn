from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here, for them to be displayed in the admin view

from .models import Venue, Artist, Note, Show, CustomUser

admin.site.register([Venue, Artist])
admin.site.register([Note, Show])
admin.site.register(CustomUser)
