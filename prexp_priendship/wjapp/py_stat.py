import wjapp.py_vote_19 as vt
import wjapp.py_lwj as lwj
import wjapp.py_cobill as cb
import firstexp.py_submit_log_analyzer as fsla
import secondexp.py_submit_log_analyzer as ssla

p_hash = fsla.create_p_hash()

def get_intersection_w_uni_list(net1, net2):
	ip_list = []
	for pair in net1.keys():
		if pair in net2.keys():
			ip_list.append(pair)
	
	wl_1 = []
	wl_2 = []
	pl = []
	for pair in ip_list:
		w_1 = net1[pair]
		w_2 = net2[pair]
		if w_1 != 0 and w_2 != 0:
			wl_1.append(w_1)
			wl_2.append(w_2)
			pl.append(sorted([p_hash[pid] for pid in pair]))
	return [wl_1, wl_2, pl]

def get_intersection_w_multi_list(net_list):
	ip_list = []
	for pair in net_list[0].keys():
		is_inter = True
		for net in net_list[1:]:
			if pair not in net.keys():
				is_inter = False
				break
		if is_inter == True:
			ip_list.append(pair)

	wll = []
	for idx in range(len(net_list)):
		wll.append([])
	pl = []
	for pair in ip_list:
		w_list = [net[pair] for net in net_list]
		all_nzero = True
		for w in w_list:
			if w == 0:
				all_nzero = False
				break
		if all_nzero == True:
			for idx in range(len(w_list)):
				wll[idx].append(w_list[idx])
			pl.append(sorted([p_hash[pid] for pid in pair]))
	return wll+[pl]

def get_w_list_hash():
	fep_network = fsla.create_network_with_whole_process()
	sep_network = ssla.create_network_with_whole_process()
	v_network = vt.create_vote_network(piv_w_value=1)
	lwj_network = lwj.create_lwj_network(piv_w_value=1)
	cb_network = cb.create_cb_network(piv_w_value=1)

	w_uni_hash = {}
	w_multi_hash = {}
	col = {
		"fep": fep_network,
		"sep": sep_network,
	}
	row = {
		"v": v_network,
		"lwj": lwj_network,
		"cb": cb_network,
	}
	
	for c in col.keys():
		w_uni_hash[c] = {}

		w_multi_hash[c] = {}
		for r in row.keys():
			w_multi_hash[c][r] = {}

	for c in col.keys():
		for r in row.keys():
			w_uni_hash[c][r] = get_intersection_w_uni_list(col[c], row[r])

			for dr in row.keys():
				if dr != r:
					w_multi_hash[c][r][dr] = get_intersection_w_multi_list([col[c], row[r], row[dr]])
	return [w_uni_hash, w_multi_hash]
