#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:18:24 2020

@author: luciasuelves
"""

from pymongo import MongoClient
#from errorHandler import jsonErrorHandler
from bson.json_util import dumps
import re
# Connect to the database
client = MongoClient("mongodb://localhost/companies")


#@jsonErrorHandler
def getCompanyWithName(name):
    companies = client.get_default_database()["cleancompanies"]
    namereg = re.compile(name, re.IGNORECASE)
    print(namereg)
    query = companies.find_one({"name": namereg})
    if not query:
        raise ValueError("Company not found")
    return dumps(query)