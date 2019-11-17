import json
import os
def processFile(fname, _type, num, cong_year):
	ret = []
	with open(fname) as json_file:
		data = json.load(json_file)
		try:
			enacted = str(data["history"]["enacted"]).upper()
		except:
			enacted = "FALSE"
		try:
			summary = data["summary"]["text"]
			summary = summary.replace("'", "''")
		except:
			summary = ""
		try:
			category = data["subjects_top_term"]
		except:
			category = ""
		intro_date = data["introduced_at"]
		ret.append(billINSERT(_type, num, cong_year, enacted, summary, category, intro_date))
		sponsors = []
		try:
			sponsors.append(data["sponsor"]["bioguide_id"])
		except:
			pass
		try:
			for d in data["cosponsors"]:
				sponsors.append(d["bioguide_id"])
		except:
			pass
		ret.extend(sponsorINSERT(_type, num, cong_year, sponsors))
		return ret


def billINSERT(_type, num, cong_year, enacted, summary, category, intro_date):
	s = "INSERT INTO Bill VALUES("
	s += "'" + _type + "', "
	s += str(num) + ", "
	s += str(cong_year) + ", "
	s += enacted + ", "
	s += "'" + summary + "', "
	s += "'" + category + "', "
	s += "'" + intro_date + "')"
	s += ";"
	return s

def sponsorINSERT(_type, num, cong_year, sponsors):
	ret = []
	for sp in sponsors:
		ret.append("INSERT INTO SponsoredBy VALUES(" + "'" + _type + "', " + str(num) + ", " + str(cong_year) + ", " + "'" + sp + "');")
	return ret


def main(fname):
	f = open(fname, 'w')
	for i in range(5000):
		try:
			for x in processFile(os.path.abspath('..')+"\\json\\bills\\116\\bills\\hr\\hr" + str(i) +"\\data.json", "hr", i, 116):
				f.write(x)
				f.write("\n")
		except:
			pass
		try:
			for y in processFile(os.path.abspath('..')+"\\json\\bills\\116\\bills\\s\\s" + str(i) +"\\data.json", "s", i, 116):
				f.write(y)
				f.write("\n")
		except:
			pass


main("load-production-bills.sql")