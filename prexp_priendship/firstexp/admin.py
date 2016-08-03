from django.contrib import admin
from firstexp.models import Politician
# Register your models here.

class PoliticianAdmin(admin.ModelAdmin):
	list_display = ("name", "photo")
	list_filter = ("name",)


admin.site.register(Politician, PoliticianAdmin)
