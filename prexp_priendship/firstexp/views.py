from django.shortcuts import render
from django.http import HttpResponse
from firstexp.models import Politician, SubmitLog
from random import randrange

# Create your views here.

class Question():
	def __init__(self, content, color):
		self.content = content
		self.color = color

q_list = [Question("친하", "green"), Question("안 친하", "red")]

def reg_db(request):
	for p in Politician.objects.all():
		p.delete()
	for line in open("utf8_mod_unified_assembly.txt", "r"):
		ll = line.split("\t")
		_name = ll[0]
		_photo = ll[7]
		_pid = int(ll[7].split("/")[-1].split(".jpg")[0])
		new_p = Politician(name=_name, photo=_photo, pid=_pid)
		new_p.save()
	return HttpResponse("success!")

def front(request):
	return render(request, "front.html")

def start(request):
	if request.method == "POST":
		print(request.POST)
		_token = request.POST["csrfmiddlewaretoken"]
		_q_kind = request.POST["q_kind"]
		_shown_list = request.POST["shown_p"]
		_select_list = request.POST["select_p"]
		new_log = SubmitLog(token=_token, q_kind=_q_kind, shown_list=_shown_list, select_list=_select_list)
		new_log.save()

	p_list = Politician.objects.all().order_by("?")
	return render(request, "start.html", {"rp_list": p_list[:6], "q_kind": q_list[randrange(0, 2)]})
