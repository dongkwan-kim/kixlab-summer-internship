from django.contrib import admin
from wjapp.models import LWJNetwork
# Register your models here.


class LWJNetworkAdmin(admin.ModelAdmin):
	list_display = ("p1", "p2", "weight", "do_i_have")
	list_filter = ("do_i_have",)

admin.site.register(LWJNetwork, LWJNetworkAdmin)
