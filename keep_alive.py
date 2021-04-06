from flask import Flask, make_response
from threading import Thread
import json
import flask
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

class UserSettings(Resource):
	def get(self, userid):
		with open("settings.json", "r") as f:
			users = json.load(f)
		with open("statistics.json", "r") as f:
			userStats = json.load(f)
		if userid in users:
			username = users[str(userid)]["username"]
			ranCmds = userStats[str(userid)]["rancmd"]
			xp = userStats[str(userid)]["xp"]
			sentMsgs = userStats[str(userid)]["sentmsgs"]
			allowMentions = users[str(userid)]["allowMentions"]
			autoRejectFights = users[str(userid)]["autoRejectFights"]
			passiveMode = users[str(userid)]["passiveMode"]
			whisperEconomy = users[str(userid)]["whisperEconomy"]
			onJoinMsg = users[str(userid)]["onJoinMsg"]
			allowUserInteraction = users[str(userid)]["allowUserInteraction"]
			response = flask.jsonify({"username": f"{username}", "allowMentions": f"{allowMentions}", "autoRejectFights": f"{autoRejectFights}", "passiveMode": f"{passiveMode}", "whisperEconomy": f"{whisperEconomy}", "onJoinMsg": f"{onJoinMsg}", "allowUserInteraction": f"{allowUserInteraction}", "ranCmds": f"{ranCmds}", "xp": f"{xp}", "sentMsgs": f"{sentMsgs}"})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		else:
			response = flask.jsonify({"message": "404: Couldn't find a user with that ID in my database, try running d!settings on that account."})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response

api.add_resource(UserSettings, "/api/profile/<userid>")

class Leaderboard(Resource):
	def get(self, ctgry: str):
		with open("statistics.json", "r") as f:
			users = json.load(f)
		leader_board = {}
		total = []
		x = 15
		for user in users:
			name = str(user)
			username = users[user]["username"]
			total_amount = users[user][ctgry]
			leader_board[total_amount] = name
			total.append(total_amount)
		
		total = sorted(total,reverse=True)
		index = 1
		mesge = []
		for amt in total:
			id_ = leader_board[amt]
			name = users[id_]["username"]
			mesge.append(f"{name} - {amt}")
			if index == x:
				break
			else:
				index += 1


		response = flask.jsonify({"first": f"1. {mesge[0]}", "second": f"2. {mesge[1]}", "third": f"3. {mesge[2]}", "fourth": f"4. {mesge[3]}", "fifth": f"5. {mesge[4]}", "sixth": f"6. {mesge[5]}", "seventh": f"7. {mesge[6]}", "eight": f"8. {mesge[7]}", "nineth": f"9. {mesge[8]}", "tenth": f"10. {mesge[9]}", "eleventh": f"11. {mesge[10]}", "twelveth": f"12. {mesge[11]}", "thirteenth": f"13. {mesge[12]}", "fourteenth": f"14. {mesge[13]}", "fifteenth": f"15. {mesge[14]}"})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

api.add_resource(Leaderboard, "/api/leaderboard/<ctgry>")


class BotInfo(Resource):
	def get(self):
		with open("botinfo.json", "r") as f:
			botinf = json.load(f)
		roomName = botinf["botinfo"]["botroomname"]
		roomUrl = botinf["botinfo"]["botroomurl"]
		roomCount = botinf["botinfo"]["botroomcount"]
		roomDescription = botinf["botinfo"]["botroomdescription"]
		response = flask.jsonify({"roomName": f"{roomName}", "roomUrl": f"{roomUrl}", "roomCount": f"{roomCount}", "roomDescription": f"{roomDescription}"})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

api.add_resource(BotInfo, "/api/botinfo")

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)
  print("Running yOO")

def keep_alive():
    t = Thread(target=run)
    t.start()
    print("Keep Alive Started dawg")
    

