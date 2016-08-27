from django.shortcuts import render
from django.http import HttpResponse
import firstexp.models as fem
import firstexp.py_submit_log_analyzer as fsla
import secondexp.models as sem
import secondexp.py_submit_log_analyzer as ssla
from wjapp.models import LWJNetwork
import wjapp.py_vote_19 as vt
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

def vote_manipulate(request, option):
	if option == "crawl":
		return HttpResponse("Blocked, Check the wjapp/views.py")
		vt.crawl(293)
	elif option == "vectorize":
		vt.int_vectorize()
	elif option == "vis":
		v_network = vt.create_visjs_vote_network()
		return render(request, "wjapp/votevis.html", {"nodes": v_network[0], "edges": v_network[1], "exp_name": exp_name})
	else:
		return HttpResponse("check the wjapp/views.py")

	return HttpResponse("Success: "+option)

def export_all_db(request):
	"""
	:output: .csv file
	
	p1, p2, w_fep, w_sep, w_lwj, w_vot
	.., .., ....., ....., ....., .....
	"""
	
	LWJ = LWJNetwork.objects.all()
	fep_network = fsla.create_network_with_whole_process()
	sep_network = ssla.create_network_with_whole_process()

	p_hash = fsla.create_p_hash()
	pid_hash = dict((y, x) for (x, y) in p_hash.items())

	output = open("db.csv", "w")
	for obj_lwj in LWJ:
		pair = [obj_lwj.p1, obj_lwj.p2]
		pid_pair = tuple(sorted([pid_hash[p] for p in pair]))
		fep_w = fep_network[pid_pair]
		sep_w = sep_network[pid_pair]
		
		line_arr = pair + [str(fep_w), str(sep_w), str(obj_lwj.weight)]
		line = ",".join(line_arr)
		output.write(line+"\r\n")
	output.close()
	return HttpResponse("success!")

def reg_db(request, deactive=True):
	if deactive:
		return HttpResponse("Deactived, check the wjapp.views.py")

	# clear db
	old_LWJ = LWJNetwork.objects.all()
	for olwj in old_LWJ:
		olwj.delete()
	
	my_pobj_list = fem.Politician.objects.all()
	my_p_list = [p.name for p in my_pobj_list]
	
	row_idx = 0
	for line in open("all.csv", "r"):
		if row_idx == 0:
			his_p_list = line.strip().split(",")[1:]
			his_p_list = [p.replace("(새)", "") for p in his_p_list]
		elif row_idx >= 300:
			break
		else:
			line_arr = line.split(",")
			for col_idx in range(1, row_idx):
				_p1 = his_p_list[col_idx]
				_p2 = his_p_list[row_idx]
				_weight = float(line_arr[col_idx])
				if _p1 in my_p_list and _p2 in my_p_list:
					_do_i_have = True
				else:
					_do_i_have = False
				
				if _do_i_have:
					LWJ = LWJNetwork(p1=_p1, p2=_p2, weight=_weight, do_i_have=_do_i_have)
					LWJ.save()
		row_idx += 1
	return HttpResponse("success!")
