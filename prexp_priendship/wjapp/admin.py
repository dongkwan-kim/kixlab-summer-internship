from django.contrib import admin
from wjapp.models import LWJNetwork, Vote19, VoteVector
# Register your models here.


class LWJNetworkAdmin(admin.ModelAdmin):
	list_display = ("p1", "p2", "weight", "do_i_have")
	list_filter = ("do_i_have",)

class Vote19Admin(admin.ModelAdmin):
	list_display = ("name", "party")

class VoteVectorAdmin(admin.ModelAdmin):
	list_display = ("name", "party")

admin.site.register(LWJNetwork, LWJNetworkAdmin)
admin.site.register(Vote19, Vote19Admin)
admin.site.register(VoteVector, VoteVectorAdmin)
