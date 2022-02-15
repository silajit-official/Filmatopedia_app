from django.contrib import admin
from .models import ExtendedUser,Suggestion,Group,GroupMember

# Register your models here.
admin.site.register(ExtendedUser)
admin.site.register(Suggestion)
admin.site.register(GroupMember)
admin.site.register(Group)
