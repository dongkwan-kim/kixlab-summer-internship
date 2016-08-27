def crawl(num):
	
	'''
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
	'''
