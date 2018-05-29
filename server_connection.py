#!/usr/bin/python

# Script created by Dr. Jorge Abreu Vicente and Mattia Molteni
# For the company Datavard AG.
# For the product Carchain.
# All rights reserved for Datavard AG

import requests
import json
import datetime

def auth(id = "car1234"):
    """
    Function that is used to get the authentification
    details to acces to the Carchain server.

    Inputs:
        : id [string] : Identfiction to enter the system. 

    Returns:
        : Dictionary: identifier and password keys
    
    """

    return {"identifier":id, "password":"car1234_token"}


def carchain_server_auth(url = "https://dvd-carchain.herokuapp.com/auth/local"):
    """Returns the URL for the Carchain server."""
    return url

def carchain_server_data(url = "https://dvd-carchain.herokuapp.com/Carevent"):
    """Returns the URL for the Carchain server."""
    return url



def get_token():
    """
    Gets the token of the API toget access to the server data.
    """
    r = requests.post(carchain_server_auth(), auth())
    j = json.loads(r.text)
    return j["jwt"]

def data_to_write(carID, event, payload):

    return {
        "carID":carID,
        "event":event,
        "payload":payload,
        "timestamp":str(datetime.datetime.now())
        }

def write_data_to_server(carID, event, payload):
    """
    Writes the data to the car database in the server.
    : data: [dictionary] with keys and values measured by different sensors
    """

    url_to_write = carchain_server_data()
    headers = {
        "Authorization":"Bearer %s"%get_token()
        }
    data = data_to_write(carID, event, payload)
    new_entry = requests.post(url_to_write, headers = headers, data = data)

    if new_entry.status_code == 200:
        print 30*"""*"""
        print """Data written SUCCESSFULLY to carchain server"""
        print 30*"""*"""
    else:
        print 30*"""*"""
        print """WARNING: Some problem found. Post Status request is %s"""%str(new_entry.status_code)
        print 30*"""*"""
        
    pass

