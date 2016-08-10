from django.contrib import admin
from secondexp.models import Politician, SubmitLog
# Register your models here.

class PoliticianAdmin(admin.ModelAdmin):
	list_display = ("name", "photo", "pid")
	list_filter = ("name",)

class SubmitLogAdmin(admin.ModelAdmin):
	list_display = ("token", "shown_list", "affinity_score")
	list_filter = ("token",)

admin.site.register(Politician, PoliticianAdmin)
admin.site.register(SubmitLog, SubmitLogAdmin)
