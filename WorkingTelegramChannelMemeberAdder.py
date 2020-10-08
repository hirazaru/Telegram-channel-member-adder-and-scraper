"""
Project Name: Telegram Member Adder To Channel
Developed BY: VIASK (via5k)
First Launched : 08-Oct-2020

"""
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random

api_id = 111111 #API ID
api_hash = '45049565ff307d070e0a71de0b001b39' #API HASH
phone = '+10000000000' #MOBILE NUMBER WITH COUNTRY CODE
client = TelegramClient(phone, api_id, api_hash)
 
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
input_file = 'C:\\Users\\User\\Desktop\\members.csv' #LOCATION OF THE FILE CONTAINING USERS INFO
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        #user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 20000
groups=[]
channeluser= 'LetsSwingg' #USERNAME OF THE CHANNEL WHERE THE MEMBERS WILL BE ADDED

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
n = 0
for user in users:
    time.sleep(5)
    n += 1
    if n % 5 == 0:
        time.sleep(10)
    try:
        print ("Adding {}".format(user['id'],user['username']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
            
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
            time.sleep(2)
            AskedJoinedUsers = 'C:\\Users\\User\\Desktop\\AskedJoinedUsers.csv' #CREATING THE LIST OF USERS THAT WERE USED TO JOINED THE CHANNEL
            with open(AskedJoinedUsers, 'a+', encoding='UTF-8') as g:
                writer = csv.writer(g,delimiter=",",lineterminator="\n")
                writer.writerow([user['id']])
                writer.writerow("\n")
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        
        client(InviteToChannelRequest(
        channeluser,
        [user_to_add]
        ))
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        sys.exit()
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
        n=n-1
        NotJoinedUsers = 'C:\\Users\\User\\Desktop\\NotJoinedUsers.csv' #New file that stores the data of the users that were not able to join the channel
        with open(NotJoinedUsers, 'a+', encoding='UTF-8') as g:
            writer = csv.writer(g,delimiter=",",lineterminator="\n")
            writer.writerow([user['id']])
            writer.writerow("\n") 
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
print('GITHUB: via5k')