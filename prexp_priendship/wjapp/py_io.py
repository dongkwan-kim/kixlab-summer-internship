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
	
	if ref == "all":
		all_pair = get_set_of_pair(p_hash.keys())
		lwj_network = lwj.create_lwj_network(piv_w_value=1)
		v_network = vt.create_vote_network(piv_w_value=1)
		cb_network = cb.create_cb_network(piv_w_value=1)
		output.write(",".join(["p1", "p2", "fep_w", "sep_w", "v_w", "lwj_w", "cb_w"])+"\r\n")
		for pair in all_pair:
			fep_w = get_w(fep_network, pair)
			sep_w = get_w(sep_network, pair)
			lwj_w = get_w(lwj_network, pair)
			v_w = get_w(v_network, pair)
			cb_w = get_w(cb_network, pair)
			
			line_arr = [p_hash[pid] for pid in pair] + [str(fep_w), str(sep_w), str(v_w), str(lwj_w), str(cb_w)]
			line = ",".join(line_arr)
			output.write(line+"\r\n")
	

	elif ref == "lwj":
		lwj_network = lwj.create_lwj_network(piv_w_value=1)
		for lwj_pair in lwj_network.keys():
			fep_w = get_w(fep_network, lwj_pair)
			sep_w = get_w(sep_network, lwj_pair)
			lwj_w = lwj_network[lwj_pair]

			line_arr = [p_hash[pid] for pid in lwj_pair] + [str(fep_w), str(sep_w), str(lwj_w)]
			line = ",".join(line_arr)
			output.write(line+"\r\n")
	
	elif ref == "vote":
		v_network = vt.create_vote_network(piv_w_value=1)
		for v_pair in v_network.keys():
			fep_w = get_w(fep_network, v_pair)
			sep_w = get_w(sep_network, v_pair)
			v_w = v_network[v_pair]

			line_arr = [p_hash[pid] for pid in v_pair] + [str(fep_w), str(sep_w), str(v_w)]
			line = ",".join(line_arr)
			output.write(line+"\r\n")
	
	elif ref == "cobill":
		cb_network = cb.create_cb_network(piv_w_value=1)
		for cb_pair in cb_network.keys():
			fep_w = get_w(fep_network, cb_pair)
			sep_w = get_w(sep_network, cb_pair)
			cb_w = cb_network[cb_pair]
		
			line_arr = [p_hash[pid] for pid in cb_pair] + [str(fep_w), str(sep_w), str(cb_w)]
			line = ",".join(line_arr)
			output.write(line+"\r\n")

	output.close()	
	return HttpResponse("success!")

def get_w(network, pair):
	try:
		return network[pair]
	except KeyError:
		return "-"

def reg_network(request, network):
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
	
		piv_attendance = 0.34 # = avg - 1*stdev
		vvlen = len(vv_list)
		for idx in range(vvlen):
			for jdx in range(idx+1, vvlen):
				vv1 = vv_list[idx]
				vv2 = vv_list[jdx]
				if vt.get_attendance(vv1.vote) > piv_attendance\
					and vt.get_attendance(vv2.vote) > piv_attendance:
					p_pair = sorted([vv1.name, vv2.name])
					weight = 1/(1+vt.get_eud(vv1.vote, vv2.vote))
					Vote = VoteNetwork(p1=p_pair[0], p2=p_pair[1], weight=weight)
					Vote.save()		

	elif network == "cobillud":
		old_cb = CoBillNetwork.objects.all()
		for ocb in old_cb:
			ocb.delete()
		
		pair_list = get_set_of_pair(my_p_list)
		p_cnt_hash = dict([(str(p), 0) for p in my_p_list])
		cb_network = dict([(x, 0) for x in pair_list])
		cb20_list = CoBill20.objects.all()
		for cb20 in cb20_list:
			p_list = literal_eval(cb20.p_list)
			intersection_list = []
			for p in p_list:
				p_name = p.split("_")[0]
				if p_name in my_p_list:
					if p_name in ["김성태", "최경환"]:
						if p.split("_")[1] in ["金聖泰", "崔炅煥"]:
							intersection_list.append(p_name)
							p_cnt_hash[p_name] += 1
					else:
						intersection_list.append(p_name)
						p_cnt_hash[p_name] += 1
			i_pair_list = get_set_of_pair(intersection_list)
			for p_tuple in i_pair_list:
				cb_network[p_tuple] += 1
		
		for ((p1, p2), weight) in cb_network.items():
			if weight > 0:
				union = p_cnt_hash[p1]+p_cnt_hash[p2]-weight
				if union > 36: # = avg - 1*stdev
					j_weight = weight/union
					cobill = CoBillNetwork(p1=p1, p2=p2, weight=j_weight)
					cobill.save()

	elif network == "cobilld":
		old_cb = CoBillNetwork.objects.all()
		for ocb in old_cb:
			ocb.delete()
		
		pair_list = get_list_of_pair(my_p_list)
		p_cnt_hash = dict([(str(p), 0) for p in my_p_list])
		cb_network = dict([(x, 0) for x in pair_list])
		cb20_list = CoBill20.objects.all()
		for cb20 in cb20_list:
			p_list = literal_eval(cb20.p_list)

			leader_p = p_list[0]
			leader_name = leader_p.split("_")[0]
			if leader_name in my_p_list:
				if leader_name in ["김성태", "최경환"]:
					if leader_p.split("_")[1] not in ["金聖泰", "崔炅煥"]:
						continue
			else:
				continue

			intersection_list = []
			for p in p_list:
				p_name = p.split("_")[0]
				if p_name in my_p_list:
					if p_name in ["김성태", "최경환"]:
						if p.split("_")[1] in ["金聖泰", "崔炅煥"]:
							intersection_list.append(p_name)
							p_cnt_hash[p_name] += 1
					else:
						intersection_list.append(p_name)
						p_cnt_hash[p_name] += 1
			
			for ip in intersection_list:
				if leader_name != ip:
					cb_network[(leader_name, ip)] += 1
		
		rcb_network = {}
		for ((p1, p2), weight) in cb_network.items():
			sorted_p = tuple(sorted([p1, p2]))
			rcb_network[sorted_p] = cb_network[(p1, p2)] + cb_network[(p2, p1)]

		for ((p1, p2), weight) in rcb_network.items():
			if weight > 0:
				cobill = CoBillNetwork(p1=p1, p2=p2, weight=weight)
				cobill.save()

	return HttpResponse("success!")

def get_set_of_pair(l):
	return set([tuple(sorted([x, y])) for x in l for y in l if x != y])

def get_list_of_pair(l):
	return [(x, y) for x in l for y in l if x != y]

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
