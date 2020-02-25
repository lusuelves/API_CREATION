from pymongo import MongoClient
from bson.json_util import dumps
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Connect to the database
client = MongoClient("mongodb://localhost/ChatWithHeart")

users = client.get_default_database()["Users"]
convers = client.get_default_database()["Conversations"]
messages = client.get_default_database()["Messages"] 


"""
This function creates a new conversation, if there is no conversation with that
name and it directly adds the conversation to the user who created it.
"""
def createChat(chat_title,user):
    if not exist_chat_title(chat_title):
        convers.insert({'title': chat_title, 'participants': [], 'messages':[]})
    chat_id = get_chat_info(chat_title)['_id'] 
    add_user(chat_title,user)
    return dumps(chat_id)

def exist_chat_title(chat_title):
    return convers.find_one({'title':chat_title})

def add_user(chat_title,*args):
    chat_id = get_chat_info(chat_title)['_id']
    if users.find_one({'username':args[0]}):
        user_id = get_user_info(args[0])['_id']
        if not user_in_chat(user_id,chat_id):
            users.update({'_id':user_id},{'$push':{'chats': chat_id}})
            convers.update({'_id':chat_id},{'$push':{'participants':user_id}})
            return dumps(chat_id)
        else:
            return "{user} is already participant in the conversation".format(user=args[0])
    else:
        print("User does not exist")

def new_message(user_id,chat_id,message):  
    return messages.insert({'text':message,'author':user_id,'conversation':chat_id}) 

def add_message(chat_title, username, message):
    chat_id = get_chat_info(chat_title)['_id']
    user_id = get_user_info(username)['_id']
    if user_in_chat(user_id,chat_id):
        message_id = new_message(user_id, chat_id, message)
        add_message_to_chat(chat_id,message_id)
        add_message_to_user(user_id,message_id)
        return dumps(message_id)
    else:
        print("You are not in the chat")

def get_user_info(username):
    return users.find_one({'username':username})

def get_chat_info(chat_title):
    return convers.find_one({'title':chat_title})

def get_chat_title(chat_id):
    return convers.find_one({'_id':chat_id})['title']

def exist_user(username):
    return users.find_one({'username':username})

def add_message_to_chat(chat_id,message):
    return convers.update({'_id':chat_id},{'$push':{'messages':message}})
    
def add_message_to_user(user_id,message_id):
    return users.update({'_id':user_id},{'$push':{'messages':message_id}})

def user_in_chat(user_id,chat_id):
    return user_id in convers.find_one({'_id':chat_id})['participants']

"""
Gets conversation to display it afterwards.
"""
def get_conversation(chat_title):
    messages_in_chat = []
    chat_id = get_chat_info(chat_title)['_id']
    for message_id in convers.find_one({'_id':chat_id})['messages']:
        user_id = messages.find_one({'_id':message_id})['author']
        username = users.find_one({'_id':user_id})['username']
        mess = username + ': ' + messages.find_one({'_id':message_id})['text']
        messages_in_chat.append(mess)
    return messages_in_chat

"""
Format the messages to analise sentiments.
"""
def get_messages_from_chat(chat_title):
    messages_in_chat = ''
    chat_id = get_chat_info(chat_title)['_id']
    for message_id in convers.find_one({'_id':chat_id})['messages']:
        messages_in_chat += messages.find_one({'_id':message_id})['text'] + ' '
    return messages_in_chat

"""
Analise sentiments for an entire conversation
"""
def get_sentiments_from_chat(chat_title):
    messages_in_chat = get_messages_from_chat(chat_title)
    sia = SentimentIntensityAnalyzer()
    sentiments = sia.polarity_scores(messages_in_chat)
    return json.dumps(sentiments)



