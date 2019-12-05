import json
import os
seen = set([])
senateToBioguide = {'S307': 'B000944', 'S275': 'C000127', 'S308': 'C000141', 'S277': 'C000174', 'S309': 'C001070', 'S221': 'F000062', 'S311': 'K000367', 'S306': 'M000639', 'S313': 'S000033', 'S284': 'S000770', 'S314': 'T000464', 'S316': 'W000802', 'S317': 'B001261', 'S318': 'W000437', 'S289': 'A000360', 'S252': 'C001035', 'S287': 'C001056', 'S253': 'D000563', 'S254': 'E000285', 'S293': 'G000359', 'S236': 'I000024', 'S174': 'M000355', 'S322': 'M001176', 'S259': 'R000122', 'S323': 'R000584', 'S260': 'R000307', 'S324': 'S001181', 'S326': 'U000039', 'S327': 'W000805', 'S331': 'G000555', 'S337': 'C001088', 'S338': 'M001183', 'S354': 'B001230', 'S330': 'B001267', 'S396': 'B001243', 'S341': 'B001277', 'S342': 'B000575', 'S343': 'B001236', 'S300': 'B001135', 'S372': 'C001047', 'S373': 'C001075', 'S266': 'C000880', 'S377': 'G000562', 'S153': 'G000386', 'S359': 'H001046', 'S361': 'H001042', 'S344': 'H001061', 'S305': 'I000055', 'S345': 'J000293', 'S378': 'L000575', 'S057': 'L000174', 'S346': 'L000577', 'S369': 'M000133', 'S347': 'M000934', 'S288': 'M001153', 'S364': 'M001169', 'S229': 'M001111', 'S348': 'P000603', 'S380': 'P000595', 'S349': 'P000449', 'S350': 'R000595', 'S270': 'S000148', 'S365': 'S001184', 'S184': 'S000320', 'S303': 'T000250', 'S351': 'T000461', 'S390': 'V000128', 'S247': 'W000779', 'S391': 'Y000064', 'S353': 'S001194', 'S374': 'C001095', 'S403': 'S001191', 'S386': 'D000622', 'S366': 'W000817', 'S363': 'K000383', 'S375': 'D000618', 'S398': 'C001096', 'S357': 'F000463', 'S355': 'C001098', 'S362': 'K000384', 'S370': 'B001288', 'S383': 'S001198', 'S379': 'P000612', 'S376': 'E000295', 'S384': 'T000476', 'S381': 'R000605', 'S382': 'S001197', 'S387': 'H001075', 'S389': 'K000393', 'S388': 'H001076', 'S385': 'C001113', 'S402': 'R000608', 'S393': 'J000300', 'S394': 'S001203', 'S395': 'H001079', 'S404': 'S001217', 'S397': 'B001310', 'S399': 'H001089', 'S401': 'R000615', 'S400': 'M001197'}

def processFile(fname):
	global seen, senateToBioguide
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
				idToUse = p['id']
				if idToUse in senateToBioguide:
					idToUse = senateToBioguide[idToUse]
				if (idToUse, _type, bill_num, 116) not in seen:
					ret.append(voteINSERT(idToUse, _type, bill_num, 116, decision))
					seen.add((idToUse, _type, bill_num, 116))
				else:
					ret.append(voteUPDATE(idToUse, _type, bill_num, 116, decision))
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

def voteUPDATE(rep_id, bill_type, bill_num, cong_year, decision):
	s = "UPDATE Vote SET "
	s += "decision = " + "'" + decision + "' "
	s += "WHERE "
	s += "rep_id = " + "'" + rep_id + "' AND "
	s += "bill_type = " + "'" + bill_type + "' AND "
	s += "bill_num = " + str(bill_num) + " AND "
	s += "cong_year = " + str(cong_year)
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
			for y in processFile(os.path.abspath('..')+"\\json\\bills\\116\\votes\\2019\\s" + str(i) +"\\data.json"):
				f.write(y)
				f.write("\n")
		except:
			pass

# processFile(os.path.abspath('..')+"\\json\\bills\\116\\votes\\2019\\h10\\data.json")
main("load-production-votes.sql")