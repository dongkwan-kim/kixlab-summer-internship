from django.shortcuts import render
from django.http import HttpResponse
import firstexp.models as fem
import secondexp.models as sem
import firstexp.py_submit_log_analyzer as fsla
import secondexp.py_submit_log_analyzer as ssla
# Create your views here.

exp_name = "with Prof. Lee wonjae"

def analyze(request):
	fep_network = fsla.create_visjs_with_whole_process()
	sep_network = ssla.create_visjs_with_whole_process()
	fep_slog_list = fem.SubmitLog.objects.all()
	sep_slog_list = sem.SubmitLog.objects.all()

	fep_user_set = set([u.token for u in fep_slog_list])
	sep_user_set = set([u.token for u in sep_slog_list])
	return render(request, "wjapp/analyze.html",
	{
		"fep_nodes": fep_network[0],
		"fep_edges": fep_network[1],
		"sep_nodes": sep_network[0],
		"sep_edges": sep_network[1],
		"fep_n": len(fep_user_set),
		"sep_n": len(sep_user_set),
		"exp_name": exp_name
	})

def reg_db(request):
	for line in open("utf8_mod_unified_assembly_50.txt", "r"):
		ll = line.split("\t")
		_name = ll[0]
		_photo = ll[7]
		_pid = int(ll[7].split("/")[-1].split(".jpg")[0])
		new_p = Politician(name=_name, photo=_photo, pid=_pid)
		new_p.save()
	return HttpResponse("success!")

