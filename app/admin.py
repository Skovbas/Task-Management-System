from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Account, Task, Category, Comment, Notification, AdminNotification, AdditionInformationForUser
from django import forms
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
    
class SendNotificationForm(forms.Form):
    message = forms.CharField(label="Notification Message", max_length=200)

@admin.register(AdminNotification)
class NotificationAdmin(admin.ModelAdmin):
    add_form_template = "admin/custom_add_form.html"

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            form = SendNotificationForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data["message"]

                notification = AdminNotification.objects.create(message=message)

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "notifications",
                    {
                        "type": "send_notification",
                        "message": message
                    }
                )

                return HttpResponseRedirect("../{}/".format(notification.pk))
        else:
            form = SendNotificationForm()

        context = self.get_changeform_initial_data(request)
        context["form"] = form
        return super().add_view(request, form_url, extra_context=context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_url = [
            path("send-notification/", self.admin_site.admin_view(self.add_view), name="send-notification"),
        ]
        return custom_url + urls
    
admin.site.register(Task, TaskAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(AdditionInformationForUser)