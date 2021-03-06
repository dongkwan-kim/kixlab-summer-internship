from django.shortcuts import render
from django.http import HttpResponse
from firstexp.models import Politician, SubmitLog
from random import randrange
import firstexp.py_submit_log_analyzer as sla

# Create your views here.
exp_name = "1st prototype"

class Question():
    def __init__(self, content, color):
        self.content = content
        self.color = color

q_list = [Question("친하", "green"), Question("안 친하", "red")]

def reg_db(request):
    for p in Politician.objects.all():
        p.delete()
    for line in open("utf8_mod_unified_assembly_49.txt", "r"):
        ll = line.split("\t")
        _name = ll[0]
        _photo = ll[7]
        _pid = int(ll[7].split("/")[-1].split(".jpg")[0])
        new_p = Politician(name=_name, photo=_photo, pid=_pid)
        new_p.save()
    return HttpResponse("success!")

def export_logs(request):
    out_file = open("submit_logs.txt", "w")
    q_kind_dict = dict([(x.content, x.color) for x in q_list])
    for sl in SubmitLog.objects.all():
        line = "\t".join([sl.token,
                        q_kind_dict[sl.q_kind],
                        sl.shown_list,
                        sl.select_list
                        ])
        out_file.write(line+"\r\n")
    out_file.close()
    return HttpResponse("success!")

def visualize(request):
    visjs_network = sla.create_visjs_with_whole_process()
    return render(request, "firstexp/resultvis.html", {"nodes": visjs_network[0], "edges": visjs_network[1], "exp_name": exp_name})

def front(request):
    return _front(request)

def deploy_front(request):
    return _front(request, "deploy/")

def _front(request, odir=""):
    return render(request, odir+"firstexp/front.html", {"exp_name": exp_name})

def start(request):
    return _start(request)

def deploy_start(request):
    return _start(request, "deploy/")

def _start(request, odir=""):
    # how many did a user solve
    num_of_sol = 0

    if request.method == "POST":
        # log save
        _token = request.POST["csrfmiddlewaretoken"]
        _q_kind = request.POST["q_kind"]
        _shown_list = request.POST["shown_p"]
        _select_list = request.POST["select_p"]
        new_log = SubmitLog(token=_token, q_kind=_q_kind, shown_list=_shown_list, select_list=_select_list)
        new_log.save()
        # num_of_sol update
        log_list = SubmitLog.objects.filter(token=_token)
        num_of_sol = len(log_list)

    # random sort
    p_list = Politician.objects.all().order_by("?")
    return render(request, odir+"firstexp/start.html", {"rp_list": p_list[:6], "q_kind": q_list[randrange(0, 2)], "nos": num_of_sol, "exp_name": exp_name})
