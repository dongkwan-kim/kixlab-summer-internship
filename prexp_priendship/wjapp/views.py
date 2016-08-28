from django.shortcuts import render
from django.http import HttpResponse
import firstexp.models as fem
import firstexp.py_submit_log_analyzer as fsla
import secondexp.models as sem
import secondexp.py_submit_log_analyzer as ssla
from wjapp.models import LWJNetwork, VoteNetwork, CoBillNetwork
from wjapp.models import Vote19, VoteVector, CoBill20
import wjapp.py_vote_19 as vt
import wjapp.py_lwj as lwj
import wjapp.py_cobill as cb

from ast import literal_eval 
# Create your views here.

exp_name = "Analysis"

def analyze(request):
	fep_network = fsla.create_visjs_with_whole_process()
	sep_network = ssla.create_visjs_with_whole_process()
	v_network = vt.create_visjs_vote_network()
	lwj_network = lwj.create_visjs_lwj_network()
	
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
		"v_nodes": v_network[0],
		"v_edges": v_network[1],
		"lwj_nodes": lwj_network[0],
		"lwj_edges": lwj_network[1],
		"fep_n": len(fep_user_set),
		"sep_n": len(sep_user_set),
		"exp_name": exp_name
	})

def vote_visualize(request):
	v_network = vt.create_visjs_vote_network()
	return render(request, "wjapp/votevis.html", {"nodes": v_network[0], "edges": v_network[1], "exp_name": "Vote Network of 19th Assembly"})

def lwj_visualize(request):
	lwj_network = lwj.create_visjs_lwj_network()
	return render(request, "wjapp/lwjvis.html", {"nodes": lwj_network[0], "edges": lwj_network[1], "exp_name": "Network of Prof Lee"})

def export_all_db(request, ref):
	"""
	:output: .csv file
	
	p1, p2, w_fep, w_sep, w_[ref]
	.., .., ....., ....., .......,
	"""
	fep_network = fsla.create_network_with_whole_process()
	sep_network = ssla.create_network_with_whole_process()
	p_hash = fsla.create_p_hash()
	pid_hash = dict((y, x) for (x, y) in p_hash.items())
	output = open("db_with_"+ref+".csv", "w")
	
	if ref == "lwj":
		lwj_network = lwj.create_lwj_network(piv_w_value=1)
		for lwj_pair in lwj_network.keys():
			fep_w = fep_network[lwj_pair]
			sep_w = sep_network[lwj_pair]
			lwj_w = lwj_network[lwj_pair]

			line_arr = [p_hash[pid] for pid in lwj_pair] + [str(fep_w), str(sep_w), str(lwj_w)]
			line = ",".join(line_arr)
			output.write(line+"\r\n")
	
	elif ref == "vote":
		v_network = vt.create_vote_network(piv_w_value=1)
		for v_pair in v_network.keys():
			fep_w = fep_network[v_pair]
			sep_w = sep_network[v_pair]
			v_w = v_network[v_pair]

			line_arr = [p_hash[pid] for pid in v_pair] + [str(fep_w), str(sep_w), str(v_w)]
			line = ",".join(line_arr)
			output.write(line+"\r\n")
	
	output.close()	
	return HttpResponse("success!")

def reg_network(request, network, deactive=False):
	if deactive:
		return HttpResponse("Deactived, check the wjapp.views.py")
	
	my_pobj_list = fem.Politician.objects.all()
	my_p_list = [p.name for p in my_pobj_list]
	
	if network == "lwj":
		old_LWJ = LWJNetwork.objects.all()
		for olwj in old_LWJ:
			olwj.delete()

		row_idx = 0
		for line in open("all.csv", "r"):
			if row_idx == 0:
				his_p_list = line.strip().split(",")
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
						LWJ = LWJNetwork(p1=_p1, p2=_p2, weight=_weight)
						LWJ.save()
			row_idx += 1

	elif network == "vote":
		old_vote = VoteNetwork.objects.all()
		for ovote in old_vote:
			ovote.delete()

		vv_list = VoteVector.objects.all()
		p_hash = fsla.create_p_hash()
		
		vvlen = len(vv_list)
		for idx in range(vvlen):
			for jdx in range(idx+1, vvlen):
				vv1 = vv_list[idx]
				vv2 = vv_list[jdx]
				p_pair = sorted([vv1.name, vv2.name])
				weight = 1/(1+vt.get_eud(vv1.vote, vv2.vote))
				Vote = VoteNetwork(p1=p_pair[0], p2=p_pair[1], weight=weight)
				Vote.save()		

	elif db == "cobill":
		old_cb = CoBillNetwork.objects.all()
		for ocb in old_cb:
			ocb.delete()

		cb20_list = CoBill20.objects.all()
		for cb20 in cb20_list:
			p_list = literal_eval(cb20.p_list)
			print(p_list)
			break
	return HttpResponse("success!")

def reg_db(request, db):
	"""
	This function crawls other pages to regiser db.
	So, Use carefully.
	"""
	if db == "vote":
		return HttpResponse("Blocked, check wjapp.views")
		vt.crawl(293)
	
	elif db == "cobill":
		return HttpResponse("Blocked, check wjapp.views")
		cb.crawl_all_bill()

	return HttpResponse("success!")
