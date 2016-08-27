from django.contrib import admin
from wjapp.models import LWJNetwork, VoteNetwork, CoBillNetwork
from wjapp.models import Vote19, VoteVector, CoBill20
# Register your models here.

class LWJNetworkAdmin(admin.ModelAdmin):
	list_display = ("p1", "p2", "weight")

class Vote19Admin(admin.ModelAdmin):
	list_display = ("name", "party")

class VoteVectorAdmin(admin.ModelAdmin):
	list_display = ("name", "party")

class VoteNetworkAdmin(admin.ModelAdmin):
	list_display = ("p1", "p2", "weight")

class CoBill20Admin(admin.ModelAdmin):
	list_display = ("bill_no", "p_list")

class CoBillNetworkAdmin(admin.ModelAdmin):
	list_display = ("p1", "p2", "weight")

admin.site.register(LWJNetwork, LWJNetworkAdmin)
admin.site.register(Vote19, Vote19Admin)
admin.site.register(VoteVector, VoteVectorAdmin)
admin.site.register(VoteNetwork, VoteNetworkAdmin)
admin.site.register(CoBill20, CoBill20Admin)
admin.site.register(CoBillNetwork, CoBillNetworkAdmin)
