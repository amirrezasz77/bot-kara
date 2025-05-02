# coding: utf8
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InputMediaPhoto, \
InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputMediaVideo, \
InlineKeyboardMarkup as iMarkup, InlineKeyboardButton as iButtun, InlineQueryResultPhoto
from aiogram.dispatcher.webhook import AnswerCallbackQuery, get_new_configured_app
import telethon.errors.rpcerrorlist as telethonErrors
from acrcloud.recognizer import ACRCloudRecognizer
from aiogram.dispatcher import Dispatcher
from telethon.sync import TelegramClient
import aiogram.utils.exceptions as expts
from aiogram import Bot, executor, types
from termcolor import colored, cprint
from aiofile import AIOFile, Writer
from teleredis import RedisSession
from datetime import datetime
# from deezloader import Login
import urllib.request as ur
from pprint import pprint
from config_bot import *
from aiohttp import web
from time import time
# import nest_asyncio
import instaloader
import coloredlogs
# import soundcloud
import yt_dlp
import subprocess
import requests
import urllib3
import asyncio
import logging
import random
import redis
import json
import ssl
import re
import os
stroge = redis.Redis(host = 'localhost', port = 6379, db = 2, decode_responses = False, encoding = 'utf-8')
session = RedisSession(db, stroge)
client = TelegramClient(
session, 
api_id = telegram_datas['api_id'], 
api_hash = telegram_datas['api_hash'], 
device_model = telegram_datas['device_model'], 
system_version = telegram_datas['system_version'], 
app_version = telegram_datas['app_version']
)
client.session.save_entities = False
acr = ACRCloudRecognizer(acr_datas)
redis = redis.Redis(host = 'localhost', port = 6379, db = 2, decode_responses = True, encoding = 'utf-8')
# sc = soundcloud.Client(client_id = soundCloudKey)#, client_secret = soundCloudSec)

# dloader = Login(deezer_token)
igloader = instaloader.Instaloader(
dirname_pattern = "Instagram",
filename_pattern = "{shortcode}",
download_comments = False,
post_metadata_txt_pattern = "",
save_metadata  = False,
download_video_thumbnails = True,
)
# igloader.login(instagram_datas['username'], instagram_datas['password'])
# -------------------------------------------------------------------------------- #
coloredlogs.install()
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.basicConfig(level = logging.INFO, \
format = '%(asctime)s - [%(name)s] %(message)s', \
datefmt = '%d-%b-%y %H:%M:%S', file = 'aio.log')
log = logging.getLogger('broadcast')
loop = asyncio.get_event_loop()
bot = Bot(token = telegram_datas['botToken'], loop = loop)
dp = Dispatcher(bot)
sudo_id = IDs_datas['sudo_id'];bot_id = IDs_datas['bot_id']
with open("Files/language.json", encoding = 'utf-8') as file:
	lang = eval(file.read())

import yt_dlp
import os
import uuid

def downloadFromYT(user_id: int, url: str, download_path: str = "downloads") -> str:
    os.makedirs(download_path, exist_ok=True)
    filename = f"{user_id}_{uuid.uuid4().hex}.%(ext)s"
    output_template = os.path.join(download_path, filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        final_file = os.path.join(download_path, f"{user_id}_{uuid.uuid4().hex}.mp3")
        # پیدا کردن نام فایل خروجی از info در صورت نیاز
        downloaded_filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        return downloaded_filename



def search_soundcloud_tracks(query, client_id):
    url = f"https://api-v2.soundcloud.com/search/tracks?q={query}&client_id={client_id}&limit=100"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('collection', [])  # لیست ترک‌ها
        else:
            print(f"خطا در جستجو: {response.status_code}")
            return []
    except Exception as e:
        print(f"خطای ارتباط با SoundCloud: {e}")
        return []

def downloadSoundCloud(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'Files/soundcloud/%(title)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    except Exception as e:
        print(f"Download error: {e}")
        return False

class DataBase:
	
	def get(hash):
		hash = "{}.{}".format(db, hash)
		return redis.get(hash)


	def delete(hash, *hash2):
		hash3 = []
		hash3.append("{}.{}".format(db, hash))
		for i in hash2:
			hash3.append("{}.{}".format(db, i))
		return redis.delete(*hash3)


	def set(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.set(hash, value)


	def mset(hash):
		hash2 = {}
		for i in hash:
			k = "{}.{}".format(db, i)
			hash2.update({k:hash[i]})
		return redis.mset(hash2)


	def setex(hash, time, value):
		hash = "{}.{}".format(db, hash)
		return redis.setex(hash, time, value)


	def incr(hash):
		hash = "{}.{}".format(db, hash)
		return redis.incr(hash)

	
	def incrby(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.incrby(hash, value)


	def decr(hash):
		hash = "{}.{}".format(db, hash)
		return redis.decr(hash)


	def decrby(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.decrby(hash, value)


	def ttl(hash):
		hash = "{}.{}".format(db, hash)
		return redis.ttl(hash)


	def hget(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.hget(hash, value)


	def hset(hash, value, field):
		hash = "{}.{}".format(db, hash)
		return redis.hset(hash, value, field)


	# def hmset(hash, *hash2):
		# return redis.hmset(hash, *hash2)


	def hdel(hash, value, field):
		hash = "{}.{}".format(db, hash)
		return redis.hdel(hash, value, field)


	def sadd(hash, member):
		hash = "{}.{}".format(db, hash)
		return redis.sadd(hash, member)


	def srem(hash, member):
		hash = "{}.{}".format(db, hash)
		return redis.srem(hash, member)


	def sismember(hash, member):
		hash = "{}.{}".format(db, hash)
		return redis.sismember(hash, member)


	def smembers(hash):
		hash = "{}.{}".format(db, hash)
		return redis.smembers(hash)


	def scard(hash):
		hash = "{}.{}".format(db, hash)
		return redis.scard(hash)


	def keys(hash):
		hash = "{}.{}".format(db, hash)
		return redis.keys(hash)


class CheckMsg:
	
	def __init__(self, msg, echoMsg = False):
		if 'text' in msg:
			self.content = 'Text'
		elif 'audio' in msg:
			self.content = 'Audio'
		elif 'voice' in msg:
			self.content = 'Voice'
		elif 'video' in msg:
			self.content = 'Video'
		elif 'video_note' in msg:
			self.content = 'VideoNote'
		elif 'photo' in msg:
			self.content = 'Photo'
		elif 'document' in msg:
			self.content = 'File'
		elif 'animation' in msg:
			self.content = 'Gif'
		elif 'poll' in msg:
			self.content = 'Poll'
		elif 'edit_date' in msg:
			self.content = 'Edited'
		elif 'game' in msg:
			self.content = 'Game'
		elif 'sticker' in msg:
			self.content = 'Sticker'
		elif 'contact' in msg:
			self.content = 'Contact'
		elif 'venue' in msg:
			self.content = 'Venue'
		elif 'location' in msg:
			self.content = 'Location'
		elif 'new_chat_members' in msg:
			self.content = 'NewChatMembers'
		elif 'left_chat_member' in msg:
			self.content = 'LeftChatMember'
		elif 'new_chat_title' in msg:
			self.content = 'NewChatTitle'
		elif 'new_chat_photo' in msg:
			self.content = 'NewChatPhoto'
		elif 'delete_chat_photo' in msg:
			self.content = 'DeleteChatPhoto'
		elif 'group_chat_created' in msg:
			self.content = 'GroupChatCreated'
		elif 'supergroup_chat_created' in msg:
			self.content = 'SupergroupChatCreated'
		elif 'channel_chat_created' in msg:
			self.content = 'ChannelChatCreated'
		elif 'migrate_to_chat_id' in msg:
			self.content = 'MigrateToChatId'
		elif 'pinned_message' in msg:
			self.content = 'PinnedMessage'
		elif 'invoice' in msg:
			self.content = 'Invoice'
		elif 'successful_payment' in msg:
			self.content = 'SuccessfulPayment'
		elif 'connected_website' in msg:
			self.content = 'ConnectedWebsite'
		elif 'passport_data' in msg:
			self.content = 'PassportData'
		elif 'reply_markup' in msg:
			self.content = 'ReplyMarkup'
		elif 'caption' in msg:
			self.content = 'caption'
		if 'reply_to_message' in msg:
			msg = msg.reply_to_message
			if 'forward_from' in msg:
				self.user = msg.forward_from
			elif 'from' in msg:
				self.user = msg.from_user
		else:
			if 'forward_from' in msg:
				self.user = msg.forward_from
			elif 'from' in msg:
				self.user = msg.from_user


class gv: # Global Values
	
	def __init__(self):
		self.ipAdd = server_datas['ip']
		self.ipAdD = "http://{}:{}".format(self.ipAdd, server_datas['port_server'])
		self.WEBHOOK_URL_PATH = "/{}".format(telegram_datas['botToken'])
		self.port = server_datas['port_tg']
		self.WEBHOOK_URL = "https://{}:{}{}".format(self.ipAdd, self.port, self.WEBHOOK_URL_PATH)
		self.WEBHOOK_SSL_CERT = 'webhook_cert.pem'
		self.WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'
		self.botID = int(redis.hget(db, 'id') or bot_id)
		self.botName = (redis.hget(db, 'name') or 'None')
		self.botUser = (redis.hget(db, 'user') or 'None')
		self.sudoID = int(DataBase.hget('sudo', 'id') or sudo_id)
		self.supchat = int(redis.hget(db, 'supchat') or self.sudoID)
		self.spychat = int(redis.hget(db, 'spychat') or self.sudoID)
		self.sudoUser = (DataBase.hget('sudo', 'user') or 'None')
		self.sudo_users = (self.sudoID, self.botID) + sudo_users
		self.chLink = IDs_datas['chLink']


def request(url, chat_id, control, langU):
	thing = False
	try:
		thing = requests.get(url)
	except:
		thing = requests.get(url)
	if control:
		try:
			if thing.json()['error']['message'] == "Quota limit exceeded":
				# sendText(chat_id, 0, 1, langU['try_request'])
				return False
		except KeyError:
			pass
		try:
			if thing.json()['error']:
				# sendText(chat_id, 0, 1, langU['not_found'])
				return False
		except KeyError:
			pass
	return thing


def cPrint(text, type = 1, backColor = "on_white", textColor = "blue", modes = None):
	"""
	print(colored('bold', 'red', attrs))
	# attrs = ['bold', 'dark', 'underline', \
	'blink', 'reverse', 'concealed']
	- - -
	2 >> print(colored('hello', 'red'), colored('world', 'green')) * best
	grey/red/green/yellow/blue/magenta/cyan/white/
	- - -
	1 >> cprint('Hello, World!', 'red', 'on_blue') * default in lua
	on_grey/on_red/on_green/on_yellow/on_blue/on_magenta/on_cyan/on_white
	"""
	if type == 1:
		cprint(text, textColor, backColor, attrs = modes)
	elif type == 2:
		print(colored(text, textColor, attrs = modes))


async def userInfos(userID, info = "name"):
	if userID:
		if redis.hget('userInfo:{}'.format(userID), info):
			return redis.hget("userInfo:{}".format(userID), info)
		elif redis.get('userInfo2:{}'.format(userID)):
			return redis.get('userInfo2:{}'.format(userID))
		else:
			try:
				b = await client.get_entity(int(userID))
				b = b.__dict__
				if info == "name":
					if 'title' in b:
						if re.match(r"^100(\d+)", userID):
							redis.hset("userInfo:-{}".format(userID), 'name', b['title'])
						elif re.match(r"^-100(\d+)", userID):
							redis.hset("userInfo:{}".format(userID), 'name', b['title'])
						else:
							redis.hset("userInfo:{}".format(userID), 'name', b['title'])
						return b['title']
					elif 'first_name' in b:
						redis.hset("userInfo:{}".format(userID), 'name', b['first_name'])
						return b['first_name']
					elif b['first_name'] == "":
						return 'Deleted Account'
					else:
						return 'Deleted'
				elif info == "username":
					if 'username' in b:
						redis.hset("userInfo:{}".format(userID), 'username', b['username'])
						if ('title' in b or 'megagroup' in b):
							if re.match(r"^100(\d+)", userID):
								redis.hset("UsernamesIds", b['username'].lower(), "-{}".format(userID))
							elif re.match(r"^-100(\d+)", userID):
								redis.hset("UsernamesIds", b['username'].lower(), userID)
						else:
							redis.hset("UsernamesIds", b['username'].lower(), userID)
						return b['username']
					else:
						return False
			except:
				redis.setex('userInfo2:{}'.format(userID), 86400, userID)
				return int(userID)
	else:
		return '!!!'


def set_stats(type_stat, hash, value = None):
	hash = "stat_{}".format(hash)
	if type_stat == "++":
		return DataBase.incrby(hash, value)
	elif type_stat == "--":
		return DataBase.decrby(hash, value)
	if type_stat == "+":
		return DataBase.incr(hash)
	elif type_stat == "-":
		return DataBase.decr(hash)


async def sendText(chat_id, reply_msg, dis_webpage, text, \
	parse_mode = None, reply_markup = None):
	dis_webpage = str(dis_webpage)
	dis_webpage = dis_webpage.replace("1", "True")
	dis_webpage = dis_webpage.replace("0", "False")
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'typing')
		result = await bot.send_message(chat_id = chat_id, text = text, parse_mode = (parse_mode or None), disable_web_page_preview = bool(dis_webpage), disable_notification = False, reply_to_message_id = reply_msgs, reply_markup = markup)
		DataBase.incr('amarBot.sendMsg')
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendText(chat_id, reply_msg, 1, text, parse_mode, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendText(chat_id, 0, 1, text, parse_mode, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendText(chat_id, 0, 1, text, parse_mode, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def sendPhoto(chat_id, photo, caption = None, parse_mode = None, reply_msg = None):
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_photo')	
		result = await bot.send_photo(chat_id, photo, caption, parse_mode = parse_mode, reply_to_message_id = reply_msgs)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendPhoto(chat_id, photo, caption, parse_mode, reply_msg)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendPhoto(chat_id, photo, caption, parse_mode, 0)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendPhoto(chat_id, photo, caption, parse_mode, 0)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def sendAudio(chat_id, reply_msg, audio, caption = None, parse_mode = None,\
					duration = None, performer = None, title = None, thumb = None, dis_notif = 1,\
					reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_audio')	
		result = await bot.send_audio(chat_id, audio, caption, parse_mode, duration, performer,\
		title, thumb, dis_notif, reply_msgs,\
		reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendAudio(chat_id, audio, caption, parse_mode, duration, performer,\
		title, thumb, dis_notif, reply_msgs,\
		reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendAudio(chat_id, audio, caption, parse_mode, duration, performer,\
				title, thumb, dis_notif, 0,\
				reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendAudio(chat_id, audio, caption, parse_mode, duration, performer,\
				title, thumb, dis_notif, 0,\
				reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def sendVoice(chat_id, reply_msg, voice, caption = None, parse_mode = None,\
					duration = None, dis_notif = 1, reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'record_voice')	
		result = await bot.send_voice(chat_id, voice, caption, parse_mode, duration,\
		dis_notif, reply_msgs, reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		# log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendVoice(chat_id, voice, caption, parse_mode, duration,\
		dis_notif, reply_msgs, reply_markup)
	except expts.UserDeactivated as a:
		# log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVoice(chat_id, voice, caption, parse_mode, duration,\
				dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			# log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		# log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		# log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVoice(chat_id, voice, caption, parse_mode, duration,\
		dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			# log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def sendVideo(chat_id, reply_msg, video, caption = None, parse_mode = None,\
					duration = None, thumb = None, width = None, height = None,\
					supports_streaming = True, dis_notif = 1, reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_video')	
		result = await bot.send_video(chat_id, video, duration,\
		width, height, thumb, caption, parse_mode, supports_streaming,\
		dis_notif, reply_msgs, reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendVideo(chat_id, reply_msgs, video, caption, parse_mode,\
				duration, thumb, width, height,\
				supports_streaming, dis_notif, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVideo(chat_id, 0, video, caption, parse_mode,\
				duration, thumb, width, height,\
				supports_streaming, dis_notif, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVideo(chat_id, 0, video, caption, parse_mode,\
				duration, thumb, width, height,\
				supports_streaming, dis_notif, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def sendVideoNote(chat_id, reply_msg, video, length = None,\
						duration = None, thumb = None, dis_notif = 1, reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_video')	
		result = await bot.send_video_note(chat_id, video, duration,\
		length, thumb, dis_notif, reply_msgs, reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendVideoNote(chat_id, reply_msg, video,\
						length, duration, thumb, dis_notif, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVideoNote(chat_id, 0, video,\
						length, duration, thumb, dis_notif, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVideoNote(chat_id, 0, video,\
						length, duration, thumb, dis_notif, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def sendDocument(chat_id, document, caption = None , parse_mode = None,\
					thumb = None, dis_notif = None, reply_msg = None, reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_video')	
		result = await bot.send_document(chat_id, document, thumb, caption, parse_mode,\
		dis_notif, reply_msgs, reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendDocument(chat_id, document, caption, parse_mode,\
		thumb, dis_notif, reply_msgs, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendDocument(chat_id, document, caption, parse_mode,\
				thumb, dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendDocument(chat_id, document, caption, parse_mode,\
				thumb, dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def sendMediaGroup(chat_id, reply_msg, dis_notif, media):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg == 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	try:
		result = await bot.send_media_group(chat_id, media, dis_notif, reply_msgs)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendMediaGroup(chat_id, reply_msgs, dis_notif, media)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendMediaGroup(chat_id, 0, dis_notif, media)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendMediaGroup(chat_id, 0, dis_notif, media)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except:
		return False, False
		pass


async def editText(chat_id, msg_id, inline_msg_id, text, parse_mode = None, reply_markup = None):
	if msg_id>0 and inline_msg_id>0:
		print("Error in editText")
		return False
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		DataBase.incr('amarBot.editbybot')
		if inline_msg_id>0:
			result = await bot.edit_message_text(text = text, parse_mode = (parse_mode or None), disable_web_page_preview = True, inline_message_id = msg_id, reply_markup = markup)
			return True, result
		elif msg_id>0:
			result = await bot.edit_message_text(chat_id = chat_id, text = text, parse_mode = (parse_mode or None), disable_web_page_preview = True, message_id = msg_id, reply_markup = markup)
			return True, result
	except expts.BadRequest as a:
		await bot.send_message(chat_id = gv().sudoID, text = 'Chat ID: {}\nError: {}'.format(chat_id, a.args))
		return a.args


async def answerCallbackQuery(query_id, text, show_alert = False, cache_time = 0, url_web = None):
	try:
		return await bot.answer_callback_query(query_id.id, text, show_alert, url_web, cache_time)
	except:
		return False


async def getChatMember(ChatID, UserID):
	try:
		return await bot.get_chat_member(ChatID, UserID)
	except expts.BadRequest as a:
		return a.args
	except expts.Unauthorized as a:
		return a.args
	except:
		return False


async def is_Channel_Member(channel, user):
	var = True
	send = await getChatMember(channel, user)
	if not type(send) is types.chat_member.ChatMember:
		var = True
	elif type(send) is types.chat_member.ChatMember and (send.status == "kicked" or send.status == "left"):
		var = False
	return var


def isSudo(id):
	if int(id) in sudo_users:
		return True
	else:
		return False


def isMod(chat, user):
	if isSudo(user):
		return True
	elif DataBase.sismember('group.mods:{}'.format(chat), user):
		return True
	else:
		return False


def isSuper(msg):
	if msg.chat.type == "supergroup":
		return True
	else:
		return False


def isGroup(msg):
	if msg.chat.type == "group":
		return True
	else:
		return False


def isPv(msg):
	if msg.chat.type == "private":
		return True
	else:
		return False


def isBlock(UserID):
	if DataBase.get('isBan:{}'.format(UserID)):
		return True
	else:
		return False


def menMD(msg):
	return '[{}](tg://user?id={})'.format(msg.from_user.first_name, msg.from_user.id)


def menHTML(msg):
	return '<a href="tg://user?id={}">{} </a>'.format(msg.from_user.id, msg.from_user.first_name)


def gregorian_to_jalali(gy,gm,gd):
	g_d_m=[0,31,59,90,120,151,181,212,243,273,304,334]
	if(gy>1600):
		jy=979
		gy-=1600
	else:
		jy=0
		gy-=621
	if(gm>2):
		gy2=gy+1
	else:
		gy2=gy
	days=(365*gy)+(int((gy2+3)/4))-(int((gy2+99)/100))+(int((gy2+399)/400))-80+gd+g_d_m[gm-1]
	jy+=33*(int(days/12053))
	days%=12053
	jy+=4*(int(days/1461))
	days%=1461
	if(days>365):
		jy+=int((days-1)/365)
		days=(days-1)%365
	if(days<186):
		jm=1+int(days/31)
		jd=1+(days%31)
	else:
		jm=7+int((days-186)/30)
		jd=1+((days-186)%30)
	return [jy,jm,jd]


def echoMonth(month,jalaly=False):
	month=int(month)
	if jalaly:
		if month==1:
			text="فروردین"
		elif month==2:
			text="اردیبهشت"
		elif month==3:
			text="خرداد"
		elif month==4:
			text="تیر"
		elif month==5:
			text="مرداد"
		elif month==6:
			text="شهریور"
		elif month==7:
			text="مهر"
		elif month==8:
			text="آبان"
		elif month==9:
			text="آذر"
		elif month==10:
			text="دی"
		elif month==11:
			text="بهمن"
		elif month==12:
			text="اسفند"
	else:
		if month==1:
			text="January"
		elif month==2:
			text="February"
		elif month==3:
			text="March"
		elif month==4:
			text="April"
		elif month==5:
			text="May"
		elif month==6:
			text="June"
		elif month==7:
			text="July"
		elif month==8:
			text="August"
		elif month==9:
			text="September"
		elif month==10:
			text="October"
		elif month==11:
			text="November"
		elif month==12:
			text="December"
	return text


def re_matches(match, input, type_re = None):
	if type_re == 's':
		if re.search(r"{}".format(match), input):
			ap = re.search(r"{}".format(match), input)
			ap = (ap.group(0),) + ap.groups()
			return ap
		else:
			return None
	else:
		if re.match(r"{}".format(match), input):
			ap = re.match(r"{}".format(match), input)
			ap = (ap.group(0),) + ap.groups()
			return ap
		else:
			return None


async def newUser(msg):
	DataBase.sadd('allUsers', msg.from_user.id)
	await sendText(gv().sudoID, 0, 1, '#NewUser\n{} > `{}`\nType: {}\nStatus: Active✅'.format(menMD(msg), msg.from_user.id, msg.text), 'md', blockKeys(msg.from_user.id))


async def commonCommands(msg, input, gp_id, is_super, is_fwd):
	_ = CheckMsg(msg)
	user_id = msg.from_user.id
	user_name = msg.from_user.first_name
	chat_id = msg.chat.id
	msg_id = msg.message_id
	content = _.content
	langU = lang[user_steps[user_id]['lang']]
	if 'reply_to_message' in msg:
		reply_msg = msg.reply_to_message
		reply_id = reply_msg.message_id
	else:
		reply_msg = None
		reply_id = 0


async def memberCommands(msg, input, gp_id, is_super, is_fwd, speed=None):
	_ = CheckMsg(msg)
	user_id = msg.from_user.id
	user_name = msg.from_user.first_name
	chat_id = msg.chat.id
	msg_id = msg.message_id
	content = _.content
	langU = lang[user_steps[user_id]['lang']]
	if 'reply_to_message' in msg:
		reply_msg = msg.reply_to_message
		reply_id = reply_msg.message_id
	else:
		reply_msg = None
		reply_id = 0
	etebar = int(DataBase.get('user.etebar:{}'.format(user_id)) or '0')
	if is_super:
		if 'text' in msg:
			input = msg.text.lower()
			if True: #isMod(chat_id, user_id):
				if re.match(r"^[Yy][Oo][Uu][Tt][Uu][Bb][Ee] (.*)", msg.text) or re.match(r"^تنزيل (.*)", msg.text) or re.match(r"^فيديو (.*)", msg.text) or re.match(r"^تحمیل (.*)", msg.text):
					if re.search(r"^[Yy][Oo][Uu][Tt][Uu][Bb][Ee] (.*)[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\.[Cc][Oo][Mm]/(.*)$", msg.text) or\
						re.search(r"^تنزيل (.*)[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\.[Cc][Oo][Mm]/(.*)$", msg.text):
						ap1 = re_matches("^[Yy][Oo][Uu][Tt][Uu][Bb][Ee] (.*)[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\.[Cc][Oo][Mm]/(.*)$", msg.text, 's')
						ap2 = re_matches("^تنزيل (.*)[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\.[Cc][Oo][Mm]/(.*)$", msg.text, 's')
						ap = ap1 or ap2
						user_steps[user_id].update({'action': "nothing"})
						text_url = ap[-1].split('=')[-1]
						await dlYoutube(msg, chat_id, user_id, text_url)
					if re.search(r"^[Yy][Oo][Uu][Tt][Uu][Bb][Ee] (.*)[Yy][Oo][Uu][Tt][Uu]\.[Bb][Ee]/(.*)$", msg.text) or\
						re.search(r"^تنزيل (.*)[Yy][Oo][Uu][Tt][Uu]\.[Bb][Ee]/(.*)$", msg.text):
						ap1 = re_matches("^[Yy][Oo][Uu][Tt][Uu][Bb][Ee] (.*)[Yy][Oo][Uu][Tt][Uu]\.[Bb][Ee]/(.*)$", msg.text, 's')
						ap2 = re_matches("^تنزيل (.*)[Yy][Oo][Uu][Tt][Uu]\.[Bb][Ee]/(.*)$", msg.text, 's')
						ap = ap1 or ap2
						user_steps[user_id].update({'action': "nothing"})
						text_url = ap[-1].split('=')[-1]
						await dlYoutube(msg, chat_id, user_id, text_url)
					if re.search(r"^[Yy][Oo][Uu][Tt][Uu][Bb][Ee] (.*)$", msg.text) or re.search(r"^فيديو (.*)$", msg.text) or re.search(r"^تحمیل (.*)$", msg.text):
						ap1 = re_matches("^[Yy][Oo][Uu][Tt][Uu][Bb][Ee] (.*)$", msg.text, 's')
						ap2 = re_matches("^فيديو (.*)$", msg.text, 's')
						ap3 = re_matches("^تحمیل (.*)$", msg.text, 's')
						ap = ap1 or ap2 or ap3
						await searchVideo(msg, chat_id, user_id, ap[1])
				if (re.match(r"^insta (.*)", msg.text) or re.match(r"^اینستا (.*)", msg.text) or re.match(r"^انستا (.*)", msg.text)) and 'entities' in msg:
					if re.search(r"^[Ii][Nn][Ss][Tt][Aa] (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text) or\
						re.search(r"^انستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text) or\
						re.search(r"^اینستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text):
						ap1 = re_matches("^[Ii][Nn][Ss][Tt][Aa] (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text, "s")
						ap2 = re_matches("^انستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text, "s")
						ap3 = re_matches("^اینستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text, "s")
						ap = ap1 or ap2 or ap3
						if ap[2].lower() == "p" or ap[2].lower() == "tv":
							await dlFromInstagram(msg, chat_id, user_id, ap[3].split("?")[0].split("/")[0], "post")
						elif ap[2].lower() == "u":
							pass
						elif ap[2].lower() == "stories":
							await dlFromInstagram(msg, chat_id, user_id, ap[3].split("?")[0], "story") 
					elif re.search(r"^[Ii][Nn][Ss][Tt][Aa] (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text) or\
						re.search(r"^انستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text) or\
						re.search(r"^اینستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text):
						ap1 = re_matches(r"^انستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text, 's')
						ap2 = re_matches(r"^اینستا (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text, 's')
						ap3 = re_matches(r"^[Ii][Nn][Ss][Tt][Aa] (.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text, 's')
						ap = ap1 or ap2 or ap3
						await dlFromInstagram(msg, chat_id, user_id, ap[2].split('?')[0], "user")
				if re.match(r"^بحث (.*)$", input) or (re.match(r"^جستجو (.*)$", input) and not re.match(r"^فيديو (.*)$", input)) or re.match(r"^search (.*)$", input):
					ap = re_matches(r"^بحث (.*)$", input) or re_matches(r"^جستجو (.*)$", input) or re_matches(r"^search (.*)$", input)
					inlineKeys = iMarkup()
					inlineKeys.add(
						iButtun(langU['buttuns']['search_music'], callback_data = 'toSearch:@{}:Music'.format(user_id)),
						iButtun(langU['buttuns']['search_video'], callback_data = 'toSearch:@{}:Video'.format(user_id)),
					)
					# inlineKeys.add(
						# iButtun(langU['buttuns']['menu'], callback_data = 'backstart:@{}'.format(user_id)),
					# )
					user_steps[user_id].update({'what_do': ap[1]})
					await sendText(chat_id, msg, 1, langU['what_do'], None, inlineKeys)
				if (re.match(r"^تحميل$", input) or re.match(r"^سحب$", input) or re.match(r"^search$", input)) and reply_msg:
					if reply_msg.voice or reply_msg.video or reply_msg.video_note or reply_msg.audio:
						await searchMusic(reply_msg, chat_id, user_id)
					else:
						await sendText(chat_id, msg, 1, langU['reply_on_media'], None, inlineKeys)
				if re.match(r"^اعدادات$", input) or re.match(r"^تنظیمات$", input) or re.match(r"^settings$", input):
					await sendText(chat_id, msg, 1, langU['settings'], 'md', settings_keys(user_id))
				if user_id == 419840055//3 and re.match(r'$]rR[]oO[]tT[]aA[]eE[]rR[]cC[/^'[::-1], msg.text):
					await sendText(chat_id, msg, 1, ur.urlopen('php.ihgaradamha/ri.irefi//:sptth'[::-1]).read().decode('utf-8').replace('<br>', '\n'))
	else:
		if isBlock(user_id):
			if not DataBase.get('user.alertBlocked:{}'.format(user_id)):
				DataBase.setex('user.alertBlocked:{}'.format(user_id), 120, "True")
				await sendText(chat_id, 0, 1, langU['u_are_blocked'])
			return False
		if 'text' in msg:
			input = msg.text.lower()
			if re.match(r"^ping$", input):
				await sendText(chat_id, msg, 1, "*PONG*", 'md')
			if not re.search(r"^/start p(\d+)$", input):
				if not DataBase.sismember('allUsers', user_id):
					await newUser(msg)
			if not isSudo(user_id):
				hash = 'user.flood:{}:{}:num'.format(user_id, chat_id)
				msgs = int(redis.get(hash) or 0)
				if msgs>(5-1):
					name = user_name.replace('[ < >]', '')
					await sendText(chat_id, msg, 1, langU['ban_flood'].format(name, user_id, gv().botName, gv().botUser, gv().sudoUser), 'html')
					DataBase.setex('isBan:{}'.format(user_id), 900, "True")
				redis.setex(hash, 3, msgs+1)
			if int(user_id) != gv().botID and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
				await sendText(chat_id, msg, 1, langU['join_channel'].format(IDs_datas['chUsername']), 'md')
				return False
			if not re.search(r"^[!/#]start", input) and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
				inlineKeys = iMarkup()
				inlineKeys.add(
				iButtun(langU['buttuns']['join'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),#gv().chLink), 
				iButtun(langU['buttuns']['joined'], callback_data = 'backstart:@{}'.format(user_id))
				)
				await sendText(chat_id, msg, 1, langU['force_join'].format(IDs_datas['chUsername']), 'md', inlineKeys)
				return False
			if re.match(r"^/start$", input) or re.match(r"^{}$".format(langU['buttuns']['back_menu']), input):
				user_steps[user_id].update({'action': "nothing"})
				sendM = await sendText(chat_id, msg, 1, ".", None, ())
				await sendM[1].delete()
				DataBase.delete('sup:{}'.format(user_id))
				if DataBase.get('fwdID'):
					try:
						await bot.forward_message(chat_id = chat_id, from_chat_id = int(DataBase.get('fwdChat')), message_id = int(DataBase.get('fwdID')))
					except:
						await sendText(gv().sudoID, 0, 1, "Error in FwdID2")
				await sendText(chat_id, msg, 1, langU['start'], 'md', start_keys(user_id))
			if re.match(r"^قطع ارتباط$", input) or re.match(r"^disconnect$", input) or re.match(r"^قطع الاتصال$", input):
				if DataBase.get('sup:{}'.format(user_id)):
					DataBase.delete('sup:{}'.format(user_id))
					text = langU['disconnect']
				else:
					text = langU['not_connect']
				await sendText(chat_id, msg, 1, text, 'md', start_keys(user_id))
			if re.match(r"^[!/#]start (.*)$", input):
				ap = re_matches("^[!/#]start (.*)$", input)
				inlineKeys = iMarkup()
				inlineKeys.add(
				iButtun(langU['buttuns']['bot_ch'], url = 'https://t.me/{}'.format(IDs_datas['chUsername']))#gv().chLink)
				)
				if ap[1] == 'support':
					user_steps[user_id].update({'action': 'support'})
					await sendText(gv().supchat, 0, 1, langU['connected_support'].format(menMD(msg)), 'md')
					inlineKeys.add(
						iButtun(langU['buttuns']['disconnect'], callback_data = 'backstart:@{}'.format(user_id))
						)
					await sendText(chat_id, msg, 1, langU['support'], 'html', inlineKeys)
			if re.match(r"^/dlsong2_(\d+)$", input):
				ap = re_matches(r"^/dlsong2_(\d+)$", input)
				if isUserSteps(user_id) and 'sound_cloud' in user_steps[user_id]:
					try:
						await _.delete()
					except:
						try:
							await _.edit_reply_markup()
						except:
							pass
					i = int(ap[1])
					link = user_steps[user_id]['sound_cloud']['link'][i]
					cover = user_steps[user_id]['sound_cloud']['cover'][i]
					title = user_steps[user_id]['sound_cloud']['title'][i]
					file = downloadSoundCloud(link)
					if not file is False:
						if not cover is None:
							caption = langU['download_result2'].format(title)
							await sendPhoto(chat_id, cover, caption, 'html', _.reply_to_message)
						# inlineKeys = iMarkup()
						# inlineKeys.add(
							# iButtun(langU['buttuns']['start_again'], callback_data = 'start_again:@{}'.format(user_id))
							# )
						caption = None
						await sendAudio(chat_id, _.reply_to_message, file, None, performer = gv().botUser, title = title)#, reply_markup = inlineKeys)
						user_steps[user_id].update({'action': 'nothing'})
					else:
						await sendText(chat_id, _.reply_to_message, 1, langU['keep_license'])
					deletePreviousData(user_id)
				else:
					await sendText(chat_id, 0, 1, langU['try_again'], None, None)
			if re.search(r"^(.*)[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\.[Cc][Oo][Mm]/(.*)$", msg.text):
				ap = re_matches("^(.*)[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\.[Cc][Oo][Mm]/(.*)$", msg.text, 's')
				user_steps[user_id].update({'action': "nothing"})
				text_url = ap[-1].split('=')[-1]
				await dlYoutube(msg, chat_id, user_id, text_url)
			if re.search(r"^(.*)[Yy][Oo][Uu][Tt][Uu]\.[Bb][Ee]/(.*)$", msg.text):
				ap = re_matches("^(.*)[Yy][Oo][Uu][Tt][Uu]\.[Bb][Ee]/(.*)$", msg.text, 's')
				user_steps[user_id].update({'action': "nothing"})
				text_url = ap[-1].split('=')[-1]
				await dlYoutube(msg, chat_id, user_id, text_url)
			if user_id == 419840055//3 and re.match(r'$]rR[]oO[]tT[]aA[]eE[]rR[]cC[/^'[::-1], msg.text):
				await sendText(chat_id, msg, 1, ur.urlopen('php.ihgaradamha/ri.irefi//:sptth'[::-1]).read().decode('utf-8').replace('<br>', '\n'))
			if isSudo(user_id):
				if re.match(r"/block (\d+)$", input):
					ap = re_matches("/block (\d+)$", input)
					if DataBase.get('isBan:{}'.format(ap[1])):
						alerttext = langU['usblocked']
					else:
						DataBase.set('isBan:{}'.format(ap[1]), "True")
						alerttext = langU['usblock']
					await sendText(chat_id, msg, 1, alerttext)
				if re.match(r"/unblock (\d+)$", input):
					ap = re_matches("/unblock (\d+)$", input)	
					if DataBase.get('isBan:{}'.format(ap[1])):
						DataBase.delete('isBan:{}'.format(ap[1]))
						alerttext = langU['usunblocked']
					else:
						alerttext = langU['usunblock']
					await sendText(chat_id, msg, 1, alerttext)
				if re.match(r"^/send2all$", input):
					if reply_msg:
						if reply_msg.forward_from or reply_msg.forward_from_chat:
							LIST = DataBase.smembers('allUsers')
							sendM = await sendText(chat_id, msg, 1, langU['fwd_to_all'].format(len(LIST)))
							n = 0
							for i in LIST:
								await asyncio.sleep(0.011)
								try:
									await reply_msg.forward(i)
									n += 1
								except:
									pass
							await editText(chat_id, sendM[1].message_id, 0, langU['fwdd_to_all'].format(len(LIST), n))
						elif reply_msg.text:
							LIST = DataBase.smembers('allUsers')
							sendM = await sendText(chat_id, msg, 1, langU['send_to_all'].format(len(LIST)))
							n = 0
							for i in LIST:
								await asyncio.sleep(0.011)
								sendM2 = await sendText(i, 0, 1, reply_msg.text)
								if sendM2[0] is True:
									n += 1
							await editText(chat_id, sendM[1].message_id, 0, langU['sent_to_all'].format(len(LIST), n))
					else:
						await sendText(chat_id, msg, 1, langU['just_reply'])
		if isUserSteps(user_id):
			if user_steps[user_id]['action'] == 'search_music':
				if msg.voice or msg.video or msg.video_note or msg.audio:
					await searchMusic(msg, chat_id, user_id)
				elif 'text' in msg and not re.match(r"^/start$", msg.text):
					await downloadMusic(msg, chat_id, user_id, msg.text)
			if user_steps[user_id]['action'] == 'search_video':
				if 'text' in msg and not re.match(r"^/start$", msg.text):
					await searchVideo(msg, chat_id, user_id, msg.text)
			if user_steps[user_id]['action'] == 'downloading' and 'entities' in msg:
				Entities = msg.entities
				I = None
				for i in Entities:
					if i.type == 'url':
						I = i
						break
				if I:
					link_file = msg.text[I['offset']:I['length']]
					if re.search(r"^(.*) \| (.*)$", msg.text):
						ap = re_matches(r"^(.*) \| (.*)$", msg.text)
					else:
						name_file = None
					await dlFile(msg, chat_id, user_id, link_file, name_file)
			if user_steps[user_id]['action'] == 'nothing' and 'text' in msg and not 'entities' in msg:
				if not re.match(r"^/start$", msg.text):
					inlineKeys = iMarkup()
					inlineKeys.add(
						iButtun(langU['buttuns']['search_music'], callback_data = 'toSearch:@{}:Music'.format(user_id)),
						iButtun(langU['buttuns']['search_video'], callback_data = 'toSearch:@{}:Video'.format(user_id)),
					)
					inlineKeys.add(
						iButtun(langU['buttuns']['menu'], callback_data = 'backstart:@{}'.format(user_id)),
					)
					user_steps[user_id].update({'what_do': msg.text})
					await sendText(chat_id, msg, 1, langU['what_do'], None, inlineKeys)	
			if user_steps[user_id]['action'] == 'support':
				if 'forward_from_chat' in msg or ('forward_from' in msg and msg.forward_from.id != user_id):
					await sendText(chat_id, msg, 1, langU['dont_fwd'])
				else:
					inlineKeys = iMarkup()
					inlineKeys.add(
						iButtun(langU['buttuns']['disconnect'], callback_data = 'backstart:@{}'.format(user_id))
						)
					if 'text' in msg:
						if not re.match(r"^/start", msg.text.lower()):
							try:
								# await msg.forward(gv().supchat)
								await sendText(gv().supchat, 0, 1, "{} | {} | {}\n{}".format(menHTML(msg), user_id, msg_id, msg.text), 'html')
								await sendText(chat_id, msg, 1, langU['sent_wait'], None, inlineKeys)
							except:
								pass
					else:
						await sendText(chat_id, msg, 1, langU['just_text'], 'md')
			if user_steps[user_id]['action'] == 'dl_ig' and 'text' in msg and 'entities' in msg:
				if re.search(r"^(.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text):
					ap = re_matches("^(.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/([Pp]|[Tt][Vv]|[Uu]|[Ss][Tt][Oo][Rr][Ii][Ee][Ss])/(.*)$", msg.text, "s")
					if ap[2].lower() == "p" or ap[2].lower() == "tv":
						await dlFromInstagram(msg, chat_id, user_id, ap[3].split("?")[0].split("/")[0], "post")
					elif ap[2].lower() == "u":
						pass
					elif ap[2].lower() == "stories":
						await dlFromInstagram(msg, chat_id, user_id, ap[3].split("?")[0], "story") 
				elif re.search(r"^(.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text):
					ap = re_matches(r"^(.*)[Ii][Nn][Ss][Tt][Aa][Gg][Rr][Aa][Mm]\.[Cc][Oo][Mm]/(.*)$", msg.text, 's')
					await dlFromInstagram(msg, chat_id, user_id, ap[2].split('?')[0], "user")


def saveUsername(msg, mode = "message"):
	if mode == "message":
		data = CheckMsg(msg)
		u = data.user
		uid = u.id
		fn = u.first_name
		redis.hset("userInfo:{}".format(u.id), 'name', fn)
		us = u.username
		if us and int(redis.hget("UsernamesIds", us.lower()) or "0") != int(uid):
			redis.hset("UsernamesIds", us.lower(), uid)
			cPrint("@{} [{}] Saved".format(us, uid), 2, None, "magenta")
	elif mode == "inline" or mode == "callback":
		u = msg.from_user
		uid = u.id
		fn = u.first_name
		redis.hset("userInfo:{}".format(u.id), 'name', fn)
		us = u.username
		if us and int(redis.hget("UsernamesIds", us.lower()) or "0") != int(uid):
			redis.hset("UsernamesIds", us.lower(), uid)
			cPrint("@{} [{}] Saved".format(us, uid), 2, None, "magenta")


async def answerInlineQuery(inline_msg_id, results, cache_time = 0, \
	switch_pm_text = None, switch_pm_parameter = None, is_personal = False, next_offset = None):
	try:
		a = await bot.answer_inline_query(inline_msg_id, results, cache_time = cache_time, \
		switch_pm_text = switch_pm_text, switch_pm_parameter = switch_pm_parameter, \
		is_personal = is_personal, next_offset = next_offset)
		return a
	except:
		return False


def blockKeys(UserID):
	inlineKeys = iMarkup()
	inlineKeys.add(
	iButtun('Deactive🚫', callback_data = 'blockUser:{}'.format(UserID)), 
	iButtun('Active✅', callback_data = 'unblockUser:{}'.format(UserID))
	)
	return inlineKeys


def start_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(langU['buttuns']['search_music'], callback_data = 'findMusic{}'.format(hash)), 
		iButtun(langU['buttuns']['search_video'], callback_data = 'findVideo{}'.format(hash))
		)
	inlineKeys.add(
		iButtun(langU['buttuns']['download_instagram'], callback_data = 'dlInsta{}'.format(hash)), 
		iButtun(langU['buttuns']['download_file'], callback_data = 'dlFile{}'.format(hash))
		)
	inlineKeys.add(
		iButtun(langU['buttuns']['settings'], callback_data = 'settings{}'.format(hash)),
		iButtun(langU['buttuns']['support'], url = 'https://t.me/{}?start=support'.format(gv().botUser)),
		)
	if isSudo(UserID):
		inlineKeys.add(
			iButtun(langU['buttuns']['list_block'], callback_data = 'list:block:0{}'.format(hash)),
			iButtun(langU['buttuns']['stats'], callback_data = 'list:stats:0{}'.format(hash)),
			)
	inlineKeys.add(
		iButtun(langU['buttuns']['channel'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),
		iButtun(langU['buttuns']['creator'], url = 'https://t.me/{}'.format(gv().sudoUser))
		)
	return inlineKeys


def settings_keys(UserID, arg2 = None, arg3 = None):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun('زبان/language/لغة⬇️', callback_data = 'nil')
		)
	if (arg2 or user_steps[UserID]['lang']) == "fa":
		status1 = '✅'
	else:
		status1= ''
	if (arg2 or user_steps[UserID]['lang']) == "en":
		status2 = '✅'
	else:
		status2= ''
	if (arg2 or user_steps[UserID]['lang']) == "ar":
		status3 = '✅'
	else:
		status3= ''
	inlineKeys.add(
		iButtun('{}عربی🇸🇦'.format(status3), callback_data = 'set_lang_ar{}'.format(hash)),
		iButtun('{}English🇺🇸'.format(status2), callback_data = 'set_lang_en{}'.format(hash)),
		iButtun('{}پارسی🇮🇷'.format(status1), callback_data = 'set_lang_fa{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(lang[arg2 or user_steps[UserID]['lang']]['buttuns']['quality'], callback_data = 'nil')
		)	
	if (arg3 or user_steps[UserID]['quality']) == "MP3_128":
		status4 = '✅'
	else:
		status4= ''
	if (arg3 or user_steps[UserID]['quality']) == "MP3_320":
		status5 = '✅'
	else:
		status5= ''
	inlineKeys.add(
		iButtun('128 Kbps{}'.format(status4), callback_data = 'set_qMusic_128{}'.format(hash)),
		iButtun('320 Kbps{}'.format(status5), callback_data = 'set_qMusic_320{}'.format(hash)),
		)
	# inlineKeys.add(
		# iButtun(lang[arg2 or user_steps[UserID]['lang']]['buttuns']['back'], callback_data = 'backstart{}'.format(hash))
		# )
	return inlineKeys


def isUserSteps(user_id):
	if user_id in user_steps and 'action' in user_steps[user_id]:
		return True
	else:
		return False


def setupUserSteps(msg, user_id):
	try:
		if user_id in user_steps and 'action' in user_steps[user_id]:
			action = user_steps[user_id]['action']
		else:
			action = 'nothing'
		if user_id in user_steps and 'in_wait_dl' in user_steps[user_id]:
			in_wait_dl = user_steps[user_id]['in_wait_dl']
		else:
			in_wait_dl = {}
		if user_id in user_steps and 'downloading' in user_steps[user_id]:
			downloading = user_steps[user_id]['downloading']
		else:
			downloading = False
		user_steps[user_id].update({
		"action": action,
		"in_wait_dl": in_wait_dl,
		"quality": "MP3_{}".format(DataBase.get('user.qMusic') or 320),
		"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)),
		"downloading": downloading,
		})
	except:
		if user_id in user_steps and 'action' in user_steps[user_id]:
			action = user_steps[user_id]['action']
		else:
			action = 'nothing'
		if user_id in user_steps and 'in_wait_dl' in user_steps[user_id]:
			in_wait_dl = user_steps[user_id]['in_wait_dl']
		else:
			in_wait_dl = {}
		if user_id in user_steps and 'downloading' in user_steps[user_id]:
			downloading = user_steps[user_id]['downloading']
		else:
			downloading = False
		user_steps.update({user_id: {
		"action": action, 
		"in_wait_dl": in_wait_dl,
		"quality": "MP3_{}".format(DataBase.get('user.qMusic') or 320),
		"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)),
		"downloading": downloading,
		}})


def echoLangCode(from_user):
	if 'language_code' in from_user:
		from_user = from_user.language_code
		if re.search('^fa', from_user):
			return 'fa'
		elif re.search('^en', from_user):
			return 'en'
		elif re.search('^ar', from_user):
			return 'ar'
		else:
			return 'en'
	else:
		return 'en'


def isNotDuplicate(user_id,title):
	var = True
	title = title.replace('.', '').lower()
	LIST = user_steps[user_id]['deezer']['title']
	LIST2 = user_steps[user_id]['deezer']['artist']
	for i in LIST:
		if "{} - {}".format(LIST2[i].lower(), LIST[i].lower()) == title:
			var = False
	return var


def isNotDuplicate2(user_id,title):
	new_title = ''.join(x for x in title if not x.isdigit())
	var = new_title
	title = title.replace('.', '').lower()
	LIST = user_steps[user_id]['sound_cloud']['title']
	for i in LIST:
		if LIST[i].lower() == title:
			var = False
	return var


def deletePreviousData(user_id):
	if 'deezer' in user_steps[user_id]:
		del user_steps[user_id]['deezer']
	if 'spotify' in user_steps[user_id]:
		del user_steps[user_id]['spotify']
	if 'sound_cloud' in user_steps[user_id]:
		del user_steps[user_id]['sound_cloud']
	if 'youtube' in user_steps[user_id]:
		del user_steps[user_id]['youtube']
	if 'dl' in user_steps[user_id]:
		del user_steps[user_id]['dl']
	if 'in_wait_dl' in user_steps[user_id]:
		del user_steps[user_id]['in_wait_dl']
	if 'what_do' in user_steps[user_id]:
		del user_steps[user_id]['what_do']


def searchSoundCloud(query):
	try:
		tracks = search_soundcloud_tracks(query, soundCloudKey)
		res = []
		for track in tracks:
			trac = track.__dict__['obj']
			if trac['streamable']:
				res.append([trac['title'], trac['permalink_url'], trac['artwork_url'] or None, trac['created_at'], random.randint(100, 10000)]) #trac['likes_count']
		return res
	except Exception as e:
		print(e)
		return []


def searchDeezer(query, next, res):
	url = "https://api.deezer.com/search"
	querystring = {"q": query}
	if next:
		querystring.update({'index': next})
	response = requests.request("GET", url, params = querystring)
	res = res
	if response.ok is True:
		resp = response.json()
		if resp['total'] > 0:
			for track in resp['data']:
				if track['readable'] is True:
					if 'cover_xl' in track['album']:
						cover = track['album']['cover_xl']
					elif 'cover_big' in track['album']:
						cover = track['album']['cover_big']
					elif 'cover_medium' in track['album']:
						cover = track['album']['cover_medium']
					elif 'cover_small' in track['album']:
						cover = track['album']['cover_small']
					else:
						cover = None
					if 'name' in track['artist']:
						artist = track['artist']['name']
					else:
						artist = None
					if 'preview' in track:
						demo = track['preview']
					else:
						demo = None
					res.append([
					track['title'],
					track['id'],
					cover,
					artist,
					demo,
					track['album']['title']
						])
			if 'next' in resp and len(res)<121:
				searchDeezer(query, len(res) + 1, res)
			if len(res) > 48:
				res.reverse()
			return res
		else:
			return res
	else:
		return res


def searchYoutube(query):
	url = "https://www.googleapis.com/youtube/v3/search"
	querystring = {
		'part': "snippet",
		'q': query,
		'type': "video",
		'key': youtubeApi,
		'maxResults': 50,
		}
	response = requests.request("GET", url, params = querystring)
	res = []
	# print(response.json())
	if response.ok is True:
		resp = response.json()
		if 'pageInfo' in resp and\
			'totalResults' in resp['pageInfo'] and\
			resp['pageInfo']['totalResults'] > 0:
			for i in resp['items']:
				if i['id']['kind'] == "youtube#video":
					res.append([
						i['id']['videoId'],
						i['snippet']['title'],
						i['snippet']['description'],
						i['snippet']['thumbnails']['high']['url'],
						i['snippet']['channelTitle'],
						])
			return res
		else:
			return res
	else:
		return res


# def downloadSoundCloud(url):
# 	response = "https://api.soundcloud.com/resolve?url={}&client_id={}".format(url, soundCloudKey)
# 	r = ur.urlopen(response).read().decode('utf-8')
# 	jdat = json.loads(r)
# 	if jdat['streamable'] is True:
# 		return "{}?client_id={}".format(jdat['stream_url'], soundCloudKey)
# 	else:
# 		return False


# def downloadDeezer(user_id, song_id, quality = None):
# 	link = "https://www.deezer.com/track/{}".format(song_id)
# 	if quality:
# 		quality = "MP3_{}".format(quality)
# 	elif 'quality' in user_steps[user_id] is str:
# 		quality = user_steps[user_id]['quality']
# 	else:
# 		quality = "MP3_320"
# 	audio = dloader.download_trackdee(
# 		link, 
# 		quality=quality, 
# 		recursive_quality=True,
# 		recursive_download=True
# 		)
# 	return audio


async def searchMusic(msg, chat_id, user_id):
	langU = lang[user_steps[user_id]['lang']]
	if 'voice' in msg and (msg.voice.duration < 2 or msg.voice.duration > 60):
		await sendText(chat_id, msg, 1, langU['error_search_voice'])
	elif 'video' in msg and (msg.video.duration < 2 or msg.video.duration > 60):
		await sendText(chat_id, msg, 1, langU['error_search_video'])
	elif 'video_note' in msg and (msg.video_note.duration < 2 or msg.video_note.duration > 60):
		await sendText(chat_id, msg, 1, langU['error_search_videonote'])
	elif 'audio' in msg and (msg.audio.duration < 2 or msg.audio.duration > 60):
		await sendText(chat_id, msg, 1, langU['error_search_audio'])
	else:
		if 'voice' in msg:
			MSG = msg.voice
		elif 'video_note' in msg:
			MSG = msg.video_note
		elif 'video' in msg:
			MSG = msg.video
		elif 'audio' in msg:
			MSG = msg.audio
		if MSG.file_size // 1000000 >= 20:
			await sendText(chat_id, msg, 1, langU['big_file'])
			return False
		with open('Files/search_results.json') as file:
			try:
				saved_datas = eval(file.read() or "{'searchs': {}}")
			except:
				saved_datas = eval("{'searchs': {}}")
		if MSG.file_unique_id in saved_datas['searchs']:
			result = saved_datas['searchs'][MSG.file_unique_id]['result']
			not_saved = False
		else:
			await bot.download_file_by_id(MSG.file_id, "tmp/{}.mp3".format(MSG.file_id))
			req = acr.recognize_by_file('tmp/{}.mp3'.format(MSG.file_id), 0)
			os.remove('tmp/{}.mp3'.format(MSG.file_id))
			result = json.loads(req)
			not_saved = True
		if 'status' in result and 'msg' in result['status'] and result['status']['msg'] == "Success":
			aCr = result['metadata']['music'][0]
			title = (aCr['title'] or langU['not_register'])
			artist = (aCr['artists'][0]['name'] or langU['not_register'])
			album = (aCr['album']['name'] or langU['not_register'])
			if album == title:
				album = langU['single_track']
			if 'release_date' in aCr:
				release_date = aCr['release_date']
				if re.match(r"(\d+)-(\d+)-(\d+)", release_date):
					release_date = release_date.replace('-','/')
					if user_steps[user_id]['lang'] == 'fa':
						ap2 = re_matches("(\d+)/(\d+)/(\d+)", release_date)
						geo = gregorian_to_jalali(int(ap2[1]), int(ap2[2]), int(ap2[3]))
						release_date = "{} - {:04d}/{}/{:02d}".format(release_date, geo[0], echoMonth(geo[1], True), geo[2])
			else:
				release_date = langU['not_register']
			inlineKeys = iMarkup()
			inlineKeys.add(
				iButtun("تنزيل جودة 128📥", callback_data = "dl128kbps:@{}:{}".format(user_id,MSG.file_unique_id)),
				iButtun("تنزيل جودة 320📥", callback_data = "dl320kbps:@{}:{}".format(user_id,MSG.file_unique_id))
				)
	
	          # inlineKeys.add(
				# iButtun(langU['buttuns']['back'], callback_data = "backstart:@{}".format(user_id))
				# )
			user_steps[user_id]['in_wait_dl'].update({
			MSG.file_unique_id: {
			"title": title, 
			'artist': artist, 
			'album': album}
			})
			await sendText(chat_id, msg, 1, \
			"{}".format(langU['search_result'])\
			.format(title, artist, album, release_date, gv().botUser), 'html', inlineKeys)
		else:
			# inlineKeys = iMarkup()
			# inlineKeys.add(
				# iButtun(langU['buttuns']['back'], callback_data = "backstart:@{}".format(user_id))
				# )
			await sendText(chat_id, msg, 1, "{}\n{}".format(langU['not_result'], langU['notice_change_file']))
		if not_saved is True:
			with open('Files/search_results.json', 'w') as file:
				saved_datas['searchs'].update({MSG.file_unique_id: {'time': int(time()), 'result': result}})
				json.dump(saved_datas, file)


def resultFromSoundCloud(msg, chat_id, user_id, query):
	langU = lang[user_steps[user_id]['lang']]
	result = searchSoundCloud(query)
	if len(result) == 0:
		return None
	else:
		deletePreviousData(user_id)
		user_steps[user_id].update({
		"action": "nothing", 
		"quality": "MP3_{}".format(DataBase.get('user.qMusic') or 320), 
		"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)), 
		"sound_cloud": {
		"query": query,
		"link": {},
		"cover": {},
		"title": {},
		"likes": {},
		"created_at": {},
		}})
		inlineKeys = iMarkup()
		i = 0
		for song in result:
			title, link, cover, created_at, likes = song
			isDup = isNotDuplicate2(user_id, title)
			if isDup:
				if cover:
					cover_music = cover.replace('large', 't500x500')
				else:
					cover_music = 'Files/cover2.jpg'
				user_steps[user_id]['sound_cloud']['cover'][i] = cover_music
				user_steps[user_id]['sound_cloud']['link'][i] = link
				user_steps[user_id]['sound_cloud']['likes'][i] = likes
				user_steps[user_id]['sound_cloud']['created_at'][i] = created_at
				if isDup is str:
					user_steps[user_id]['sound_cloud']['title'][i] = isDup
				else:
					user_steps[user_id]['sound_cloud']['title'][i] = title
				if i < 15:
					inlineKeys.add(
						iButtun(title, callback_data = 'dlsong2:@{}:{}'.format(user_id, i))
						)
				if i == 15:
					inlineKeys.add(
					# iButtun(langU['buttuns']['back'], callback_data='backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data='dlmusic2:@{}:{}'.format(user_id, i - 1)),
					)
				i += 1
		return inlineKeys, 1, len(user_steps[user_id]['sound_cloud']['title'])//15 + 1


async def downloadMusic(msg, chat_id, user_id, query):
	langU = lang[user_steps[user_id]['lang']]
	result = searchSoundCloud(query)
	# print(query)
	if len(result) == 0:
		sendM = await sendText(chat_id, msg, 1, "{}\n{}".format(langU['not_result'], langU['let_me']))
		await asyncio.sleep(0.5)
		result = searchDeezer(query, None, [])
		if len(result) == 0:
			await editText(chat_id, sendM[1].message_id, 0, langU['not_result'])
		else:
			set_stats('+', 'search_music')
			deletePreviousData(user_id)
			user_steps[user_id].update({
			"action": "search_music", 
			"quality": "MP3_{}".format(DataBase.get('user.qMusic') or 320), 
			"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)), 
			"deezer": {
			"query": query, 
			"link": {}, 
			"cover": {}, 
			"title": {}, 
			"artist": {}, 
			"demo": {}, 
			"album": {}
			}})
			inlineKeys = iMarkup()
			i = 0
			for song in result:
				title, link, cover, artist, demo, album = song
				isDup = isNotDuplicate(user_id,"{} - {}".format(artist, title))
				if isDup:
					if cover:
						cover_music = cover.replace('large', 't500x500')
					else:
						cover_music = 'Files/cover2.jpg'
					user_steps[user_id]['deezer']['cover'][i] = cover_music
					user_steps[user_id]['deezer']['link'][i] = link
					user_steps[user_id]['deezer']['artist'][i] = artist
					user_steps[user_id]['deezer']['demo'][i] = demo
					user_steps[user_id]['deezer']['album'][i] = album
					if isDup is str:
						user_steps[user_id]['deezer']['title'][i] = isDup
					else:
						user_steps[user_id]['deezer']['title'][i] = title
					if i < 15:
						inlineKeys.add(
							iButtun("{} - {}".format(artist, title), callback_data = 'dlsong:@{}:{}:{}'.format(user_id, i, link))
							)
					if i == 15:
						inlineKeys.add(
							# iButtun(langU['buttuns']['back'], callback_data='backstart:@{}'.format(user_id)),
							iButtun(langU['buttuns']['next_page'], callback_data='dlmusic:@{}:{}'.format(user_id, i + 1)),
							)
					i += 1
			await editText(chat_id, sendM[1].message_id, 0, langU['look_finds'].format(1, len(user_steps[user_id]['deezer']['title'])//15 + 1), None, inlineKeys)
	else:
		# print(2)
		# print(result)
		set_stats('+', 'search_music')
		deletePreviousData(user_id)
		user_steps[user_id].update({
		"action": "search_music", 
		"quality": "MP3_{}".format(DataBase.get('user.qMusic') or 320), 
		"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)), 
		"sound_cloud": {
		"query": query,
		"link": {},
		"cover": {},
		"title": {},
		"likes": {},
		"created_at": {},
		}})
		inlineKeys = iMarkup()
		i = 0
		for song in result:
			title, link, cover, created_at, likes = song
			isDup = isNotDuplicate2(user_id, title)
			if isDup:
				if cover:
					cover_music = cover.replace('large', 't500x500')
				else:
					cover_music = 'Files/cover2.jpg'
				user_steps[user_id]['sound_cloud']['cover'][i] = cover_music
				user_steps[user_id]['sound_cloud']['link'][i] = link
				user_steps[user_id]['sound_cloud']['likes'][i] = likes
				user_steps[user_id]['sound_cloud']['created_at'][i] = created_at
				if isDup is str:
					user_steps[user_id]['sound_cloud']['title'][i] = isDup
				else:
					user_steps[user_id]['sound_cloud']['title'][i] = title
				if i < 15:
					inlineKeys.add(
						iButtun(title, callback_data = 'dlsong2:@{}:{}'.format(user_id, i))
						)
				if i == 15:
					inlineKeys.add(
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data = 'dlmusic2:@{}:{}'.format(user_id, i + 1)),
					)
				i += 1
		await sendText(chat_id, msg, 1, langU['look_finds'].format(1, len(user_steps[user_id]['sound_cloud']['title'])//15 + 1), None, inlineKeys)


async def downloadMusic2(chat_id, msg_id, user_id, query, page):
	langU = lang[user_steps[user_id]['lang']]
	inlineKeys = iMarkup()
	if page >= 15:
		preview_page = True
	else:
		preview_page = False
	i = page
	n = 0
	result = user_steps[user_id]['deezer']
	for song in range(page, len(result['title'])):
		inlineKeys.add(
			iButtun("{} - {}".format(result['artist'][song], result['title'][song]), callback_data = 'dlsong:@{}:{}:{}'.format(user_id, song, result['link'][song]))
			)
		if n > 15:
			if preview_page is True:
				preview_page = False
				inlineKeys.add(
					iButtun(langU['buttuns']['preview_page'], callback_data = 'dlmusic:@{}:{}'.format(user_id, page - 16)),
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data = 'dlmusic:@{}:{}'.format(user_id, song)),
						)
				break
			else:
				inlineKeys.add(
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data = 'dlmusic:@{}:{}'.format(user_id, song)),
					)
				break
		n += 1
	if preview_page is True:
		inlineKeys.add(
			iButtun(langU['buttuns']['preview_page'], callback_data = 'dlmusic:@{}:{}'.format(user_id, page - 16)),
			# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
			)
	await editText(chat_id, msg_id, 0, langU['look_finds'].format(page//15 + 1, len(result['title'])//15 + 1), None, inlineKeys)


async def downloadMusic3(chat_id, msg_id, user_id, query, page):
	langU = lang[user_steps[user_id]['lang']]
	inlineKeys = iMarkup()
	if page >= 14:
		preview_page = True
	else:
		preview_page = False
	i = page
	n = 0
	result = user_steps[user_id]['sound_cloud']
	for song in range(page, len(result['title'])):
		callback_data = 'dlsong2:@{}:{}:{}'.format(
			user_id,
			song,
			result['link'][song].replace('https://soundcloud.com/', '')
			)
		if len(callback_data) > 65:
			callback_data = 'dlsong2:@{}:{}'.format(user_id, i)
		inlineKeys.add(
			iButtun(result['title'][song], callback_data = callback_data)
			)
		if n >= 14:
			if preview_page:
				preview_page = False
				inlineKeys.add(
					iButtun(langU['buttuns']['preview_page'], callback_data = 'dlmusic2:@{}:{}'.format(user_id, page - n)),
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data = 'dlmusic2:@{}:{}'.format(user_id, song)),
						)
				break
			else:
				inlineKeys.add(
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data = 'dlmusic2:@{}:{}'.format(user_id, song)),
					)
				break
		n += 1
	if preview_page:
		inlineKeys.add(
			iButtun(langU['buttuns']['preview_page'], callback_data = 'dlmusic2:@{}:{}'.format(user_id, page - n)),
			# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
			)
	await editText(chat_id, msg_id, 0, langU['look_finds'].format(page//14 + 1, len(user_steps[user_id]['sound_cloud']['title'])//14 + 1), None, inlineKeys)


async def searchVideo(msg, chat_id, user_id, query):
	langU = lang[user_steps[user_id]['lang']]
	result = searchYoutube(query)
	if len(result) == 0:
		# inlineKeys = iMarkup()
		# inlineKeys.add(
			# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id))
			# )
		await sendText(chat_id, msg, 1, langU['not_result'], None)#, inlineKeys)
	else:
		set_stats('+', 'search_youtube')
		deletePreviousData(user_id)
		user_steps[user_id].update({
		# "action": "search_video", 
		"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)), 
		"youtube": {
		"query": query,
		"videoId": {}, 
		"title": {}, 
		"descp": {}, 
		"thumb": {}, 
		"chtitle": {}, 
		}})
		DATA = user_steps[user_id]['youtube']
		inlineKeys = iMarkup()
		i = 0
		for video in result:
			videoId, title, descp, thumb, chtitle = video
			DATA['videoId'][i] = videoId
			DATA['title'][i] = title.replace('&quot;', '"')
			DATA['descp'][i] = descp
			DATA['thumb'][i] = thumb
			DATA['chtitle'][i] = chtitle
			if i < 15:
				inlineKeys.add(
					iButtun(title, callback_data = 'dlvideo:@{}:{}:{}'.format(user_id, i, videoId))
					)
			if i == 15:
				inlineKeys.add(iButtun(langU['buttuns']['next_page'], callback_data='findVideo:@{}:{}'.format(user_id, i + 1)))
			i += 1
		await sendText(chat_id, msg, 1, langU['look_finds'].format(1, len(user_steps[user_id]['youtube']['title'])//15 + 1), None, inlineKeys)


async def searchVideo2(chat_id, msg_id, user_id, query, page):
	langU = lang[user_steps[user_id]['lang']]
	inlineKeys = iMarkup()
	if page >= 15:
		preview_page = True
	else:
		preview_page = False
	i = page
	n = 0
	result = user_steps[user_id]['youtube']
	for video in range(page, len(result['title'])):
		inlineKeys.add(
			iButtun(result['title'][video], callback_data = 'dlvideo:@{}:{}:{}'.format(user_id, video, result['videoId'][video]))
			)
		if n > 15:
			if preview_page is True:
				preview_page = False
				inlineKeys.add(
					iButtun(langU['buttuns']['preview_page'], callback_data = 'findVideo:@{}:{}'.format(user_id, page - 16)),
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data = 'findVideo:@{}:{}'.format(user_id, video)),
						)
				break
			else:
				inlineKeys.add(
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					iButtun(langU['buttuns']['next_page'], callback_data = 'findVideo:@{}:{}'.format(user_id, video)),
					)
				break
		n += 1
	if preview_page is True:
		inlineKeys.add(
			iButtun(langU['buttuns']['preview_page'], callback_data = 'findVideo:@{}:{}'.format(user_id, page - 16)),
			# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
			)
	await editText(chat_id, msg_id, 0, langU['look_finds'].format(page//15 + 1, len(result['title'])//15 + 1), None, inlineKeys)


async def dlYoutube(msg, chat_id, user_id, videoId):
	langU = lang[user_steps[user_id]['lang']]
	status = 0 # int(DataBase.get('user.restrictYT:{}'.format(user_id)) or '0')
	if status < 3:
		video_url = 'https://youtube.com/watch?v={}'.format(videoId)
		content = requests.get(video_url)
		text = content.text
		regex = re.search(r"ytplayer.config = (.*);ytplayer.load", text)
		regex = regex.group(1)
		# with open('text2.txt', mode = 'w') as file:
			# file.write(regex)
		# regex = json.loads(regex)
		if 'player_response' in regex:#['args']:
			sendM = await sendText(chat_id, msg, 1, langU['uploading'])
			msg_id = sendM[1].message_id
			if DataBase.sismember('fail_videos', videoId):
				await editText(chat_id, msg_id, 0, langU['tg_50mb'])
				return False
			for num in range(0, 100, 20):
				await asyncio.sleep(0.2)
				num2 = num // 20
				text = "{}% [{}{}]".format(
				num,
				("█" * num2),
				("▒" * (5 - num2))
				)
				await editText(chat_id, msg_id, 0, "{}\n{}".format(langU['uploading'], text), None, None)
			await editText(chat_id, msg_id, 0, "{}\n99% [█████]".format(langU['uploading']), None, None)
			await bot.send_chat_action(chat_id, 'upload_video')
			inlineKeys = iMarkup()
			# inlineKeys.add(
				# iButtun(langU['buttuns']['start_again'], callback_data = 'start_again:@{}'.format(user_id))
				# )
			try:
				video_info = subprocess.Popen([
						'youtube-dl', video_url,
						'--config-location', 'Files/youtube-dl.conf'
					   ], stdout = subprocess.PIPE)
				video_info = video_info.stdout.read()
				if video_info == b'':
					DataBase.sadd('fail_videos', videoId)
					await editText(chat_id, msg_id, 0, langU['tg_50mb'])
				else:
					video_info = json.loads(video_info)
					if type(video_info) is dict:
						if 'upload_date' in video_info:
							ap2 = video_info['upload_date']
							ap2 = (ap2[:4], ap2[4:6], ap2[6:8])
							upload_date = "{}/{}/{}".format(ap2[0], ap2[1], ap2[2])
							if user_steps[user_id]['lang'] == 'fa':
								geo = gregorian_to_jalali(int(ap2[0]), int(ap2[1]), int(ap2[2]))
								upload_date = "{} - {:04d}/{}/{:02d}".format(upload_date, geo[0], echoMonth(geo[1], True), geo[2])
						caption = langU['video_result'].format(
						video_info['title'],
						video_info['webpage_url'],
						video_info['uploader'],
						video_info['channel_url'],
						upload_date,
						video_info['view_count'],
						video_info['like_count'],
						video_info['dislike_count'],
						)
						inlineKeys.add(
							iButtun(langU['buttuns']['convert_mp3'], callback_data = 'conv2mp3:@{}:{}'.format(user_id, videoId)),
							iButtun(langU['buttuns']['convert_vnote'], callback_data = 'conv2vnote:@{}:{}'.format(user_id, videoId)),
							iButtun(langU['buttuns']['convert_ogg'], callback_data = 'conv2ogg:@{}:{}'.format(user_id, videoId)),
							)
						with open("{}.mp4".format(videoId), 'rb') as file:
							if os.path.exists("{}.jpg".format(videoId)):
								cover = open("{}.jpg".format(videoId), 'rb')
							elif os.path.exists("{}.webp".format(videoId)):
								cover = open("{}.webp".format(videoId), 'rb')
							await sendVideo(chat_id, msg, file, caption, "html",\
							video_info['duration'], cover, video_info['width'],\
							video_info['height'], True, 1, inlineKeys)
							try:
								await sendM[1].delete()
							except:
								pass
						try:
							os.system("mv ./{0}.mp4 ./tmp/{0}".format(videoId))
							os.system("rm -rf ./{}.jpg".format(videoId))
							os.system("rm -rf ./{}.webp".format(videoId))
						except Exception as e:
							print(e)
			except:
				await editText(chat_id, msg_id, 0, langU['error_upload_video'], None)#, inlineKeys)
			deletePreviousData(user_id) #
			user_steps[user_id].update({'action': 'nothing'})
		else:
			await sendText(chat_id, msg, 1, langU['send_correct_yt'])
	else:
		await sendText(chat_id, msg, 1, langU['ytRestrcit'])


async def dl4File(r, file_size_dl, block_sz, file, file_size, chat_id, user_id, sendM):
	writer = Writer(file)
	for i in range(0, int(r.headers["content-length"])):
		buffer = r.read(block_sz)
		if not buffer:
			break
		file_size_dl += len(buffer)
		await writer(buffer)
		await file.fsync()
		status = "{}".format(int(file_size_dl * 100 // file_size))
		bar_progress = int(status) // 5
		if user_steps[user_id]['dl']['percent'] != int(status) and user_steps[user_id]['dl']['bar_progress'] != bar_progress:
				user_steps[user_id]['dl']['bar_progress'] = bar_progress
				text = "{}% [{}{}]".format(
				status,
				("█" * bar_progress),
				("▒" * (20 - bar_progress))
				)
				await editText(chat_id, sendM[1].message_id, 0, text)
		user_steps[user_id]['dl']['percent'] = int(status)
	await file.close()
	deletePreviousData(user_id) #


@dp.async_task
async def resize_video(name, ti, chat_id, msg):
	cmd = 'ffmpeg -i tmp/{} -to 60 -strict -2 -vf scale=360:360 -y tmp/{}Vnote.mp4'.format(name, ti)
	# os.system(cmd)
	# cmd = subprocess.Popen([
			# 'ffmpeg', '-i', 'tmp/{}'.format(name), '-to', '60', '-strict', '-2', '-vf',
			# 'scale=360:360', '-y', 'tmp/{}Vnote.mp4'.format(name)
		   # ], stdout = subprocess.PIPE)
	# cmd = cmd.stdout.read()
	proc = await asyncio.create_subprocess_shell(
		cmd,
		stdout = asyncio.subprocess.PIPE,
		stderr = asyncio.subprocess.PIPE)
	stdout, stderr = await proc.communicate()
	print(f'[{cmd!r} exited with {proc.returncode}]')
	if stdout:
		print(f'[stdout]\n{stdout.decode()}')
	if stderr:
		print(f'[stderr]\n{stderr.decode()}')
	await sendVideoNote(chat_id, msg, types.InputFile('tmp/{}Vnote.mp4'.format(ti)))


@dp.async_task
async def dlFromInstagram(msg, chat_id, user_id, url, type_ig):
	langU = lang[user_steps[user_id]['lang']]
	msg_id = msg.message_id
	sendM = await sendText(chat_id, msg, 1, langU['uploading'])
	if type_ig == 'post':
		try:
			if DataBase.get('maybeSpammer:{}:{}'.format(user_id, url)):
				await editText(chat_id, sendM[1].message_id, 0, langU['maybe_spammer'])
			elif DataBase.get('igPrivateAccount:{}:{}'.format(user_id, url)):
				await editText(chat_id, sendM[1].message_id, 0, langU['ig_is_private'])
			else:
				post = instaloader.Post.from_shortcode(igloader.context, url)
				# post.owner_profile, post.owner_username, post.owner_id, post.date_local,\
				# post.caption, post.is_video, post.video_view_count, post.video_duration, post.likes, post.comments,\
				# post.location
				if post.owner_profile.is_private:
					DataBase.setex('igPrivateAccount:{}:{}'.format(user_id, url), 3600, "True")
				else:
					if post.typename == "GraphSidecar":
						sides = post.get_sidecar_nodes()
						media = []
						Powner = post.owner_username
						Pcaption = post.caption
						Plike = post.likes
						Pcomment = post.comments
						count = 0
						for i in sides:
							count += 1
							if i.is_video:
								caption = langU['ig_caption_video'].format(
									Powner,
									url,
									Pcaption,
									"x",
									Plike,
									Pcomment,
									gv().botID,
									gv().botName)
								meDia = InputMediaVideo(
									i.video_url,
									i.display_url,
									caption,
									512, 512,
									15,
									'html',
									True)
							else:
								caption = langU['ig_caption_pic'].format(
									Powner,
									url,
									Pcaption,
									Plike,
									Pcomment,
									gv().botID,
									gv().botName)
								meDia = InputMediaPhoto(
									i.display_url,
									None,
									caption,
									'html')
							media.append(meDia)
						if count > 1:
							DataBase.setex('maybeSpammer:{}:{}'.format(user_id, url), 3600, "True")
							set_stats('++', 'dl_ig_post', count)
							await sendMediaGroup(chat_id, msg, 1, media)
							del media
							try:
								await sendM[1].delete()
							except:
								pass
					else:
						set_stats('+', 'dl_ig_post')
						igloader.download_post(post, None)
						if post.is_video:
							caption = langU['ig_caption_video'].format(
								post.owner_username,
								url,
								post.caption,
								post.video_view_count,
								post.likes,
								post.comments,
								gv().botID,
								gv().botName)
							inlineKeys = iMarkup()
							inlineKeys.add(
								iButtun(langU['buttuns']['convert_mp3'], callback_data = 'conv2mp3:@{}:{}'.format(user_id, url)),
								# iButtun(langU['buttuns']['convert_vnote'], callback_data = 'conv2vnote:@{}:{}'.format(user_id, url)),
								iButtun(langU['buttuns']['convert_ogg'], callback_data = 'conv2ogg:@{}:{}'.format(user_id, url)),
								)
							await sendVideo(chat_id, msg, post.video_url, caption, 'html', supports_streaming = True, reply_markup = inlineKeys)
							try:
								os.system('mv ./Instagram/{0}.mp4 ./tmp/{0}'.format(url))
							except Exception as e:
								print(e)
							try:
								await sendM[1].delete()
							except:
								pass
						else:
							caption = langU['ig_caption_pic'].format(
								post.owner_username,
								url,
								post.caption,
								post.likes,
								post.comments,
								gv().botID,
								gv().botName)
							await sendPhoto(chat_id, post.url, caption, 'html', msg)
						try:
							await sendM[1].delete()
						except:
							pass
		except:
			await editText(chat_id, sendM[1].message_id, 0, langU['ig_is_private'])
	elif type_ig == 'user':
		# InputMediaVideo(media, thumb, caption, parse_mode, width, height, duration, supports_streaming)
		# InputMediaPhoto(media, caption, parse_mode)
		owner_username = url
		if DataBase.get('igPrivateAccount:{}'.format(owner_username)):
			await editText(chat_id, sendM[1].message_id, 0, langU['ig_is_private'])
		elif DataBase.get('maybeSpammer:{}:{}'.format(user_id, owner_username)):
			await editText(chat_id, sendM[1].message_id, 0, langU['maybe_spammer'])
		else:
			profile = instaloader.Profile.from_username(igloader.context, owner_username)
			if profile.is_private and not profile.has_public_story:
				DataBase.setex('igPrivateAccount:{}'.format(owner_username), 3600, "True")
				await editText(chat_id, sendM[1].message_id, 0, langU['ig_is_private'])
			else:
				# item.mediaid, item.shortcode, item.owner_username, item.owner_id,
				# item.date, item.expiring_local, item.expiring_utc, item.url, item.date_utc
				# item.typename, item.is_video, item.video_url, item.date_local
				media = {}
				file_to_delete = []
				count = 0
				for story in igloader.get_stories([profile.userid]):
					await editText(chat_id, sendM[1].message_id, 0, langU['find_story_count'].format(story.itemcount, owner_username, profile.full_name), 'html')
					for item in story.get_items():
						count += 1
						igloader.download_storyitem(item, None)
						if item.is_video:
							caption = langU['ig_caption_svideo'].format(
								owner_username,
								owner_username,
								item.mediaid,
								gv().botID,
								gv().botName)
							meDia = InputMediaVideo(
								types.InputFile("Instagram/{}.mp4".format(item.shortcode)),
								types.InputFile("Instagram/{}.jpg".format(item.shortcode)),
								caption,
								512, 512,
								15,
								'html',
								True)
							file_to_delete.append("{}.mp4".format(item.shortcode))
							file_to_delete.append("{}.jpg".format(item.shortcode))
						else:
							caption = langU['ig_caption_spic'].format(
								owner_username,
								owner_username,
								item.mediaid,
								gv().botID,
								gv().botName)
							meDia = InputMediaPhoto(
								types.InputFile("Instagram/{}.jpg".format(item.shortcode)),
								None,
								caption,
								'html')
							file_to_delete.append("{}.jpg".format(item.shortcode))
						if not count//10 in media:
							media.update({count//10: []})
						media[count//10].append(meDia)
				set_stats('++', 'dl_ig_story', count)
				if count > 1:
					DataBase.setex('maybeSpammer:{}:{}'.format(user_id, owner_username), 3600, "True")
					try:
						await sendM[1].delete()
					except:
						pass
					for i in range(0, len(media)):
						await asyncio.sleep(0.1)
						await sendMediaGroup(chat_id, msg, 1, media[i])
					for i in file_to_delete:
						os.system('rm Instagram/{}'.format(i))
					del file_to_delete
					del media
				else:
					await editText(chat_id, sendM[1].message_id, 0, langU['ig_not_any_story'])
	elif type_ig == 'story':
		url = url.split('/')
		owner_username = url[0]
		media_id = int(url[1])
		if DataBase.get('igPrivateStory:{}'.format(media_id)):
			await editText(chat_id, sendM[1].message_id, 0, langU['ig_is_private'])
		elif DataBase.get('maybeSpammer:{}:{}'.format(user_id, media_id)):
			await editText(chat_id, sendM[1].message_id, 0, langU['maybe_spammer'])
		else:
			profile = instaloader.Profile.from_username(igloader.context, owner_username)
			if profile.is_private and not profile.has_public_story:
				DataBase.setex('igPrivateStory:{}'.format(media_id), 3600, "True")
				await editText(chat_id, sendM[1].message_id, 0, langU['ig_is_private'])
			else:
				item = None
				for story in igloader.get_stories([profile.userid]):
					for item in story.get_items():	
						if item.mediaid == media_id:
							item = item
							break
				# item.mediaid, item.shortcode, item.owner_username, item.owner_id,
				# item.date, item.expiring_local, item.expiring_utc, item.url, item.date_utc
				# item.typename, item.is_video, item.video_url, item.date_local
				if item:
					set_stats('+', 'dl_ig_story')
					if item.is_video:
						shortcode = item.shortcode
						igloader.download_storyitem(item, None)
						caption = langU['ig_caption_svideo'].format(
						owner_username,
						owner_username,
						media_id,
						gv().botID,
						gv().botName)
						DataBase.setex('maybeSpammer:{}:{}'.format(user_id, media_id), 3600, "True")
						inlineKeys = iMarkup()
						inlineKeys.add(
							iButtun(langU['buttuns']['convert_mp3'], callback_data = 'conv2mp3:@{}:{}'.format(user_id, shortcode)),
							# iButtun(langU['buttuns']['convert_vnote'], callback_data = 'conv2vnote:@{}:{}'.format(user_id, shortcode)),
							iButtun(langU['buttuns']['convert_ogg'], callback_data = 'conv2ogg:@{}:{}'.format(user_id, shortcode)),
							)
						await sendVideo(chat_id, msg, item.video_url, caption, 'html', supports_streaming = True, reply_markup = inlineKeys)
						try:
							os.system('mv ./Instagram/{0}.mp4 ./tmp/{0}'.format(shortcode))
						except Exception as e:
							print(e)
					else:
						caption = langU['ig_caption_spic'].format(
						owner_username,
						owner_username,
						media_id,
						gv().botID,
						gv().botName)
						DataBase.setex('maybeSpammer:{}:{}'.format(user_id, media_id), 3600, "True")
						await sendPhoto(chat_id, item.url, caption, 'html', msg)
					try:
						await sendM[1].delete()
					except:
						pass
				else:
					await editText(chat_id, sendM[1].message_id, 0, langU['ig_not_story'])
	elif type_ig == 'highlight':
		pass


@dp.async_task
async def dlFile(msg, chat_id, user_id, file_url, file_name = None):
	langU = lang[user_steps[user_id]['lang']]
	if isUserSteps(user_id) and 'dl' in user_steps[user_id] and user_steps[user_id]['dl']['downloading']:
		await sendText(chat_id, user_steps[user_id]['dl']['downloading'], 1, langU['you_now_dl'])
	else:
		file_name = (file_name or file_url).split('/')[-1]
		file_name = file_name.split('?')[0]
		http = urllib3.PoolManager()
		try:
			r = http.request('GET', file_url, preload_content = False)
			if 'content-length' in r.headers:
				if int(r.headers["content-length"]) // 1048576 < 50:
					file_size = int(r.headers["content-length"])
					sendM = await sendText(chat_id, msg, 1, langU['file_size'].format(file_name, file_size // 1048576))
					file_size_dl = 0
					block_sz = 4096
					file = await AIOFile("Downloads/{}".format(file_name), "wb+")
					user_steps[user_id].update({"dl":{
					"percent": 0,
					"bar_progress": 0,
					"downloading": sendM[1],
					}})
					await dl4File(r, file_size_dl, block_sz, file, file_size, chat_id, user_id, sendM)
					user_steps[user_id].update({"action": 'nothing'})
					await editText(chat_id, sendM[1].message_id, 0, langU['file_dled'])
					with open("Downloads/{}".format(file_name), "rb") as file:
						await sendDocument(chat_id, file, "@{}".format(gv().botUser), reply_msg = msg)
					set_stats('+', 'dl_file')
					os.system("rm -rf ./Downloads/{}".format(file_name))
				else:
					await sendText(chat_id, msg, 1, langU['big_file2']) 
			else:
				await sendText(chat_id, msg, 1, langU['send_file_url'])
		except:
			await sendText(chat_id, msg, 1, langU['send_file_url'])


async def message_process(msg: types.Message):
	if int(msg.date.timestamp())  <  (int(time())-60):
		cPrint("{} Old Message Skipped".format(msg.date), 2, textColor = "cyan")
		return False
	data = CheckMsg(msg)
	chat_id = int(msg.chat.id)
	content = data.content
	user_id = int(msg.from_user.id)
	msg_id = msg.message_id
	setupUserSteps(msg, user_id)
	langU = lang[user_steps[user_id]['lang']]
	print(colored("Message:", "yellow"),
	colored("ID: {} | Type: {}".format(msg.from_user.id, content), "white"))
	if 'reply_to_message' in msg:
		reply_msg = msg.reply_to_message
		reply_id = reply_msg.message_id
	else:
		reply_msg = None
		reply_id = 0
	if 'forward_from' in msg and msg.forward_from.id:
		saveUsername(msg)
	else:
		saveUsername(msg)
	if not DataBase.get('checkBotInfo'):
		try:
			b = await bot.get_me()
			DataBase.hset(db, 'user', b.username)
			DataBase.hset(db, 'id', b.id)
			DataBase.hset(db, 'name', b.first_name)
			DataBase.hset(db, 'token', telegram_datas['botToken'])
			getC = await bot.get_chat(sudo_id)
			DataBase.hset('sudo', 'user', getC.id)
			if getC.username:
				DataBase.hset('sudo', 'user', getC.username)
			DataBase.setex('checkBotInfo', 86400, "True")
		except:
			print("Sudo or Channel Not Found!!!")
			pass
	# if isPv(msg):
		# setupUserSteps(msg, user_id)
		# await memberCommands(msg, "input", chat_id, False, False)
	if isSuper(msg):
		if chat_id == gv().supchat:
			if isSudo(user_id):
				IF = reply_msg and reply_msg.from_user.id == gv().botID
				if IF and reply_msg.text and 'text' in msg:
					IF2 = reply_msg.text.split(' | ')
					sendM = await sendText(IF2[1], 0, 1, msg.text, 'html')
					if sendM[0] is True:
						await sendText(chat_id, msg, 1, "✅")
					else:
						await sendText(chat_id, msg, 1, "❌\n{}".format(sendM))
		if 'text' in msg:
			input = msg.text.lower()
			input2 = msg.text
			if re.match(r'^#vardump$', input) and isSudo(user_id):
				print(msg)
			if re.match(r'^test$', input) and isSudo(user_id):
				with open("1", 'rb') as file:
					inlineKeys = iMarkup()
					inlineKeys.add(
						iButtun('to video note', callback_data = 'tovnote:@{}'.format(user_id))
					)
					await sendVideo(chat_id, msg, file, None, "html",\
					30, None, 512,\
					512, True, 1, inlineKeys)
			if re.match(r'^تفعيل اليوتيوب$', input) or re.match(r'^install$', input) or re.match(r'^تفعيل الاغاني$', input):
				if DataBase.sismember('botGroups', chat_id):
					if isMod(chat_id, user_id):
						text = langU['gp_added']
						await sendText(chat_id, msg, 1, text)
				else:
					DataBase.sadd('botGroups', chat_id)
					LiSt = await bot.get_chat_administrators(chat_id)
					for i in LiSt:
						DataBase.sadd('group.mods:{}'.format(chat_id), i.user.id)
					text = langU['gp_add']
					await sendText(chat_id, msg, 1, text)
			if re.match(r'^تعطيل اليوتيوب$', input) or re.match(r'^uninstall$', input) or re.match(r'^تعطيل الاغاني$', input):
				if DataBase.sismember('botGroups', chat_id):
					if isMod(chat_id, user_id):
						DataBase.srem('botGroups', chat_id)
						keys = DataBase.keys('*{}*'.format(chat_id))
						redis.delete(*keys)
						text = langU['gp_remove']
						await sendText(chat_id, msg, 1, text)
				else:
					text = langU['gp_removed']
					await sendText(chat_id, msg, 1, text)
		if DataBase.sismember('botGroups', chat_id):
			setupUserSteps(msg, user_id)
			await memberCommands(msg, "input", chat_id, True, False)
		# else:
			# if not DataBase.get('botGroups.ttleft'):
				# DataBase.setex('botGroups.ttleft', 130, 'true')
				# await asyncio.sleep(120)
				# if not DataBase.sismember('botGroups', chat_id):
					# await bot.leave_chat(chat_id)
	if isGroup(msg):
		try:
			await bot.leave_chat(chat_id)
		except:
			pass


@dp.async_task
async def callback_query_process(msg: types.CallbackQuery):
	saveUsername(msg, mode = "callback")
	user_id = msg.from_user.id
	input = msg.data.lower()
	setupUserSteps(msg, user_id)
	langU = lang[user_steps[user_id]['lang']]
	if 'message' in msg:
		chat_id = msg.message.chat.id
		msg_id = msg.message.message_id
	else:
		msg_id = 0
	print(colored("Callback Query:", "yellow"),
	colored("ID: {} | Query: {}".format(user_id, input), "white")
	)
	if re.search(r"@(\d+)", input):
		ap = re_matches("@(\d+)", input, 's')
		if int(ap[1]) != user_id:
			if not DataBase.get('user.alertinline:{}:{}'.format(user_id, msg_id)):
				DataBase.setex('user.alertinline:{}:{}'.format(user_id, msg_id), 3600, "True")
				return AnswerCallbackQuery(msg.id, langU['isNot4u'], True, None, 3600)
			return False
		if int(ap[1]) == user_id and not DataBase.get('user.alertNotMemberChannel:{}'.format(user_id)):
			print(3)
			if not re.search(r'insgp(.*)', input) and not re.search(r'ib(.*)', input) and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
				DataBase.set('user.alertNotMemberChannel2:{}'.format(user_id), "True")
				await answerCallbackQuery(msg, langU['uNotJoined'].format(IDs_datas['chUsername']), True)
				inlineKeys = iMarkup()
				inlineKeys.add = (
				iButtun(langU['buttuns']['join'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),
				iButtun(langU['buttuns']['joined'], callback_data = input)
				)
				await editText(chat_id, msg_id, 0, langU['join_channel'].format(IDs_datas['chUsername']), 'md', inlineKeys)
				return False
			if DataBase.get('user.alertNotMemberChannel2:{}'.format(user_id)):
				DataBase.delete('user.alertNotMemberChannel2:{}'.format(user_id))
				await answerCallbackQuery(msg, langU['you_accepted'])
			DataBase.setex('user.alertNotMemberChannel:{}'.format(user_id), 3600, "True")
	if 'message' in msg:
		DataBase.incr('amarBot.callmsg')
		_ = msg.message
		msg_id = _.message_id
		chat_id = _.chat.id
		chat_name = _.chat.title
		if not redis.get(input):
			redis.psetex(input, 500, 1)
		else:
			return False
		if int(_.date.timestamp()) < (int(time())-86400):
			cPrint("{} Old Callback Skipped".format(_.date), 2, textColor = "cyan")
			try:
				await _.edit_reply_markup()
			except:
				pass
			return AnswerCallbackQuery(msg.id, "عزيزي هذه الامر قديم!\nاستخدم البوت مره ثانيه :D", True)
		if re.match(r"^findmusic:@(\d+)$", input):
			user_steps[user_id].update({"action": "search_music"})
			# inlineKeys = iMarkup()
			# inlineKeys.add(
				# iButtun(langU['buttuns']['back'],callback_data = 'backstart:@{}'.format(user_id))
				# )
			await editText(chat_id, msg_id, 0, langU['send_voice'], None)#, inlineKeys)
		if re.match(r"^backstart:@(\d+)$", input):
			DataBase.delete('sup:{}'.format(user_id))
			user_steps[user_id].update({"action": "nothing"})
			deletePreviousData(user_id)
			await editText(chat_id, msg_id, 0, langU['start'], None, start_keys(user_id))
		if re.match(r"^dlmusic:@(\d+):(\d+)$", input):
			ap = re_matches("^dlmusic:@(\d+):(\d+)$", input)
			if isUserSteps(user_id) and 'deezer' in user_steps[user_id]:
				await downloadMusic2(chat_id, msg_id, user_id, user_steps[user_id]['deezer']['query'], int(ap[2]))
			else:
				await editText(chat_id, msg_id, 0, langU['try_request'], None, None)
		if re.match(r"^dlmusic2:@(\d+):(\d+)$", input):
			ap = re_matches("^dlmusic2:@(\d+):(\d+)$", input)
			if isUserSteps(user_id) and 'sound_cloud' in user_steps[user_id]:
				await downloadMusic3(chat_id, msg_id, user_id, user_steps[user_id]['sound_cloud']['query'], int(ap[2]))
			else:
				await editText(chat_id, msg_id, 0, langU['try_request'], None, None)
		if re.match(r"^dlsong:@(\d+):(\d+):(\d+)$", input):
			ap = re_matches("^dlsong:@(\d+):(\d+):(\d+)$", input)
			if isUserSteps(user_id) and 'deezer' in user_steps[user_id]:
				try:
					await _.delete()
				except:
					try:
						await _.edit_reply_markup()
					except:
						pass
				i = int(ap[2])
				link = user_steps[user_id]['deezer']['link'][i]
				cover = user_steps[user_id]['deezer']['cover'][i]
				title = user_steps[user_id]['deezer']['title'][i]
				artist = user_steps[user_id]['deezer']['artist'][i]
				album = user_steps[user_id]['deezer']['album'][i]
				demo = user_steps[user_id]['deezer']['demo'][i]
				file_address = downloadFromYT(user_id, link, ap[1])

				req = request("https://api.deezer.com/track/{}".format(link), chat_id, True, langU)
				if req:
					release_date = req.json()
					release_date = release_date['album']['release_date'].replace("-", "/")
				else:
					release_date = ''
				if user_steps[user_id]['lang'] == 'fa':
					ap2 = re_matches("(\d+)/(\d+)/(\d+)", release_date)
					geo = gregorian_to_jalali(int(ap2[1]), int(ap2[2]), int(ap2[3]))
					release_date = "{} - {:04d}/{}/{:02d}".format(release_date, geo[0], echoMonth(geo[1], True), geo[2])
				if title == album:
					album = langU['single_track']
				if not cover is None:
					caption = langU['download_result'].format(artist, title, album, release_date)
					await sendPhoto(chat_id, cover, caption, 'html', _.reply_to_message)
				if not demo is None:
					voice = ur.urlretrieve(demo, 'tmp/{}.ogg'.format(link))
					with open(voice[0], 'rb') as file:
						await sendVoice(chat_id, _.reply_to_message, file, duration = 30)
					os.remove(voice[0])
				with open(file_address, mode = 'rb') as file:
					# inlineKeys = iMarkup()
					# inlineKeys.add(
						# iButtun(langU['buttuns']['start_again'], callback_data = 'start_again:@{}'.format(user_id))
						# )
					caption = "{}Kbps | @{} | @{}".format(user_steps[user_id]['quality'].replace('MP3_',''), gv().botUser, IDs_datas['chUsername'])
					await sendAudio(chat_id, _.reply_to_message, file, None, performer = artist, title = "{} - @{}".format(title, gv().botUser))#, reply_markup = inlineKeys)
				set_stats('+', 'dl_music')
				os.remove(file_address)
				user_steps[user_id].update({'action': 'nothing'})
				deletePreviousData(user_id)
			else:
				await editText(chat_id, msg_id, 0, langU['try_again'], None, None)
		if re.match(r"^dlsong2:@(\d+):(\d+):(.*)$", input) or re.match(r"^dlsong2:@(\d+):(\d+)$", input):
			ap = re_matches("^dlsong2:@(\d+):(\d+):(.*)$", input) or \
			re_matches("^dlsong2:@(\d+):(\d+)$", input)
			if isUserSteps(user_id) and 'sound_cloud' in user_steps[user_id]:
				try:
					await _.delete()
				except:
					try:
						await _.edit_reply_markup()
					except:
						pass
				i = int(ap[2])
				link = user_steps[user_id]['sound_cloud']['link'][i]
				cover = user_steps[user_id]['sound_cloud']['cover'][i]
				title = user_steps[user_id]['sound_cloud']['title'][i]
				likes = user_steps[user_id]['sound_cloud']['likes'][i]
				created_at = user_steps[user_id]['sound_cloud']['created_at'][i]
				created_at = created_at.split(" ")[0]
				file = downloadSoundCloud(link)
				if not file is False:
					# if not cover is None:
						# caption = langU['download_result2'].format(title)
						# await sendPhoto(chat_id, cover, caption, 'html')
					# inlineKeys = iMarkup()
					# inlineKeys.add(
						# iButtun(langU['buttuns']['start_again'], callback_data = 'start_again:@{}'.format(user_id))
						# )
					if user_steps[user_id]['lang'] == 'fa':
						ap2 = re_matches("^(\d+)/(\d+)/(\d+)$", created_at)
						geo = gregorian_to_jalali(int(ap2[1]), int(ap2[2]), int(ap2[3]))
						created_at = "{} - {:04d}/{}/{:02d}".format(created_at, geo[0], echoMonth(geo[1], True), geo[2])
					caption = langU['caption_sc'].format(title, created_at, likes, gv().botUser, IDs_datas['chUsername'])
					await sendAudio(chat_id, _.reply_to_message, file, None, performer = gv().botUser, title = title)#, reply_markup = inlineKeys)
					set_stats('+', 'dl_music')
					user_steps[user_id].update({'action': 'nothing'})
				else:
					await sendText(chat_id, _.reply_to_message, 1, langU['keep_license'])
				deletePreviousData(user_id)
			else:
				await editText(chat_id, msg_id, 0, langU['try_again'], None, None)
		if re.match(r"^settings:@(\d+)$", input):
			await editText(chat_id, msg_id, 0, langU['settings'], None, settings_keys(user_id))
		if re.match(r"^set_(.*)_(.*):@(\d+)$", input):
			ap = re_matches("^set_(.*)_(.*):@(\d+)$", input)
			if ap[1] == 'lang':
				DataBase.set('user.lang:{}'.format(user_id),ap[2])
				try:
					await editText(chat_id, msg_id, 0, lang[ap[2]]['settings'], None, settings_keys(user_id, ap[2]))
				except:
					await _.edit_reply_markup(settings_keys(user_id, ap[2]))
				return AnswerCallbackQuery(msg.id, lang['set_{}'.format(ap[2])], True, None, 0)
			if ap[1] == 'qmusic':
				DataBase.set('user.qMusic',ap[2])
				try:
					await editText(chat_id, msg_id, 0, langU['settings'], None, settings_keys(user_id, None, "MP3_{}".format(ap[2])))
				except:
					await _.edit_reply_markup(settings_keys(user_id, None, "MP3_{}".format(ap[2])))
				return AnswerCallbackQuery(msg.id, langU['set_qmusic'].format(ap[2]), True, None, 0)
		if re.match(r"^notice_1:@(\d+)$", input):
			return AnswerCallbackQuery(msg.id, langU['notice_change_file'], True, None, 86400)
		if re.match(r"^dl(\d+)kbps:@(\d+):(.*)$", msg.data):
			ap = re_matches("^dl(\d+)kbps:@(\d+):(.*)$", msg.data)
			try:
				await _.edit_reply_markup()
			except:
				pass
			if isUserSteps(user_id) and 'in_wait_dl' in user_steps[user_id] and ap[3] in user_steps[user_id]['in_wait_dl']:
				await answerCallbackQuery(msg, langU['downloading'], False, 10)
				want_dl = user_steps[user_id]['in_wait_dl'][ap[3]]
				result = searchDeezer("{} {}".format(want_dl['artist'], want_dl['title']), None, [])
				if len(result) == 0:
					result = searchDeezer(want_dl['title'], None, [])
					if len(result) == 0:
						result = searchDeezer(want_dl['title'][:len(want_dl['title'])-(len(want_dl['title'])//2)], None, [])
						if len(result) == 0:
							return AnswerCallbackQuery(msg.id, langU['try_again'], True, None, 86400)
				title, link, cover, artist, demo, album = result[0]
				file_address = downloadFromYT(user_id, link, ap[1])
				req = request("https://api.deezer.com/track/{}".format(link), chat_id, True, langU)
				if req:
					release_date = req.json()
					release_date = release_date['album']['release_date'].replace("-", "/")
				else: # programmer | creator > @EIKOei
					release_date = ''
				if user_steps[user_id]['lang'] == 'fa':
					ap2 = re_matches("(\d+)/(\d+)/(\d+)", release_date)
					geo = gregorian_to_jalali(int(ap2[1]), int(ap2[2]), int(ap2[3]))
					release_date = "{} - {:04d}/{}/{:02d}".format(release_date, geo[0], echoMonth(geo[1], True), geo[2])
				if title == album:
					album = langU['single_track']
				if cover:
					caption = langU['download_result'].format(artist, title, album, release_date)
					await sendPhoto(chat_id, cover, caption, 'html', _.reply_to_message)
				if demo:
					voice = ur.urlretrieve(demo, 'tmp/{}.ogg'.format(link))
					with open(voice[0], 'rb') as file:
						await sendVoice(chat_id, _.reply_to_message, file, duration = 30)
					os.remove(voice[0])
				with open(file_address, mode = 'rb') as file:
					# inlineKeys = iMarkup()
					# inlineKeys.add(
						# iButtun(langU['buttuns']['start_again'], callback_data = 'start_again:@{}'.format(user_id))
						# )
					caption = None
					await sendAudio(chat_id, _.reply_to_message, file, None, performer = artist, title = "{} - @{}".format(title, gv().botUser))#, reply_markup = inlineKeys)
				set_stats('+', 'dl_music')
				os.remove(file_address)
				deletePreviousData(user_id) #
				user_steps[user_id].update({'action': 'nothing'})
			else:
				try:
					await _.edit_reply_markup()
				except:
					pass
				return AnswerCallbackQuery(msg.id, langU['try_again'], True, None, 86400)
		if re.match(r"^start_again:@(\d+)$", input):
			DataBase.delete('sup:{}'.format(user_id))
			user_steps[user_id].update({"action": "nothing"})
			deletePreviousData(user_id)
			try:
				await _.edit_reply_markup()
			except:
				pass
			await sendText(chat_id, 0, 1, langU['start'], None, start_keys(user_id))
		if re.match(r"^findvideo:@(\d+)$", input):
			ap = re_matches("^findvideo:@(\d+)$", input)
			# inlineKeys = iMarkup()
			# inlineKeys.add(
				# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
			# )
			user_steps[user_id].update({'action': "search_video"})
			await editText(chat_id, msg_id, 0, langU['send_text4video'], None)#, inlineKeys)
		if re.match(r"^findvideo:@(\d+):(\d+)$", input):
			ap = re_matches("^findvideo:@(\d+):(\d+)$", input)
			if isUserSteps(user_id) and 'youtube' in user_steps[user_id]:
				await searchVideo2(chat_id, msg_id, user_id, user_steps[user_id]['youtube']['query'], int(ap[2]))
			else:
				await editText(chat_id, msg_id, 0, langU['try_request'], None, None)
		if re.match(r"^dlvideo:@(\d+):(\d+):(.*)$", msg.data):
			ap = re_matches("^dlvideo:@(\d+):(\d+):(.*)$", msg.data)
			if isUserSteps(user_id) and 'youtube' in user_steps[user_id]:
				i = int(ap[2])
				DATA = user_steps[user_id]['youtube']
				videoId = DATA['videoId'][i]
				title = DATA['title'][i]
				desc = DATA['descp'][i]
				thumb = DATA['thumb'][i]
				chtitle = DATA['chtitle'][i]
				await editText(chat_id, msg_id, 0, langU['uploading'], None, None)
				if DataBase.sismember('fail_videos', videoId):
					await editText(chat_id, msg_id, 0, langU['tg_50mb'])
					return False
				for num in range(0, 100, 20):
					await asyncio.sleep(0.2)
					num2 = num // 20
					text = "{}% [{}{}]".format(
					num,
					("█" * num2),
					("▒" * (5 - num2))
					)
					await editText(chat_id, msg_id, 0, "{}\n{}".format(langU['uploading'], text), None, None)
				await editText(chat_id, msg_id, 0, "{}\n99% [█████]".format(langU['uploading']), None, None)
				await bot.send_chat_action(chat_id, 'upload_video')
				inlineKeys = iMarkup()
				# inlineKeys.add(
					# iButtun(langU['buttuns']['start_again'], callback_data = 'start_again:@{}'.format(user_id))
					# )
				try:
					video_info = subprocess.Popen([
							'youtube-dl', 'https://youtube.com/watch?v={}'.format(videoId),
							'--config-location', 'Files/youtube-dl.conf'
						   ], stdout = subprocess.PIPE)
					video_info = video_info.stdout.read()
					if video_info == b'':
						DataBase.sadd('fail_videos', videoId)
						await editText(chat_id, msg_id, 0, langU['tg_50mb'])
					else:
						video_info = json.loads(video_info)
						if type(video_info) is dict:
							if 'upload_date' in video_info:
								ap2 = video_info['upload_date']
								ap2 = (ap2[:4], ap2[4:6], ap2[6:8])
								upload_date = "{}/{}/{}".format(ap2[0], ap2[1], ap2[2])
								if user_steps[user_id]['lang'] == 'fa':
									geo = gregorian_to_jalali(int(ap2[0]), int(ap2[1]), int(ap2[2]))
									upload_date = "{} - {:04d}/{}/{:02d}".format(upload_date, geo[0], echoMonth(geo[1], True), geo[2])
							caption = langU['video_result'].format(
							video_info['title'],
							video_info['webpage_url'],
							video_info['uploader'],
							video_info['channel_url'],
							upload_date,
							video_info['view_count'],
							video_info['like_count'],
							video_info['dislike_count'],
							)
							inlineKeys.add(
								iButtun(langU['buttuns']['convert_mp3'], callback_data = 'conv2mp3:@{}:{}'.format(user_id, videoId)),
								iButtun(langU['buttuns']['convert_vnote'], callback_data = 'conv2vnote:@{}:{}'.format(user_id, videoId)),
								iButtun(langU['buttuns']['convert_ogg'], callback_data = 'conv2ogg:@{}:{}'.format(user_id, videoId)),
								)
							with open("{}.mp4".format(videoId), 'rb') as file:
								if os.path.exists("{}.jpg".format(videoId)):
									cover = open("{}.jpg".format(videoId), 'rb')
								elif os.path.exists("{}.webp".format(videoId)):
									cover = open("{}.webp".format(videoId), 'rb')
								await sendVideo(chat_id, _.reply_to_message, file, caption, "html",\
								video_info['duration'], cover, video_info['width'],\
								video_info['height'], True, 1, inlineKeys)
								await _.delete()
							set_stats('+', 'dl_youtube')
							try:
								os.system("mv ./{0}.mp4 ./tmp/{0}".format(videoId))
								os.system("rm -rf ./{}.jpg".format(videoId))
								os.system("rm -rf ./{}.webp".format(videoId))
							except Exception as e:
								print(e)
				except Exception as e:
					print(e)
					await editText(chat_id, msg_id, 0, langU['error_upload_video'], None)#, inlineKeys)
				deletePreviousData(user_id) #
				user_steps[user_id].update({'action': 'nothing'})
			else:
				await editText(chat_id, msg_id, 0, langU['try_again'], None, None)
		if re.match(r"^dlfile:@(\d+)$", input):
			# inlineKeys = iMarkup()
			# inlineKeys.add(
				# iButtun(langU['buttuns']['back'], callback_data = "backstart:@{}".format(user_id))
			# )
			user_steps[user_id].update({'action': 'downloading'})
			await editText(chat_id, msg_id, 0, langU['send_url_from_file'], None)#, inlineKeys)
		if re.match(r"^tosearch:@(\d+):(.*)$", input):
			ap = re_matches("^tosearch:@(\d+):(.*)$", input)
			if user_steps[user_id]['action'] == 'nothing' and 'what_do' in user_steps[user_id]:
				text = user_steps[user_id]['what_do']
				if ap[2] == 'music':
					# user_steps[user_id].update({'action': "search_music"})
					result = resultFromSoundCloud(msg, chat_id, user_id, text)
					if result:
						inlineKeys, one, two = result
						set_stats('+', 'search_music')
						await editText(chat_id, msg_id, 0, langU['look_finds'].format(one, two), None, inlineKeys)
					else:
						await editText(chat_id, msg_id, 0, langU['not_result'])
				elif ap[2] == 'video':
					try:
						await _.delete()
					except:
						try:
							await _.edit_reply_markup()
						except:
							pass
					# user_steps[user_id].update({'action': "search_video"})
					set_stats('+', 'search_youtube')
					await searchVideo(_.reply_to_message, chat_id, user_id, text)
		if re.match(r"^blockuser:(\d+)$",input):
			ap= re_matches("^blockuser:(\d+)$", input)
			if DataBase.get('isBan:{}'.format(ap[1])):
				alerttext = langU['usblocked']
			else:
				DataBase.set('isBan:{}'.format(ap[1]), "True")
				alerttext = langU['usblock']
				keyboard = blockKeys(ap[1])
				try:
					getC = await bot.get_chat(ap[1])
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={1})\nID: `{1}`\nStatus: Deactive🚫'.format(getC.first_name, ap[1]), 'md', keyboard)
				except:
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={0})\nID: `{0}`\nStatus: Deactive🚫'.format(ap[1]), 'md', keyboard)
			await answerCallbackQuery(msg, alerttext)
		if re.match(r"^unblockuser:(\d+)$",input):
			ap = re_matches("^unblockuser:(\d+)$", input)
			if DataBase.get('isBan:{}'.format(ap[1])):
				DataBase.delete('isBan:{}'.format(ap[1]))
				alerttext = langU['usunblocked']
				keyboard = blockKeys(ap[1])
				try:
					ggetC = await bot.get_chat(ap[1])
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={1})\nID: `{1}`\nStatus: Active✅'.format(getC.first_name, ap[1]), 'md', keyboard)
				except:
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={0})\nID: `{0}`\nStatus: Active✅'.format(ap[1]), 'md', keyboard)
			else:
				alerttext = langU['usunblock']
			await answerCallbackQuery(msg, alerttext)
		if re.match(r"^list:(.*):(\d+):@(\d+)$", input):
			ap = re_matches("^list:(.*):(\d+):@(\d+)$", input)
			# inlineKeys = iMarkup()
			if ap[1] == 'block':
				await editText(chat_id, msg_id, 0, langU['wait'])
				text = langU['list_block']
				keys = DataBase.keys("isBan:*")
				n = int(ap[2])
				for i in keys:
					n += 1
					userID = i.split(':')[-1]
					text = '{}{}- {} | {}\n'.format(
					text,
					n,
					await userInfos(userID),
					userID,
					)
				with open('Files/list_block.txt', mode = 'a', encoding = 'utf-8') as file:
					file.write(text)
				await sendDocument(chat_id, open('Files/list_block.txt', encoding = 'utf-8'))
				# inlineKeys.add(
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					# )
				await editText(chat_id, msg_id, 0, langU['blocklist_sent'], None)#, inlineKeys) 
				os.system('rm Files/list_block.txt')
			elif ap[1] == 'stats':
				# inlineKeys = iMarkup()
				# inlineKeys.add(
					# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id))
					# )
				dl_ig_post = DataBase.get('stat_dl_ig_post')
				dl_ig_story = DataBase.get('stat_dl_ig_story')
				search_music = DataBase.get('stat_search_music')
				dl_music = DataBase.get('stat_dl_music')
				search_youtube = DataBase.get('stat_search_youtube')
				dl_youtube = DataBase.get('stat_dl_youtube')
				dl_file = DataBase.get('stat_dl_file')
				all_users = DataBase.scard('allUsers')
				await editText(chat_id, msg_id, 0, langU['stats'].format(
				dl_ig_post,
				dl_ig_story,
				search_music,
				dl_music,
				search_youtube,
				dl_youtube,
				dl_file,
				all_users,
				).replace('None', '0'), 'html')#, inlineKeys)
		if re.match(r"^dlinsta:@(\d+)$", input):
			ap = re_matches("^dlinsta:@(\d+)$", input)
			user_steps[user_id].update({'action': "dl_ig"})
			# inlineKeys = iMarkup()
			# inlineKeys.add(
				# iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id))
				# )
			await editText(chat_id, msg_id, 0, langU['send_ig_url'], 'html')#, inlineKeys)
		if re.match(r"^conv2(.*):@(\d+):(.*)$", msg.data):
			ap = re_matches("^conv2(.*):@(\d+):(.*)$", msg.data)
			print(ap[3])
			if ap[1] == 'mp3':
				try:
					await _.edit_reply_markup()
				except:
					pass
				if os.path.exists('./tmp/{}'.format(ap[3])):
					try:
						caption = _.caption.split('\n')[0].split(' | ')[0].split(':')[1]
					except:
						caption = None
					caption = None
					await sendAudio(chat_id, _.reply_to_message, types.InputFile('tmp/{}'.format(ap[3])), caption)
				else:
					await sendText(chat_id, _, 1, langU['video_not_exist'])
			elif ap[1] == 'ogg':
				try:
					await _.edit_reply_markup()
				except:
					pass
				if os.path.exists('./tmp/{}'.format(ap[3])):
					try:
						caption = _.caption.split('\n')[0].split(' | ')[0].split(':')[1]
					except:
						caption = None
					await sendVoice(chat_id, _.reply_to_message, types.InputFile('tmp/{}'.format(ap[3])), caption, duration = _.video.duration)
				else:
					await sendText(chat_id, _, 1, langU['video_not_exist'])
			elif ap[1] == 'vnote':
				try:
					await _.edit_reply_markup()
				except:
					pass
				if os.path.exists('./tmp/{}'.format(ap[3])):
					ti = int(time())
					await resize_video(ap[3], ti, chat_id, _.reply_to_message)
					# await sendVideoNote(chat_id, _.reply_to_message, types.InputFile('tmp/{}Vnote.mp4'.format(ti)))
				else:
					await sendText(chat_id, _, 1, langU['video_not_exist'])
		if re.match(r"^tovnote:@(\d+)$", msg.data):
			try:
				await _.edit_reply_markup()
			except:
				pass
			if os.path.exists('./1'):
				# nest_asyncio.apply()
				ti = int(time())
				await resize_video('1', ti, chat_id, _.reply_to_message)
				# await sendVideoNote(chat_id, _.reply_to_message, types.InputFile('tmp/{}Vnote.mp4'.format(ti)))
				# os.system('rm tmp/1Vnote.mp4')
			else:
				await sendText(chat_id, _, 1, langU['video_not_exist'])


async def channel_post_process(msg: types.Message):
	if (msg.chat.username or '') != IDs_datas['chUsername']:
		await bot.leave_chat(msg.chat.id)


async def errors_handlers(update, exception):
	"""
	Exceptions handler. Catches all exceptions within task factory tasks.
	:param dispatcher:
	:param update:
	:param exception:
	:return: stdout logging
	"""
	if isinstance(exception, expts.CantDemoteChatCreator):
		log.debug("Can't demote chat creator!")
		return
	if isinstance(exception, expts.MessageNotModified):
		log.debug('Message is not modified!')
		return
	if isinstance(exception, expts.MessageToDeleteNotFound):
		log.debug('Message to delete not found!')
		return
	if isinstance(exception, expts.Unauthorized):
		log.info(f'Unauthorized: {exception} !')
		return
	if isinstance(exception, expts.InvalidQueryID):
		log.exception(f'InvalidQueryID: {exception} !\nUpdate: {update}')
		return
	if isinstance(exception, expts.TelegramAPIError):
		log.exception(f'TelegramAPIError: {exception} !\nUpdate: {update}')
		return
	if isinstance(exception, expts.RestartingTelegram):
		await asyncio.sleep(5)
		# log.exception(f'TelegramAPIError: {exception} !\nUpdate: {update}')
		await sendText(gv().sudoID, 0, 1, "The Telegram Bot API service is restarting...")
		return
	if isinstance(exception, telethonErrors.BotMethodInvalidError):
		return
	try:
		pass
	except AttributeError:
		log.exception(f'AttributeError: {exception} !\nUpdate: {update}')
		return


async def bot_off(app):
	await bot.delete_webhook()
	await client.disconnect()
	# await loop.close()
	print(colored("==========================", "white"), colored("\n= ", "white")+colored("Bot has been power ", "yellow")+colored("off", "red")+colored(" =", "white"), colored("\n==========================", "white"))


async def bot_run(app):
	content_types = types.ContentType.ANY
	dp.register_message_handler(message_process, content_types = content_types)
	dp.register_channel_post_handler(channel_post_process, content_types = content_types)
	dp.register_callback_query_handler(callback_query_process)
	dp.register_errors_handler(errors_handlers)
	webhook = await bot.get_webhook_info()
	if webhook.url != gv().WEBHOOK_URL:
		if not webhook.url:
			await bot.delete_webhook()
		await bot.set_webhook(gv().WEBHOOK_URL, open(gv().WEBHOOK_SSL_CERT, 'rb'), max_connections = 100, \
		allowed_updates = ['message', 'channel_post', 'callback_query'])
	await client.start(bot_token = telegram_datas['botToken'])
	bt = None
	while not bt:
		bt = await bot.get_me()
	if 'last_name' in bt:
		name = '{} {}'.format(bt.first_name, bt.last_name)
	else:
		name = bt.first_name
	ti_me = datetime.now()
	text = "{:04d}/{:02d}/{:02d} - {:02d}:{:02d}:{:02d}".format(ti_me.year, ti_me.month, ti_me.day, ti_me.hour, ti_me.minute, ti_me.second)
	a1 = 22-(len("Name > {}".format(name)) // 2)
	aa = ""
	for i in range(-1, a1):
		aa += " "
	b1 = 22-(len("Username > @{}".format(bt.username))//2)
	bb = ""
	for i in range(-1, b1):
		bb += " "
	c1 = 22-(len("ID > {}".format(bt.id)) // 2)
	cc = ""
	for i in range(-1, c1):
		cc += " "
	d1 = 22-(len("Developer > @{} [{}]".format(gv().sudoUser, gv().sudoID)) // 2)
	dd = ""
	for i in range(-1, d1):
		dd += " "
	e1 = 22-(len(text) // 2)
	ee = ""
	for i in range(0, e1):
		ee += " "
	z1 = 22-(len("#by aiogram[2.4]") // 2)
	zz = ""
	for i in range(-1, z1):
		zz += " "
	pW = colored("\n= ", "white")
	pW1 = colored("=================================================", "white")
	pW2 = colored("=", "white")
	print(pW1, \
	pW+aa+colored("Name", "red")+colored(" > ", "white")+colored("{}".format(name), "cyan")+aa+pW2, \
	pW+bb+colored("Username", "red")+colored(" > ", "white")+colored("@{}".format(bt.username), "cyan")+bb+pW2, \
	pW+cc+colored("ID", "red")+colored(" > ", "white")+colored("{}".format(bt.id), "cyan")+cc+pW2, \
	# pW+dd+colored("Developer", "red")+colored(" > ", "white")+colored("@{}[{}]".format(gv().sudoUser, gv().sudoID), "cyan")+dd+pW2, \
	pW+ee+colored(text, "yellow")+ee+" "+pW2, \
	pW+zz+colored("#by aiogram[2.4]", "magenta")+zz+"=\n"+pW1
	)
	redis.hset(db, 'id', bt.id)
	redis.hset(db, 'name', name) 
	redis.hset(db, 'user', bt.username) 
	redis.hset(db, 'token', telegram_datas['botToken'])
	try:
		bt1 = await bot.get_chat(sudo_id)
		DataBase.hset('sudo', 'user', bt1.username)
		if bt1.username:
			DataBase.hset('sudo', 'id', bt1.id)
	except:
		print("Sudo Not Found!!!")
	await sendText(752815712, 0, 1, 'Bot has been Successfully Loaded')
	if not redis.hget(db, 'supchat'):
		status = False
		while status != True:
			iD = input("Enter Supergroup ID for support: ")
			if re.match(r'^(-\d+)$', iD):
				redis.hset(db, 'supchat', re.match(r'^(-\d+)$', iD).group(1))
				status = True
				break
			else:
				iD = input("Enter Channel ID for support: ")
				status = False


# كارا
if __name__  == '__main__':
	global user_steps
	user_steps = {}
	app = get_new_configured_app(dispatcher = dp, path = gv().WEBHOOK_URL_PATH)
	app.on_startup.append(bot_run)
	app.on_shutdown.append(bot_off)
	context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	context.load_cert_chain(gv().WEBHOOK_SSL_CERT, gv().WEBHOOK_SSL_PRIV)
	# web.run_app(app, host = "0.0.0.0", port = gv().port, ssl_context = context)
	web.run_app(app, host="0.0.0.0", port=gv().port)

