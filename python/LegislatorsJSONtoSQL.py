import json
import os
def main(filename, filename2):
	d = {}
	f = open(filename2, 'w')
	with open(filename) as json_file:
		data = json.load(json_file)
		for p in data:
			_id = p["id"]["bioguide"]
			if "lis" in p["id"]:
				senateID = p["id"]["lis"]
				d[senateID] = _id
			name = p["name"]["official_full"]
			currterm = p["terms"][-1]
			_type = currterm["type"]
			state = currterm["state"]
			if _type == "rep":
				district = currterm["district"]
			else:
				district = None
			party = currterm["party"]
			phone = currterm["phone"]
			address = currterm["address"]
			try:
				contact_form = currterm["contact_form"]
			except:
				contact_form = None

			f.write(toSQLInsert(_id, name, _type, state, district, party, phone, address, contact_form))
		print(d)

def toSQLInsert(_id, name, _type, state, district, party, phone, address, contact_form):
	s = "INSERT INTO Congressman VALUES("
	s += "'" + _id + "', "
	s += "'" + name + "', " 
	s += "'" + _type + "', "
	s += "'" + state + "', "
	if district is not None:
		s += str(district) + ", "
	else:
		s += "NULL, "
	s += "'" + party + "', "
	s += "'" + phone + "', "
	s += "'" + address + "', "
	if contact_form is not None:
		s += "'" + contact_form + "'"
	else:
		s += "NULL"
	s += ");\n"
	return s
	


main(os.path.abspath('..')+"\\json\\congresspeople\\legislators-current.json", "load-production-congresspeople.sql")