
import twitter
# creates own server
from flask import Flask
from flask import jsonify
from flask import request
import time
import os
import sys 
from dotenv import load_dotenv,find_dotenv




# get a token from "https://apps.twitter.com/app/new"
load_dotenv(find_dotenv())
TWITTER_CONSUMER_KEY= os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET=os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN_KEY=os.getenv("TWITTER_ACCESS_TOKEN_KEY")
TWITTER_ACCESS_TOKEN_SECRET=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


api = twitter.Api(
consumer_key=TWITTER_CONSUMER_KEY, 
consumer_secret=TWITTER_CONSUMER_SECRET,
access_token_key=TWITTER_ACCESS_TOKEN_KEY,
access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

app = Flask(__name__)
	

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/users/<user>")
# Fetches the sequence of public Status messages for a single user
def get_user_timeline(user):
	try:
		count=request.args.get("count",default=50,type=int)
		start=request.args.get("start",default=0,type=int)
		end=request.args.get("end",default=10,type=int)

		statuses = api.GetUserTimeline(screen_name=user,count=count)
		mentions = api.GetSearch(term='to:@' + user,count=count)

		status_id_to_reply_count = {}

		# create a list-of-dicts of mentions
		mds =[]
		for m in mentions:
			md = m.AsDict()
			mds.append(md)

		sds = []
		for s in statuses:
			# reply_count = 0
			# for m in mds:
			# 	if 'in_reply_to_status_id'in m and
			# 	m['in_reply_to_status_id'] == s ['id']:
			# 		reply_count +=1
			# creates a dictionary representation of the objects
			sd = s.AsDict()
			t = time.strptime(sd["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
			ts = time.strftime('%b %d, %Y', t)
			sd["created_at"]=ts
			# create the status_id_to_reply_count entry
			status_id = sd['id']
			# status_id = "13987198172489"
			status_id_to_reply_count[status_id] = 0
			# status_id_to_reply_count["13987198172489"] = 0
			sds.append(sd)

		# status_id_to_reply_count = {
		# 	"13987198172489": 0,
		# 	"12421412412121": 0,
		# 	"89713583275875": 0,
		# }

		# calculate reply count
		# iterate through our mentions
		#	check if the in_reply_to_status_id field is present in our mention
		#		check if that status id is present in our status_id_to_reply_count dict
		#			if it is, we add 1 to the value in the dictionary (using that as the key)
		for m in mds:
			if "in_reply_to_status_id" in m:
				status_id=m["in_reply_to_status_id"]
				if status_id in status_id_to_reply_count:
					status_id_to_reply_count[status_id]+=1

		# status_id_to_reply_count = {
		# 	"13987198172489": 1,
		# 	"12421412412121": 5,
		# 	"89713583275875": 3,
		# }	

		# before we pass sds (our list of dicts of the tweets) back to the user
		# get each tweet dict from sds
		# add a reply_count field to it
		# set the value to the reply count that we currently have in status_id_to_reply_count
		# use the 'id' field in the tweet as the key to find the related entry in the status_id_to_reply_count dict
		# sds = [
		#	{
		#		"id": "148128497",
		#		"text": "seitest"
		#
		#	},
		#	{
		#		"id": "358758322",
		#		"text": "setst"
		#
		#		},
		# ]
		for sd in sds:
			status_id=sd["id"]
			sd['reply_count'] = status_id_to_reply_count[status_id]

		# Pagination
		sds = sds[start:end+1]

		# changes python to json
		return jsonify(sds)

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		error = str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno)
		return app.response_class(
			response="{'error':'Unable to communicate with Twitter - " + error + "}",
			status=408,
			mimetype='application/json')
    

@app.route("/hashtags/<hashtag>")
# Fetches the sequence of public Status messages for a single user
def get_hashtag_timeline(hashtag):
	try:
		count=request.args.get("count",default=50,type=int)
		start=request.args.get("start",default=0,type=int)
		end=request.args.get("end",default=10,type=int)

		statuses = api.GetSearch(term='#'+hashtag,count=count)
		

		
		sds = []
		for s in statuses:
			# creates a dictionary representation of the objects
			sd = s.AsDict()
			t = time.strptime(sd['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
			ts = time.strftime('%b %d, %Y', t)
			sd["created_at"]=ts
			# create the status_id_to_reply_count entry
			
			# status_id_to_reply_count["13987198172489"] = 0
			sds.append(sd)

		# status_id_to_reply_count = {
		# 	"13987198172489": 0,
		# 	"12421412412121": 0,
		# 	"89713583275875": 0,
		# }

		# calculate reply count
		# iterate through our mentions
		#	check if the in_reply_to_status_id field is present in our mention
		#		check if that status id is present in our status_id_to_reply_count dict
		#			if it is, we add 1 to the value in the dictionary (using that as the key)
		

		# Pagination
		sds = sds[start:end+1]

		



		# changes python to json
		return jsonify(sds)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		error = str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno)
		return app.response_class(
			response="{'error':'Unable to communicate with Twitter - " + error + "}",
			status=408,
			mimetype='application/json')

# 	count=request.args.get("count",default=50,type=int)
# 	start=request.args.get("start",default=0,type=int)
# 	end=request.args.get("end",default=None,type=int)
# 	statuses = api.GetSearch(term='#'+hashtag,count=count)

# 	statuses = api.GetUserTimeline(screen_name=user,count=count)
# 	mentions = api.GetSearch(term='to:@' + user,count=count)

# 		status_id_to_reply_count = {}

# 		# create a list-of-dicts of mentions
# 		mds =[]
# 		for m in mentions:
# 			md = m.AsDict()
# 			mds.append(md)

# 		sds = []
# 		for s in statuses:
# 			# creates a dictionary representation of the objects
# 			sd = s.AsDict()
# 			t = time.strptime(sd['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
# 			ts = time.strftime('%b %d, %Y', t)
# 			sd["created_at"]=ts
# 			# create the status_id_to_reply_count entry
# 			status_id = sd['id']
# 			# status_id = "13987198172489"
# 			status_id_to_reply_count[status_id] = 0
# 			# status_id_to_reply_count["13987198172489"] = 0
# 			sds.append(sd)

	
# 	# changes python to json
# 	return jsonify(sds)

	

# # reference:https://python-twitter.readthedocs.io/en/latest/twitter.html

# #get_hashtag_timeline("#SpaceX")

# #get_user_timeline("ElonMusk")

