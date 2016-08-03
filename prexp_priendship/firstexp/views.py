from django.shortcuts import render
from django.http import HttpResponse
from firstexp.models import Politician
from random import shuffle

# Create your views here.

def reg_db(request):
	for p in Politician.objects.all():
		p.delete()
	for line in open("utf8_mod_unified_assembly.txt", "r"):
		ll = line.split("\t")
		_name = ll[0]
		_photo = ll[7]
		new_p = Politician(name=_name, photo=_photo)
		new_p.save()
	return HttpResponse("success!")

def front(request):
	return render(request, "front.html")

def start(request):
	p_list = Politician.objects.all().order_by("?")
	return render(request, "start.html", {"rp_list": p_list[:6]})
