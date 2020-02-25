from pymongo import MongoClient
from bson.json_util import dumps
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np
import json
# Connect to the database
client = MongoClient("mongodb://localhost/ChatWithHeart")

users = client.get_default_database()["Users"]
messages = client.get_default_database()["Messages"]

def createUser(name):
    if users.find_one({'username': name}):
        return False
    else:
        users.insert({'username': name, 'chats': [], 'messages':[]})
        return dumps(users.find_one({'username':name})['_id'])

def get_messages_from_user(username):
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
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=messages.keys())
    similarity_matrix = distance(df,df)
    sim_df = pd.DataFrame(similarity_matrix, columns=messages.keys(), index=messages.keys())
    np.fill_diagonal(sim_df.values, 0) # Remove diagonal max values and set those to 0
    similar = (sim_df[username].nlargest(n = 2).index.tolist())
    return json.dumps(similar)
        
def get_messages_from_every_user():
    messages_in_users = dict()
    for user in users.find():
        for message_id in user['messages']:
            message = messages.find_one({'_id':message_id})['text']
            messages_in_users[user['username']] = message
    return messages_in_users