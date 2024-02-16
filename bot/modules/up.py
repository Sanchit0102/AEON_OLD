# OMFOO
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup
import sys, os, time, io, re, traceback, warnings, weakref, collections.abc,random,string
import subprocess
from .listener import MirrorLeechListener
from bot.helper.ext_utils.fs_utils import clean_download, get_base_name, get_path_size
from pathlib import PurePath

from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters 

from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, deleteMessage, delete_all_messages, update_all_messages, sendStatusMessage
from bot.helper.mirror_utils.status_utils.upload_status import UploadStatus
from bot import LOGGER, dispatcher, DOWNLOAD_DIR, Interval, INDEX_URL, download_dict, download_dict_lock

def up(update, context):
      args = update.message.text.split(" ", maxsplit=2)
      if(len(args) > 1):
        uid = update.message.message_id
        tag = update.message.from_user.mention_html(update.message.from_user.first_name)
        gid = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=12))
        listener = MirrorLeechListener(context.bot, update.message, isZip=False, extract=False, isQbit=False, isLeech=False, tag=tag)
        #up_dir = f'{DOWNLOAD_DIR}{uid}'
        name = " ".join(map(str, args[1:]))# args[1:]
       # subprocess.run(["mv",name,up_dir])
        #ot = subprocess.Popen(["find", ".", "-name", f'{up_dir}/{name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdout, stderr = ot.communicate()
        up_path = name
        print(up_path)
        up_dir = PurePath(up_path).parents[0]
        size = get_path_size(f'{up_dir}/{name}')
        sendMessage(f"Uploading: {name}",context.bot,update.message)
        drive = GoogleDriveHelper(name,up_dir ,size ,listener)
        upload_status = UploadStatus(drive, size, gid, listener)
            
        '''
        with download_dict_lock:
            download_dict[uid] = upload_status
        update_all_messages()
        '''
        drive.upload(name,u_index=None,c_index=0)
       
      else:
          sendMessage(f"Send File Name",context.bot,update.message) 
up_handler = CommandHandler(BotCommands.UpCommand, up,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(up_handler)
