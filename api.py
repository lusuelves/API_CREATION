#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:46:41 2020

@author: luciasuelves
"""

from flask import Flask, request,render_template
import random
from companies import getCompanyWithName
from createUser import createUser
from conversations import createChat, add_user, add_message, get_messages_from_chat, get_messages_from_user,get_sentiments_from_chat, recommend, who_are_you           

app = Flask(__name__)


@app.route('/user/create')
def index():
    return render_template('test.html')

@app.route('/')
def hello():
    return """
            <h1> Welcome to Chat with the Heart </h1>
            <form action="/user/create">
            <input type="submit" value="Create User" />
            </form>
            """

@app.route('/user/create/<name>')
def create(name):
    return createUser(name)

@app.route('/chat/create/<title>')
def newChat(title):
    return createChat(title)

@app.route('/chat/<chat_title>/adduser')
def addUserToChat(chat_title):
    return add_user(chat_title)

@app.route('/chat/<chat_title>/addmessage')
def addMessageToChat(chat_title):
    return add_message(chat_title)

@app.route('/chat/<chat_title>/list')
def getMessagesFromChat(chat_title):
    return get_messages_from_chat(chat_title)

@app.route('/chat/<chat_title>/sentiment')
def getSentimentsFromChat(chat_title):
    return get_sentiments_from_chat(chat_title)

@app.route('/user/<username>/sentiment')
def getSentimentsFromUser(username):
    return get_messages_from_user(username)

@app.route('/user/<username>/recommend')
def getRecommendation(username):
    return recommend(username)

@app.route('/who', methods=['POST'] )
def who():
    first_name = request.form['first_name']
    if createUser(first_name):
        return """
            <h1>Welcome {first_name}</h1>
            <form action="{first_name}/newchat" method="post">
                        Chat name: <input type="text" name="chat_title">  <br />
                        <input type="submit" name= "form" value="Submit" />
            </form>
            """.format(first_name=first_name)
    else:
        return 'Username already exists'
        
@app.route('/<username>/newchat', methods=['POST'] )
def newchat(username):
    chat_title = request.form['chat_title']
    return createChat(chat_title,username)
app.run("0.0.0.0", 5000, debug=True)