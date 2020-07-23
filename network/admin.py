from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import posts
from .models import profile
from .models import likes
# Register your models here.
admin.site.register(User, UserAdmin)  
admin.site.register(posts)
admin.site.register(profile)
admin.site.register(likes)