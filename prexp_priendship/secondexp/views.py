from django.shortcuts import render
from django.http import HttpResponse
from secondexp.models import Politician, SubmitLog
from random import randrange
import secondexp.py_submit_log_analyzer as sla
import secondexp.py_newsapi as na

# binary realtion with news api
exp_name = "2nd prototype"

def reg_db(request):
	for p in Politician.objects.all():
		p.delete()
	for line in open("mod_utf8_unified_assembly_50.txt", "r"):
		ll = line.split("\t")
		_name = ll[0]
		_photo = ll[7]
		_pid = int(ll[7].split("/")[-1].split(".jpg")[0])
		new_p = Politician(name=_name, photo=_photo, pid=_pid)
		new_p.save()
	return HttpResponse("success!")

def export_logs(request):
	out_file = open("submit_logs.txt", "w")
	for sl in SubmitLog.objects.all():
		line = "\t".join([sl.token,
						  sl.shown_list,
						  sl.select_list
						])
		out_file.write(line+"\r\n")
	out_file.close()
	return HttpResponse("success!")

def visualize(request):
	visjs_network = sla.create_visjs_with_whole_process()
	return render(request, "secondexp/resultvis.html", {"nodes": visjs_network[0], "edges": visjs_network[1], "exp_name": exp_name})

def front(request):
	return render(request, "secondexp/front.html", {"exp_name": exp_name})

def start(request):
	# how many did a user solve
	num_of_sol = 0
	if request.method == "POST":
		print(request.POST)
		# log save
		_token = request.POST["csrfmiddlewaretoken"]
		_shown_list = request.POST["shown_p"]
		_affinity_score = request.POST["affinity_score"]
		new_log = SubmitLog(token=_token, shown_list=_shown_list, affinity_score=_affinity_score)
		new_log.save()
		# num_of_sol update
		log_list = SubmitLog.objects.filter(token=_token)
		num_of_sol = len(log_list)
	
	# random sort
	p_list = Politician.objects.all().order_by("?")
	rp_list = p_list[:2]
	nn = na.NaverNewsXML(" ".join([str(x.name) for x in rp_list]), display=3)
	news_list = nn.get_news_items()
	
	return render(request, "secondexp/start.html", {"rp_list": rp_list, "nos": num_of_sol, "exp_name": exp_name, "news_list": news_list})
