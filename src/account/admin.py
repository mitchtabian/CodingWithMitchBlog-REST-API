from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
	list_display = ('pk', 'email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('pk', 'email','username',)
	readonly_fields=('pk', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)



