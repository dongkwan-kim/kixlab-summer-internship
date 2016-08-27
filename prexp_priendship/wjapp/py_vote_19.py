import urllib.request
import urllib.parse
import json
from wjapp.models import Vote19, VoteVector
import firstexp.models as fem
import math

def int_vectorize():
	vote_db = Vote19.objects.all()
	my_p_list = fem.Politician.objects.all()

	for vote in vote_db:
		for p in my_p_list:
			# only intersection of mine and 19's
			if vote.name == p.name:
				v_list = vote.vote.split(",")
				vectorized_list = []
				for v_word in v_list:
					if v_word == "찬성":
						vectorized_list.append("1")
					elif v_word == "반대":
						vectorized_list.append("-1")
					else:
						# abstention, absence, etc.
						vectorized_list.append("0")
				new_vv = VoteVector(name=vote.name, party=vote.party, vote=",".join(vectorized_list))
				new_vv.save()

def get_eud(vv1, vv2):
	"""
	:param vv1, vv2: VoteVector.vote 1,0,-1,1, ... ,
	:return: Euclidean distance of vv1 and vv2
	"""
	vv1_list = [int(v) for v in vv1.split(",")]
	vv2_list = [int(v) for v in vv2.split(",")]

	if len(vv1_list) != len(vv2_list):
		raise(Exception("VectorLengthDifferentError"))

	eud = math.sqrt(sum([(e1 - e2)**2 for (e1, e2) in zip(vv1_list, vv2_list)]))
	return eud


# max num = 293
def crawl(num):
	vote_db = Vote19.objects.all()
	
	# start from previous index
	for num in range(len(vote_db)+1, num):
		base_url = "http://read-data.codenamu.org/congress-report/api/congress_people/"
		base_url += str(num) + ".json"
		request = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
		response = urllib.request.urlopen(request)
		js = json.loads(response.read().decode("utf-8"))

		name = js["congress_person"]["name_kr"]
		party = js["congress_person"]["party"]
		vote_list = js["congress_person"]["bill_votes"]
		vote_hash = {}
		for vote in vote_list:
			vote_hash[vote["bill_id"]] = vote["vote"]

		new_vote_list = []
		for i in range(1, 2571):
			try:
				new_vote_list.append(vote_hash[i])
			except:
				new_vote_list.append("없음")
	
		vote_line = ",".join(new_vote_list)
		new_model = Vote19(name=name, party=party, vote=vote_line)
		new_model.save()
