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
import wjapp.py_stat as stat
import wjapp.py_io as io

from ast import literal_eval
# Create your views here.

exp_name = "Analysis"

def analyze(request):
    fep_network = fsla.create_visjs_with_whole_process()
    sep_network = ssla.create_visjs_with_whole_process()
    v_network = vt.create_visjs_vote_network()
    lwj_network = lwj.create_visjs_lwj_network()
    cb_network = cb.create_visjs_cb_network()

    fep_slog_list = fem.SubmitLog.objects.all()
    sep_slog_list = sem.SubmitLog.objects.all()

    fep_user_set = set([u.token for u in fep_slog_list])
    sep_user_set = set([u.token for u in sep_slog_list])

    w_hash = stat.get_w_list_hash()
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
        "cb_nodes": cb_network[0],
        "cb_edges": cb_network[1],
        "fep_n_person": len(fep_user_set),
        "sep_n_person": len(sep_user_set),
        "fep_n_submit": len(fep_slog_list),
        "sep_n_submit": len(sep_slog_list),
        "w_uni_hash": w_hash[0],
        "exp_name": exp_name
    })


def ref_visualize(request, name):
    if name == "vote":
        v_network = vt.create_visjs_vote_network()
        return render(request, "wjapp/resultvis.html", {"nodes": v_network[0], "edges": v_network[1], "exp_name": "Network of 19th Assembly Vote Result"})

    elif name == "lwj":
        lwj_network = lwj.create_visjs_lwj_network()
        return render(request, "wjapp/resultvis.html", {"nodes": lwj_network[0], "edges": lwj_network[1], "exp_name": "Network of 20th Assembly's features (By Prof Lee)"})

    elif name == "cobill":
        cb_network = cb.create_visjs_cb_network()
        return render(request, "wjapp/resultvis.html", {"nodes": cb_network[0], "edges": cb_network[1], "exp_name": "Network of 20th Assembly Cosponsorship"})


def export_all_db(request, ref):
    return io.export_all_db(request, ref)

def reg_network(request, network):
    return io.reg_network(request, network)

def reg_db(request, db):
    return io.reg_db(request, db)
