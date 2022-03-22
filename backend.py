import json
from flask import Flask, jsonify, request
import requests as rq
backend = Flask(__name__)

data = {

    }


def getStars(address):
    r = rq.get('https://airdrop.devnet.publicawesome.dev/address/'+address)
    j = json.loads(r.content.decode('utf-8'))
    data[j["denom"]] = {
        "name": "Stars",
        "bal": j["balance"],
        "link": "https://app.stargaze.zone/airdrop"
        }
    return r.content

def getMantle(address):
    r = rq.get('https://cosmos-stakedrop.assetmantle.one/delegator/'+address)
    j = json.loads(r.content.decode('utf-8'))
    data["mantle"] = {
        "name": "AssetMantle",
        "bal": (j["estimated"]/1000000),
        "link": "https://airdrop.assetmantle.one/stakedrop"
        }
    return r.content

def getGame(address):
    r = rq.post('https://airdrop.gamenet.one/query', json={"operationName":"GET_AIRDROP","variables":{"acc_address":address},"query":"query GET_AIRDROP($acc_address: String!) {\n  airdrop(acc_address: $acc_address) {\n    denom\n    amount\n    __typename\n  }\n}\n"})
    j = json.loads(r.content.decode('utf-8'))
    data["game"] = {
        "name": "Game",
        "bal": (j["data"]["airdrop"]["amount"]/1000000),
        "link": "https://airdrop.gamenet.one/"        
        }
    return r.content

def getDesmos(address):
    r = rq.get('https://api.airdrop.desmos.network/users/'+address)
    j = json.loads(r.content.decode('utf-8'))
    data["desmos"] = {
        "name": "Desmos",
        "bal": j["dsm_allotted"],
        "link":"https://airdrop.desmos.network/
        }
    return r.content

def getLikeCoin(address):
    r = rq.get('https://airdrop.like.co/api/overview?address='+address)
    j = json.loads(r.content.decode('utf-8'))
    data["likeCoin"] = {
        "name": "LikeCoin",
        "bal": (j["allocatedAmount"]/1000000000),
        "link": "https://app.like.co/airdrop/claim"
        }
    return r.content


@backend.after_request
def add_header(response):
    response.headers['access-control-allow-origin'] = 'http://airdrop.mechikoff.com'
    return response
    
#Generic GET request at the primary route. Returns the entire car dataset
# http://localhost:5000/
@backend.route('/', methods=['GET'])
def getAllCars():
    return jsonify(cars)

#GET a particular car by ID
@backend.route('/airdrop', methods=['GET'])
def getAirdrops():
    address = request.args.get("address")
    getStars(address)
    getMantle(address)
    getGame(address)
    getDesmos(address)
    getLikeCoin(address)
    return jsonify(data)
    
backend.run(host = '0.0.0.0')
