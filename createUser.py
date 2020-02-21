#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:18:24 2020

@author: luciasuelves
"""

from pymongo import MongoClient
#from errorHandler import jsonErrorHandler
from bson.json_util import dumps
# Connect to the database
client = MongoClient("mongodb://localhost/ChatWithHeart")


#@jsonErrorHandler
def createUser(name):
    users = client.get_default_database()["Users"]
    if users.find_one({'username': name}):
        return False
    else:
        users.insert({'username': name, 'chats': [], 'messages':[]})
        return dumps(users.find_one({'username':name})['_id'])