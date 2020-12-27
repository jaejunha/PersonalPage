import datetime

TIME_VISIT = 240

CONST_ID = 0
CONST_PWD = 1

def getAccount(list_account):
	try:
		file = open("config/password.csv", "r")
		for line in file.readlines():
			list_ele = line.split(",")
			list_account.append( (list_ele[CONST_ID].strip(), list_ele[CONST_PWD].strip()) )

		return True

	except FileNotFoundError:
		print("관리자 계정을 만드세요!")
		return False

def checkAccount(res, list_account):
	ret = False

	length = int(res.headers['Content-length'])
	raw_input = res.rfile.read(length).decode("utf-8") 
	list_input = raw_input.split("&")

	for account in list_account:
		if account[CONST_ID] == list_input[CONST_ID].split("=")[1] and account[CONST_PWD] == list_input[CONST_PWD].split("=")[1]:
			ret = True
			break
				
	return ret

def checkVisit(dic_visit, ip):
	if (ip in dic_visit) is False:
		return False

	now = datetime.datetime.now()
	return now < dic_visit[ip]

def calSessionLength():
	now = datetime.datetime.now()
	return now + datetime.timedelta(minutes = TIME_VISIT)
