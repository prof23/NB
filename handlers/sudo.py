from utlis.rank import setrank,isrank,remrank,remsudos,setsudo,GPranks
from utlis.send import send_msg, BYusers,sendM,GetLink,Glang
from utlis.tg import Bot,Ckuser
from config import *
#b
from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json,datetime,os
import importlib

from utlis.send import run

from os import listdir
from os.path import isfile, join
def setsudos(redis,userID):
	try:
		get = redis.sismember("{}Nbot:sudos".format(BOT_ID),userID)
		if get:
			return "sudos"
		save = redis.sadd("{}Nbot:sudos".format(BOT_ID),userID)
		
		return save
	except Exception as e:
		return "sudos"


def sudo(client, message,redis):
	type = message.chat.type
	userID = message.from_user.id
	chatID = message.chat.id
	rank = isrank(redis,userID,chatID)
	text = message.text
	title = message.chat.title
	userFN = message.from_user.first_name
	type = message.chat.type
	lang = Glang(redis,chatID)
	moduleCMD = "lang."+lang+"-cmd"
	moduleREPLY = "lang."+lang+"-reply"
	c = importlib.import_module(moduleCMD)
	r = importlib.import_module(moduleREPLY)
	if redis.hexists("{}Nbot:stepSUDO".format(BOT_ID),userID):
		tx = redis.hget("{}Nbot:stepSUDO".format(BOT_ID),userID)
		if text :
			redis.hset("{}Nbot:TXreplys".format(BOT_ID),tx,text)
			redis.hdel("{}Nbot:stepSUDO".format(BOT_ID),userID)
			Bot("sendMessage",{"chat_id":chatID,"text":r.SRtext.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
		
		if message.sticker:
			ID = message.sticker.file_id
			redis.hset("{}Nbot:STreplys".format(BOT_ID),tx,ID)
			redis.hdel("{}Nbot:stepSUDO".format(BOT_ID),userID)
			Bot("sendMessage",{"chat_id":chatID,"text":r.SRst.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if message.animation:
			ID = message.animation.file_id
			redis.hset("{}Nbot:GFreplys".format(BOT_ID),tx,ID)
			redis.hdel("{}Nbot:stepSUDO".format(BOT_ID),userID)
			Bot("sendMessage",{"chat_id":chatID,"text":r.SRgf.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if message.voice:
			ID = message.voice.file_id
			redis.hset("{}Nbot:VOreplys".format(BOT_ID),tx,ID)
			redis.hdel("{}Nbot:stepSUDO".format(BOT_ID),userID)
			Bot("sendMessage",{"chat_id":chatID,"text":r.SRvo.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if message.photo:
			ID = message.photo.file_id
			redis.hset("{}Nbot:PHreplys".format(BOT_ID),tx,ID)
			redis.hdel("{}Nbot:stepSUDO".format(BOT_ID),userID)
			Bot("sendMessage",{"chat_id":chatID,"text":r.SRph.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
		if message.document:
			ID = message.document.file_id
			redis.hset("{}Nbot:DOreplys".format(BOT_ID),tx,ID)
			redis.hdel("{}Nbot:stepSUDO".format(BOT_ID),userID)
			Bot("sendMessage",{"chat_id":chatID,"text":r.SRfi.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})



	if text and (type is "supergroup" or type is "group"):
		if re.search(c.leaveChatS, text):
			Bot("leaveChat",{"chat_id":chatID})
			redis.srem("{}Nbot:groups".format(BOT_ID),chatID)
			redis.sadd("{}Nbot:disabledgroups".format(BOT_ID),chatID)
			NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
			redis.hset("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID,str(NextDay_Date))

		if re.search(c.creators, text) and Ckuser(message):
			text = text.replace("مسح ","")
			arrays = redis.get("{}Nbot:{}:creator".format(BOT_ID,chatID))
			if arrays:
				print(arrays)
				b = BYusers({arrays},chatID,redis,client)
				kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delList","creator",userID]))]])
				if	b is not "":
					Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
				else:
					Bot("sendMessage",{"chat_id":chatID,"text":r.creatorempty,"reply_to_message_id":message.message_id,"parse_mode":"markdown"})
			else:
				Bot("sendMessage",{"chat_id":chatID,"text":r.creatorempty,"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

		if re.search(c.setcreator, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.setcreator2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = setrank(redis,"creator",userId,chatID,"one")
				if setcr is "creator":
					send_msg("UD",client, message,r.DsetRK,"",getUser,redis)
				elif (setcr is True or setcr is 1):
					send_msg("UD",client, message,r.setRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if re.search(c.remcreator, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.remcreator2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = remrank(redis,"creator",userId,chatID,"one")
				if setcr:
					send_msg("UD",client, message,r.remRK,"",getUser,redis)
				elif not setcr:
					send_msg("UD",client, message,r.DremRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})


	if text and (type is "private" or (type is "supergroup" or type is "group")) :
		if re.search(c.STreplyBOT, text):
			tx = text.replace(c.RPreplyBOT,"")
			if redis.hexists("{}Nbot:TXreplys".format(BOT_ID,chatID),tx):
				Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			elif redis.hexists("{}Nbot:STreplys".format(BOT_ID,chatID),tx):
				Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			elif redis.hexists("{}Nbot:GFreplys".format(BOT_ID,chatID),tx):
				Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			elif redis.hexists("{}Nbot:VOreplys".format(BOT_ID,chatID),tx):
				Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			else:
				redis.hset("{}Nbot:stepSUDO".format(BOT_ID),userID,tx)
				kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.MoreInfo, url="t.me/UpdatesAstro")]])
				Bot("sendMessage",{"chat_id":chatID,"text":r.Sendreply % tx,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})
			


		if re.search(c.DLreplyBOT, text):
			tx = text.replace(c.RPdreplyBOT,"")
			if redis.hexists("{}Nbot:TXreplys".format(BOT_ID,chatID),tx):
				redis.hdel("{}Nbot:TXreplys".format(BOT_ID,chatID),tx)
				Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			elif redis.hexists("{}Nbot:STreplys".format(BOT_ID,chatID),tx):
				redis.hdel("{}Nbot:STreplys".format(BOT_ID,chatID),tx)
				Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			elif redis.hexists("{}Nbot:GFreplys".format(BOT_ID,chatID),tx):
				redis.hdel("{}Nbot:GFreplys".format(BOT_ID,chatID),tx)
				Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			elif redis.hexists("{}Nbot:VOreplys".format(BOT_ID,chatID),tx):
				redis.hdel("{}Nbot:GFreplys".format(BOT_ID,chatID),tx)
				Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
			else:
				Bot("sendMessage",{"chat_id":chatID,"text":r.Norp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if re.search(c.ReplylistBOT, text):
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STword,callback_data=json.dumps(["showreplylistBOT","",userID])),InlineKeyboardButton(c.STgifs,callback_data=json.dumps(["showGFreplylistBOT","",userID])),],[InlineKeyboardButton(c.STvoice,callback_data=json.dumps(["showVOreplylistBOT","",userID])),InlineKeyboardButton(c.STsticker,callback_data=json.dumps(["showSTreplylistBOT","",userID])),]])
			Bot("sendMessage",{"chat_id":chatID,"text":r.blocklist.format(text,title),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":reply_markup})



		if rank is "sudo":
			if text == c.remfiles:
				onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
				array = []
				if not onlyfiles:
					Bot("sendMessage",{"chat_id":chatID,"text":r.NOaddfiles2,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
					return False
				for f in onlyfiles:
					array.append([InlineKeyboardButton(f,callback_data=json.dumps(["delF",f,userID]))])
				array.append([InlineKeyboardButton(c.remallfiles,callback_data=json.dumps(["delFa","",userID]))])
				kb = InlineKeyboardMarkup(array)
				Bot("sendMessage",{"chat_id":chatID,"text":r.dlFiles,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":kb})


			if text == c.files:
				onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
				filesR = redis.smembers("{}Nbot:botfiles".format(BOT_ID))
				array = []
				print(onlyfiles)
				if not onlyfiles:
					Bot("sendMessage",{"chat_id":chatID,"text":r.NOaddfiles2,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
					return False
				for f in onlyfiles:
					if f in filesR:
						s = r.true
					else:
						s = r.false
					array.append([InlineKeyboardButton(f+" "+s,callback_data=json.dumps(["au",f,userID]))])
				kb = InlineKeyboardMarkup(array)
				Bot("sendMessage",{"chat_id":chatID,"text":r.Files,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":kb})

			if text == c.ADDfiles:
				url = "https://raw.githubusercontent.com/prof23/files/master/files"
				req = requests.get(url).text
				if not re.search(".py",req):
					Bot("sendMessage",{"chat_id":chatID,"text":r.NOaddfiles,"reply_to_message_id":message.message_id,"disable_web_page_preview":True,"parse_mode":"html"})
					return False

				files = req.split("\n")
				array = []
				for f in files:
					array.append([InlineKeyboardButton(f,callback_data=json.dumps(["dlf",f,userID]))])
				kb = InlineKeyboardMarkup(array)
				Bot("sendMessage",{"chat_id":chatID,"text":r.addFiles,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":kb})


			if text == c.Ubot:
				Files_H = ["inline.py","all.py","callback.py","delete.py","edit.py","gpcmd.py","locks.py","msg.py","nf.py","ranks.py","sudo.py"]
				#Files_H = ["gpcmd.py"]
				Files_U = ["tg.py","locks.py","rank.py","send.py"]
				Files_B = ["bot.py","setup.py"]
				for fnh in Files_H:
					url = "https://raw.githubusercontent.com/prof23/NB/master/handlers/"+fnh
					out = requests.get(url).text
					f = open("./handlers/"+fnh,"w+")
					f.write(out)
					f.close()
				for fnu in Files_U:
					url = "https://raw.githubusercontent.com/prof23/NB/master/utlis/"+fnu
					out = requests.get(url).text
					f = open("./utlis/"+fnu,"w+")
					f.write(out)
					f.close()
				for fnb in Files_B:
					url = "https://raw.githubusercontent.com/prof23/NB/master/"+fnb
					out = requests.get(url).text
					f = open("./"+fnb,"w+")
					f.write(out)
					f.close()
				Bot("sendMessage",{"chat_id":chatID,"text":r.Wres,"reply_to_message_id":message.message_id,"parse_mode":"html"})
				run(redis,chatID)
				

			if text == c.Ulang:
				t = r.Dulang
				t2 = r.Wres
				os.system("rm -rf lang;git clone https://github.com/prof23/Lang.git;sudo cp -R Lang/lang lang/; rm -rf Lang")
				Bot("sendMessage",{"chat_id":chatID,"text":t,"reply_to_message_id":message.message_id,"parse_mode":"html"})
				Bot("sendMessage",{"chat_id":chatID,"text":t2,"reply_to_message_id":message.message_id,"parse_mode":"html"})
				run(redis,chatID)
			if re.search(c.setSudoC, text):
				tx = text.replace(c.RsetSudoC,"")
				v = Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html"})
				if v["ok"]:
					redis.set("{}Nbot:SHOWsudos".format(BOT_ID),tx)
					Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShow,"reply_to_message_id":message.message_id,"parse_mode":"html"})
				elif v["ok"] == False:
					Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.message_id,"parse_mode":"html"})

			if re.search(c.sudosList, text) and Ckuser(message):
				text = text.replace("مسح ","")
				arrays = redis.smembers("{}Nbot:sudos".format(BOT_ID,chatID))
				b = BYusers(arrays,chatID,redis,client)
				kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delList","sudos",userID]))]])
				if	b is not "":
					Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
				else:
					Bot("sendMessage",{"chat_id":chatID,"text":r.listempty.format(text),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

			if re.search(c.setsudos, text) and Ckuser(message):
				if re.search("@",text):
					user = text.split("@")[1]
				if re.search(c.setsudos2,text):
					user = text.split(" ")[2]
				if message.reply_to_message:
					user = message.reply_to_message.from_user.id
				if 'user' not in locals():return False
				try:
					getUser = client.get_users(user)
					userId = getUser.id
					userFn = getUser.first_name
					setcr = setsudos(redis,userId)
					if setcr is "sudos":
						send_msg("UD",client, message,r.DsetRK,"",getUser,redis)
					elif (setcr is True or setcr is 1):
						send_msg("UD",client, message,r.setRK,"",getUser,redis)
				except Exception as e:
					print(e)
					Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

			if re.search(c.remsudos, text) and Ckuser(message):
				if re.search("@",text):
					user = text.split("@")[1]
				if re.search(c.remsudos2,text):
					user = text.split(" ")[2]
				if message.reply_to_message:
					user = message.reply_to_message.from_user.id
				if 'user' not in locals():return False
				try:
					getUser = client.get_users(user)
					userId = getUser.id
					userFn = getUser.first_name
					setcr = remsudos(redis,userId)
					if setcr:
						send_msg("UD",client, message,r.remRK,"",getUser,redis)
					elif not setcr:
						send_msg("UD",client, message,r.DremRK,"",getUser,redis)
				except Exception as e:
					Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
			
			if re.search(c.banall, text):
				if re.search("@",text):
					user = text.split("@")[1]
				if re.search(c.ban2all,text):
					user = text.split(" ")[2]
				if message.reply_to_message:
					user = message.reply_to_message.from_user.id
				if 'user' not in locals():return False
				try:
					getUser = client.get_users(user)
					userId = getUser.id
					userFn = getUser.first_name
					BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
					Getrank = isrank(redis,userId,chatID)
					GetGprank = GPranks(userId,chatID)
					if Getrank == "bot":return False
					if Getrank == "sudos" or Getrank == "sudo":
						Bot("sendMessage",{"chat_id":chatID,"text":r.cTsudo,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						return False
					if redis.sismember("{}Nbot:bans".format(BOT_ID),userId):
						Bot("sendMessage",{"chat_id":chatID,"text":r.Dbanall.format(BY),"reply_to_message_id":message.message_id,"parse_mode":"html"})
					else:
						redis.sadd("{}Nbot:bans".format(BOT_ID),userId)
						Bot("sendMessage",{"chat_id":chatID,"text":r.banall.format(BY),"reply_to_message_id":message.message_id,"parse_mode":"html"})
						if (GetGprank == "member" or GetGprank == "restricted"):
							Bot("kickChatMember",{"chat_id":chatID,"user_id":userId})
				except Exception as e:
					print(e)
					Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

			if re.search(c.unbanall, text):
				if re.search("@",text):
					user = text.split("@")[1]
				if re.search(c.unban2all,text):
					user = text.split(" ")[2]
				if message.reply_to_message:
					user = message.reply_to_message.from_user.id
				if 'user' not in locals():return False
				try:
					getUser = client.get_users(user)
					userId = getUser.id
					userFn = getUser.first_name
					Getrank = isrank(redis,userId,chatID)
					GetGprank = GPranks(userId,chatID)
					if Getrank == "bot":return False
					if redis.sismember("{}Nbot:bans".format(BOT_ID),userId):
						redis.srem("{}Nbot:bans".format(BOT_ID),userId)
						send_msg("BNN",client, message,r.unbanall,"bans",getUser,redis)
					else:
						send_msg("BNN",client, message,r.Dunbanall,"bans",getUser,redis)
				except Exception as e:
					print(e)
					Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

			if re.search(c.TKall, text):
				if re.search("@",text):
					user = text.split("@")[1]
				if re.search(c.TK2all,text):
					user = text.split(" ")[2]
				if message.reply_to_message:
					user = message.reply_to_message.from_user.id
				if 'user' not in locals():return False
				try:
					getUser = client.get_users(user)
					userId = getUser.id
					userFn = getUser.first_name
					Getrank = isrank(redis,userId,chatID)
					GetGprank = GPranks(userId,chatID)
					if Getrank == "bot":return False
					if Getrank == "sudos" or Getrank == "sudo":
						Bot("sendMessage",{"chat_id":chatID,"text":r.cTsudo,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						return False
					if redis.sismember("{}Nbot:restricteds".format(BOT_ID),userId):
						send_msg("BNN",client, message,r.Drestrictedall,"restricteds",getUser,redis)
					else:
						send_msg("BNN",client, message,r.restrictedall,"restricteds",getUser,redis)
						redis.sadd("{}Nbot:restricteds".format(BOT_ID),userId)
						if (GetGprank == "member"):
							Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,
						    "can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,"can_invite_users": 0,})
				except Exception as e:
					print(e)
					Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

			if re.search(c.unTKall, text):
				if re.search("@",text):
					user = text.split("@")[1]
				if re.search(c.unTK2all,text):
					user = text.split(" ")[2]
				if message.reply_to_message:
					user = message.reply_to_message.from_user.id
				if 'user' not in locals():return False
				try:
					getUser = client.get_users(user)
					userId = getUser.id
					userFn = getUser.first_name
					Getrank = isrank(redis,userId,chatID)
					GetGprank = GPranks(userId,chatID)
					if Getrank == "bot":return False
					if redis.sismember("{}Nbot:restricteds".format(BOT_ID),userId):
						send_msg("BNN",client, message,r.unrestrictedall,"restricteds",getUser,redis)
						redis.srem("{}Nbot:restricteds".format(BOT_ID),userId)
					else:
						send_msg("BNN",client, message,r.Dunrestrictedall,"restricteds",getUser,redis)
				except Exception as e:
					print(e)
					Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

			if re.search(c.Alllist, text) and Ckuser(message):
				reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STbanall,callback_data=json.dumps(["showbanall","",userID])),InlineKeyboardButton(c.STtkall,callback_data=json.dumps(["showtkall","",userID])),]])
				Bot("sendMessage",{"chat_id":chatID,"text":r.banlist,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":reply_markup})
			
			
			if re.search(c.stats, text) and Ckuser(message):
				pr = redis.scard("{}Nbot:privates".format(BOT_ID))
				gp = redis.scard("{}Nbot:groups".format(BOT_ID))
				kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.CKgps,callback_data=json.dumps(["ckGPs","",userID]))]])
				Bot("sendMessage",{"chat_id":chatID,"text":r.showstats.format(gp,pr),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})
			
			if re.search(c.fwdall, text) and message.reply_to_message:
				Bot("forwardMessage",{"chat_id":chatID,"from_chat_id":chatID,"message_id":message.reply_to_message.message_id})
				reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["fwdtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["fwdtoprivates","",userID])),]])
				Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})

			if re.search(c.showGPS, text) and Ckuser(message):
				IDS = redis.smembers("{}Nbot:groups".format(BOT_ID))
				GPslist = ""
				i = 1
				for ID in IDS:
					get = Bot("getChat",{"chat_id":ID})
					if get["ok"]:
						Title = (get["result"]["title"] or "None")
						Link = (redis.hget("{}Nbot:links".format(BOT_ID),ID) or GetLink(ID) or "none")
						name = "[{}]({})".format(Title,Link)
						N = r.ShowGPN.format(i,name,ID)
						GPslist = GPslist+"\n\n"+N
						i +=1
				sendM("NO",GPslist,message)
			
			if text == c.Laudo :
				R = text.split(" ")[1]
				get = redis.get("{}Nbot:autoaddbot".format(BOT_ID))
				BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
				if get :
					Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
				else:
					save = redis.set("{}Nbot:autoaddbot".format(BOT_ID),1)
					Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

			if text == c.Uauto :
				R = text.split(" ")[1]
				BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
				get = redis.get("{}Nbot:autoaddbot".format(BOT_ID),chatID)
				if get :
					save = redis.delete("{}Nbot:autoaddbot".format(BOT_ID))
					Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
				else:
					Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
			if re.search(c.Setauto, text):
				N = text.split(" ")[2]
				redis.set("{}Nbot:autoaddbotN".format(BOT_ID),int(N))
				Bot("sendMessage",{"chat_id":chatID,"text":r.SetAuto.format(N),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
			if re.search(c.leaveChat,text):
				ch = text.split(" ")[1]
				Bot("leaveChat",{"chat_id":ch})
				redis.srem("{}Nbot:groups".format(BOT_ID),ch)
				redis.sadd("{}Nbot:disabledgroups".format(BOT_ID),ch)
				NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
				redis.hset("{}Nbot:disabledgroupsTIME".format(BOT_ID),ch,str(NextDay_Date))
				Bot("sendMessage",{"chat_id":chatID,"text":r.DoneleaveChat,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})




			if re.search(c.sendall, text) and message.reply_to_message and Ckuser(message):
				if message.reply_to_message.text:
					v = Bot("sendMessage",{"chat_id":chatID,"text":message.reply_to_message.text,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

				if message.reply_to_message.photo:
					ID = message.reply_to_message.photo.file_id
					CP = message.reply_to_message.caption
					v = Bot("sendphoto",{"chat_id":chatID,"photo":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

				if message.reply_to_message.voice:
					ID = message.reply_to_message.voice.file_id
					CP = message.reply_to_message.caption
					v = Bot("sendvoice",{"chat_id":chatID,"voice":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

				if message.reply_to_message.audio:
					ID = message.reply_to_message.audio.file_id
					CP = message.reply_to_message.caption
					v = Bot("sendaudio",{"chat_id":chatID,"audio":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

				if message.reply_to_message.document:
					ID = message.reply_to_message.document.file_id
					CP = message.reply_to_message.caption
					v = Bot("senddocument",{"chat_id":chatID,"document":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})



				if message.reply_to_message.sticker:
					ID = message.reply_to_message.sticker.file_id
					CP = message.reply_to_message.caption
					v = Bot("sendsticker",{"chat_id":chatID,"sticker":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

				if message.reply_to_message.animation:
					ID = message.reply_to_message.animation.file_id
					CP = message.reply_to_message.caption
					v = Bot("sendanimation",{"chat_id":chatID,"animation":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

				if message.reply_to_message.video:
					ID = message.reply_to_message.video.file_id
					CP = message.reply_to_message.caption
					v = Bot("sendvideo",{"chat_id":chatID,"video":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

				if message.reply_to_message.video_note:
					ID = message.reply_to_message.video_note.file_id
					CP = message.reply_to_message.caption
					v = Bot("sendVideoNote",{"chat_id":chatID,"video_note":ID,"caption":CP,"reply_to_message_id":message.message_id,"parse_mode":"html"})
					if v["ok"]:
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STgroup,callback_data=json.dumps(["sendtogroups","",userID])),InlineKeyboardButton(c.STprivates,callback_data=json.dumps(["sendtoprivates","",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.sendto,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					elif v["ok"] == False:
						Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

