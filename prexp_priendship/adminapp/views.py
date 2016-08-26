from django.shortcuts import render
from django.http import HttpResponse
import firstexp.models as fem
import secondexp.models as sem
# Create your views here.

exp_name = ""

def top_front(request):
	return render(request, "real_front.html", {"exp_name": exp_name})

