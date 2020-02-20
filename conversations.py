from pymongo import MongoClient
#from errorHandler import jsonErrorHandler
from bson.json_util import dumps
# Connect to the database
client = MongoClient("mongodb://localhost/ChatWithHeart")


#@jsonErrorHandler
# Create chat, updates for chats in users and includes users id in participants.
def createChat(title):
    convers = client.get_default_database()["Conversations"]
    unique_title = define_title(convers,title) #We want a unique title
    convers.insert({'title': unique_title, 'participants': [], 'messages':[]}) #After verifying title and user create chat
    chat_id = get_chat(title)[0] #Get the chat id to add it to the users chats
    add_user(unique_title)
    return dumps(chat_id)
    
def define_title(convers,title):
    while convers.find_one({'title': title}):
        title = input("Enter another name for the conversation : ") 
    return title

def get_user():
    users = client.get_default_database()["Users"]
    user = input('What username?: ')
    return (users.find_one({'username':user})['_id'],users)

def get_chat(title):
    convers = client.get_default_database()["Conversations"]
    return (convers.find_one({'title':title})['_id'], convers)

def add_chat_to_user(chat_id):
    (user_id,users) = get_user()
    users.update({'_id':user_id},{'$push':{'chats': chat_id}})
    return user_id

def add_user_to_chat(chat_title, user_id):
    (chat_id, convers) = get_chat(chat_title)
    return convers.update({'_id':chat_id},{'$push':{'participants':user_id}})

def add_user(chat_title):
    (chat_id, convers) = get_chat(chat_title)
    user_id = add_chat_to_user(chat_id)
    add_user_to_chat(chat_title, user_id)
    return dumps(chat_id)

def new_message(user_id,chat_id):
    messages = client.get_default_database()["Messages"]
    message = input('Write message: ')   
    return messages.insert({'text':message,'author':user_id,'conversation':chat_id}) 

def add_message(chat_title):
    (chat_id, convers) = get_chat(chat_title)
    (user_id, users) = get_user()
    if user_in_chat(user_id,chat_id,convers):
        message_id = new_message(user_id, chat_id)
        add_message_to_chat(chat_id,convers,message_id)
        add_message_to_user(user_id,users,message_id)
        return dumps(message_id)
    else:
        print("You are not in the chat")
        add_message(chat_title)
    
def add_message_to_chat(chat_id,convers,message):
    return convers.update({'_id':chat_id},{'$push':{'messages':message}})
    
def add_message_to_user(user_id,users,message_id):
    return users.update({'_id':user_id},{'$push':{'messages':message_id}})

def user_in_chat(user_id,chat_id,convers):
    return user_id in convers.find_one({'_id':chat_id})['participants']
    