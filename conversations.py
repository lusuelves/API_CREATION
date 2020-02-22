from pymongo import MongoClient
#from errorHandler import jsonErrorHandler
from bson.json_util import dumps
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
import seaborn as sns
import numpy as np
# Connect to the database
client = MongoClient("mongodb://localhost/ChatWithHeart")

users = client.get_default_database()["Users"]
convers = client.get_default_database()["Conversations"]
messages = client.get_default_database()["Messages"] 
#@jsonErrorHandler
# Create chat, updates for chats in users and includes users id in participants.
def createChat(title,user):
    convers = client.get_default_database()["Conversations"]
    unique_title = define_title(convers,title) #We want a unique title
    convers.insert({'title': unique_title, 'participants': [], 'messages':[]}) #After verifying title and user create chat
    chat_id = get_chat(title)[0] #Get the chat id to add it to the users chats
    add_user(unique_title,user)
    return dumps(chat_id)
    
def define_title(convers,title):
    while convers.find_one({'title': title}):
        title = input("Enter another name for the conversation : ") 
    return title

def get_user():
    users = client.get_default_database()["Users"]
    user = input('What username?: ')
    #user = '<label for="lname">Last name:</label>'
    return (users.find_one({'username':user})['_id'],users)

def get_chat(title):
    convers = client.get_default_database()["Conversations"]
    return (convers.find_one({'title':title})['_id'], convers)

def add_chat_to_user(chat_id,*args):
    if args:
        user = args[0]
        users = client.get_default_database()["Users"]
    else:
        (user_id,users) = get_user()
        users.update({'_id':user_id},{'$push':{'chats': chat_id}})
    users.update({'username':user},{'$push':{'chats': chat_id}})
    return args[0]

def add_user_to_chat(chat_title, user):
    (chat_id, convers) = get_chat(chat_title)
    users = client.get_default_database()["Users"]
    user_id = users.find_one({'username':user})['_id']
    return convers.update({'_id':chat_id},{'$push':{'participants':user_id}})

def add_user(chat_title,*args):
    print(args)
    (chat_id, convers) = get_chat(chat_title)
    user = args[0]
    add_chat_to_user(chat_id,user)
    add_user_to_chat(chat_title, user)
    return dumps(chat_id)

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
"""
def add_message_terminal(chat_title):
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
"""  
def add_message_to_chat(chat_id,message):
    return convers.update({'_id':chat_id},{'$push':{'messages':message}})
    
def add_message_to_user(user_id,message_id):
    return users.update({'_id':user_id},{'$push':{'messages':message_id}})

def user_in_chat(user_id,chat_id):
    return user_id in convers.find_one({'_id':chat_id})['participants']

def get_messages_from_chat(chat_title):
    messages_in_chat = ''
    chat_id = get_chat_info(chat_title)['_id']
    for message_id in convers.find_one({'_id':chat_id})['messages']:
        messages_in_chat += messages.find_one({'_id':message_id})['text'] + ' '
    return messages_in_chat
        
def get_sentiments_from_chat(chat_title):
    messages_in_chat = get_messages_from_chat(chat_title)
    sia = SentimentIntensityAnalyzer()
    sentiments = sia.polarity_scores(messages_in_chat)
    return json.dumps(sentiments)

def get_messages_from_user(username):
    users = client.get_default_database()["Users"]
    messages = client.get_default_database()["Messages"]
    messages_in_user = {}
    user_id = users.find_one({'username':username})['_id']
    for message_id in users.find_one({'_id':user_id})['messages']:
        message = messages.find_one({'_id':message_id})['text']
        messages_in_user[username] = message
    return json.dumps(messages_in_user)

def recommend(username):
    messages = get_messages_from_every_user()
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(messages.values())
    print(list(count_vectorizer.vocabulary_.keys()))
    m = sparse_matrix.todense()
    print(m.shape)
    print(m[0])
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=messages.keys())
    print(df)
    similarity_matrix = distance(df,df)
    print(similarity_matrix)
    sim_df = pd.DataFrame(similarity_matrix, columns=messages.keys(), index=messages.keys())
    print(sim_df)
    np.fill_diagonal(sim_df.values, 0) # Remove diagonal max values and set those to 0
    similar = (sim_df[username].nlargest(n = 2).index.tolist())
    return json.dumps(similar)
        
def get_messages_from_every_user():
    users = client.get_default_database()["Users"]
    messages = client.get_default_database()["Messages"]
    messages_in_users = dict()
    for user in users.find():
        for message_id in user['messages']:
            message = messages.find_one({'_id':message_id})['text']
            messages_in_users[user['username']] = message
    return messages_in_users

def who_are_you():
    return """<form action="/action_page.php">
                  <label for="fname">First name:</label>
                  <input type="text" id="fname" name="fname"><br><br>
                  <label for="lname">Last name:</label>
                  <input type="text" id="lname" name="lname"><br><br>
                  <input type="submit" value="Submit">
            </form>"""
            
def exist_user(username):
    return users.find_one({'username':username})['chats']

def get_chat_title(chat_id):
    return convers.find_one({'_id':chat_id})['title']