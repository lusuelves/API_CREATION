#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:46:41 2020

@author: luciasuelves
"""

from flask import Flask, request
import random
from companies import getCompanyWithName
from createUser import createUser
from conversations import createChat, add_user

app = Flask(__name__)


@app.route('/')
def hello():
    pepe = {
        "nombre": "Luis",
        "edad": 30
    }
    return pepe


def controllerFn(): return {"hola": "pepe"}


app.route('/hola')(controllerFn)

@app.route('/company/<name>')
def getCompany(name):
    return getCompanyWithName(name)

@app.route('/user/create/<name>')
def create(name):
    return createUser(name)

@app.route('/chat/create/<title>')
def newChat(title):
    return createChat(title)

@app.route('/chat/<chat_title>/adduser')
def addUserToChat(chat_title):
    return add_user(chat_title)

app.run("0.0.0.0", 5000, debug=True)