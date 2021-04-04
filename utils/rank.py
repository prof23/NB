from config import *
from utlis.tg import Bot

def setrank(redis,rank,userID,chatID,type):
	try:
		if type is "array":
			get = redis.sismember("{}Nbot:{}:{}".format(BOT_ID,chatID,rank),userID)
			if get:
				return rank
			save = redis.sadd("{}Nbot:{}:{}".format(BOT_ID,chatID,rank),userID)
			
			return save
		elif type is "one":
			get = redis.get("{}Nbot:{}:{}".format(BOT_ID,chatID,rank))
			if get and int(get) == userID:
				return rank
			save = redis.set("{}Nbot:{}:{}".format(BOT_ID,chatID,rank),userID)
			
			return save
	except Exception as e:
		return rank

def remrank(redis,rank,userID,chatID,type):
	try:
		if type is "array":
			get = redis.sismember("{}Nbot:{}:{}".format(BOT_ID,chatID,rank),userID)
			if not get:
				return 0
			save = redis.srem("{}Nbot:{}:{}".format(BOT_ID,chatID,rank),userID)
			
			return save
		elif type is "one":
			get = redis.get("{}Nbot:{}:{}".format(BOT_ID,chatID,rank))
			if get and int(get) != userID:
				return 0
			save = redis.delete("{}Nbot:{}:{}".format(BOT_ID,chatID,rank),userID)
			
			return save
	except Exception as e:
		return 0
def isrank(redis,userID,chatID):
	get = redis.get("{}Nbot:BOTrank".format(BOT_ID))
	if get and int(get) == userID:
		return "bot"
	get = redis.get("{}Nbot:sudo".format(BOT_ID))
	if get and int(get) == userID:
		return "sudo"
	get = redis.sismember("{}Nbot:sudos".format(BOT_ID),userID)
	if get:
		return "sudos"
	get = redis.get("{}Nbot:{}:creator".format(BOT_ID,chatID))
	if get and int(get) == userID:
		return "creator"
	get = redis.sismember("{}Nbot:{}:owner".format(BOT_ID,chatID),userID)
	if get:
		return "owner"
	get = redis.sismember("{}Nbot:{}:admin".format(BOT_ID,chatID),userID)
	if get:
		return "admin"
	get = redis.sismember("{}Nbot:{}:vip".format(BOT_ID,chatID),userID)
	if get:
		return "vip"
	return 0

def setsudos(redis,userID):
	try:
		get = redis.sismember("{}Nbot:sudos".format(BOT_ID),userID)
		print("get",get)
		if get:
			return "sudos"
		save = redis.sadd("{}Nbot:sudos".format(BOT_ID),userID)
		
		return save
	except Exception as e:
		return 0

def remsudos(redis,userID):
	try:
		get = redis.sismember("{}Nbot:sudos".format(BOT_ID),userID)
		if not get:
			return 0
		save = redis.srem("{}Nbot:sudos".format(BOT_ID),userID)
		
		return save
	except Exception as e:
		return 0

def setsudo(redis,userID):
	try:
		save = redis.set("{}Nbot:sudo".format(BOT_ID),userID)
		
		return save
	except Exception as e:
		return 0

def GPranks(userID,chatID):
	get = Bot("getChatMember",{"chat_id":chatID,"user_id":userID})
	if get["ok"]:
		status = get["result"]["status"]
	else:
		status = "NoMember"
	return status



def IDrank(redis,userID,chatID,r):
	rank = isrank(redis,userID,chatID)
	if (rank is False or rank is 0):
		T = r.Rmember
	if rank == "sudo":
		T = r.Rsudo

	if rank == "sudos":
		T = r.Rsudos

	if rank == "creator":
		T = r.Rcreator

	if rank == "owner":
		T = r.Rowner

	if rank == "admin":
		T = r.Radmin

	if rank == "vip":
		T = r.Rvip
	if rank == "bot":
	  T = "bot"
	return T

def Grank(rank,r):
	if rank == "sudo":
		T = r.Rsudo

	if rank == "sudos":
		T = r.Rsudos

	if rank == "creator":
		T = r.Rcreator

	if rank == "owner":
		T = r.Rowner

	if rank == "admin":
		T = r.Radmin
	if rank == "administrator":
		T = r.Radmin
	if rank == "vip":
		T = r.Rvip
	if rank == "bot":
	  T = "bot"
	return T

