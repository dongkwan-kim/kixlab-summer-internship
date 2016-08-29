import wjapp.py_vote_19 as vt
import wjapp.py_lwj as lwj
import wjapp.py_cobill as cb
import firstexp.py_submit_log_analyzer as fsla
import secondexp.py_submit_log_analyzer as ssla

p_hash = fsla.create_p_hash()

def get_intersection_w_list(net1, net2):
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

def get_w_list_hash():
	fep_network = fsla.create_network_with_whole_process()
	sep_network = ssla.create_network_with_whole_process()
	v_network = vt.create_vote_network(piv_w_value=1)
	lwj_network = lwj.create_lwj_network(piv_w_value=1)
	cb_network = cb.create_cb_network(piv_w_value=1)

	w_list_hash = {}
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
		w_list_hash[c] = {}
	
	for c in col.keys():
		for r in row.keys():
			w_list_hash[c][r] = get_intersection_w_list(col[c], row[r])
	
	return w_list_hash
