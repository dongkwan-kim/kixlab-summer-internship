from django.shortcuts import render

# Create your views here.
exp_name = ""

def top_front(request):	
	return render(request, "real_front.html", {"exp_name": exp_name})
