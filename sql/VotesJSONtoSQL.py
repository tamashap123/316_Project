import json
import os
def processFile(fname):
	ret = []
	with open(fname) as json_file:
		data = json.load(json_file)
		try:
			bill = data["bill"]
		except:
			return []
		try:
			am = data["amendment"]
			return []
		except:
			pass
		_type = bill["type"]
		if _type not in ["hr", "s"]:
			return []
		bill_num = bill["number"]
		for x in data["votes"]:
			if x not in ["Yea", "Aye", "Nay"]:
				decision = "Abstain"
			else:
				if x in ["Yea", "Aye"]:
					decision = "Yea"
				else:
					decision = x
			for p in data["votes"][x]:
				ret.append(voteINSERT(p['id'], _type, bill_num, 116, decision))
		return ret

		
def voteINSERT(rep_id, bill_type, bill_num, cong_year, decision):
	s = "INSERT INTO Vote VALUES("
	s += "'" + rep_id + "', "
	s += "'" + bill_type + "', "
	s += str(bill_num) + ", "
	s += str(cong_year) + ", "
	s += "'" + decision + "')"
	s += ";"
	return s


def main(fname):
	f = open(fname, 'w')
	for i in range(1000):
		try:
			for x in processFile(os.path.abspath('..')+"\\json\\bills\\116\\votes\\2019\\h" + str(i) +"\\data.json"):
				f.write(x)
				f.write("\n")
		except:
			pass
		try:
			for y in processFile(os.path.abspath('..')+"\\json\\bills\\116\\votes\\2019\\h" + str(i) +"\\data.json"):
				f.write(y)
				f.write("\n")
		except:
			pass

# processFile(os.path.abspath('..')+"\\json\\bills\\116\\votes\\2019\\h10\\data.json")
main("load-production-votes.sql")