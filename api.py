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
from conversations import createChat, add_user, add_message, get_messages_from_chat, get_messages_from_user,get_sentiments_from_chat, recommend, who_are_you, exist_user, get_chat_title        

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
            <form action="/user/login">
            <input type="submit" value="Log in"/>
            </form>
            """
@app.route('/user/login')
def login():
        return  """
            <form action="/who" method="post">
                User Name: <input type="text" name="first_name">  <br />
                <input type="submit" name= "form" value="Submit" />
            </form>
        """
        
@app.route('/user/<username>')
def welcome(username):
        return """
            <h1>Welcome {username}</h1>
            """.format(username=username)
  
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
    elif exist_user(first_name):
        chats = [get_chat_title(chat_id) for chat_id in  exist_user(first_name)]
        buttons = ""
        for chat in chats:
            buttons += """<form action="/user/{first_name}/chat/{chat}">
            <input type="submit" value={chat} />
            </form>""".format(chat=chat, first_name=first_name)
        return """
            <h1>Welcome back {first_name}</h1>
            <form action="/{first_name}/newchat" method="post">
                        Chat name: <input type="text" name="chat_title">  <br />
                        <input type="submit" name= "form" value="Submit" />
            </form>
            <form action="/user/{first_name}/recommend">
                <input type="submit" value='Get recommendation' />
            </form>
            {buttons}
            """.format(first_name=first_name, buttons=buttons )
    else:
        return 'Username already exists'
    
@app.route('/user/<username>/chat/<chat_title>', methods=['POST','GET'])
def print_chats(username,chat_title):
    messages = get_messages_from_chat(chat_title)
    if request.form:
        new_message = request.form['new_message']
        print(new_message)
        add_message(chat_title,username, new_message)
    return """
        {messages}
        <form action="/user/{username}/chat/{chat}" method="post">
                        New message: <input type="text" name="new_message">  <br />
                        <input type="submit" name= "form" value="Submit" />
        </form>
        <form action="/chat/{chat}/sentiment">
            <input type="submit" value="Get sentiment"/>
        </form>
        
    """.format(messages=messages,username=username,chat=chat_title)

@app.route('/chat/{chat}/sentiment')
def get_sentiment(chat):
    return get_sentiments_from_chat(chat)

@app.route('/<username>/newchat', methods=['POST'] )
def newchat(username):
    chat_title = request.form['chat_title']
    return createChat(chat_title,username)
app.run("0.0.0.0", 5000, debug=True)