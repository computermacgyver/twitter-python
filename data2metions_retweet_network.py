#Twitter json file(s) to mentions/retweets network with networkx

import networkx as nx
try:
    import json
except ImportError:
    import simplejson as json
import codecs
import time
import datetime
import os
import random
import time
import sys


outputDir = "output/" #Output directory
os.system("mkdir -p %s"%(outputDir)) #Create directory if doesn't exist


fhLog = codecs.open("LOG.txt",'a','UTF-8')
def logPrint(s):
	fhLog.write("%s\n"%s)
	print(s)


def parse(graph,tweet):
	author=tweet["user"]["screen_name"]		
	followers=tweet["user"]["followers_count"]
	friends=tweet["user"]["friends_count"]
	location=tweet["user"]["location"]  if tweet["user"]["location"] else ""
	timezone=tweet["user"]["time_zone"] if tweet["user"]["time_zone"] else ""
	utc=tweet["user"]["utc_offset"]  if tweet["user"]["utc_offset"] else ""
	
	other_users=[]
	if "in_reply_to_screen_name" in tweet:
		other_users.append(tweet["in_reply_to_screen_name"])
	
	#tweet["entities"]["user_mentions"][*]["screen_name"]
	if "entities" in tweet and "user_mentions" in tweet["entities"]:
		users=tweet["entities"]["user_mentions"]
		for u in users:
			sn=u["screen_name"]
			if not sn in other_users:
				other_users.append(sn)
	
	try:
		graph.node[author]["tweets"]+=1
	except: #if not author in graph.node:
		graph.add_node(author,{"followers":followers,"friends":friends,"location":location,"timzone":timezone,"utc_offset":utc,"tweets":1})
	
	for target in other_users:
		try:
			graph[author][target]["weight"]+=1
		except:
			graph.add_edge(author,target,weight=1)

graph=nx.DiGraph()			

for file in sys.argv[1:]:
	print(file)
	fhb = codecs.open(file,"r")
	
	firstLine=fhb.readline()
	
	j=json.loads(firstLine)
	if "statuses" in j:
		#We have search API. The first (and only line) is a json object
		for tweet in j["statuses"]:
			parse(graph,tweet)
	else:
		parse(j)
		for line in fhb:
			#We have search API, each line is a json object
			parse(graph,json.loads(line))
	fhb.close()

filename=outputDir+"overall_%s.graphml"%int(time.time())
print("Writing graphml file to {0}...".format(filename))
nx.write_graphml(graph,filename,prettyprint=True)
print("Done.")

