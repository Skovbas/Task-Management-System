from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account, Task, Category, Comment
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ("email", 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Account, AccountAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ("title","priority" ,"creation_date", "due_date", "is_done")
    search_fields = ('title', 'description')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    
admin.site.register(Task, TaskAdmin)
admin.site.register(Category)
admin.site.register(Comment)
