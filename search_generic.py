try:
    import json
except ImportError:
    import simplejson as json
import urllib2
import urllib
import codecs
import time
import datetime
import os
import random
import time
import tweepy
from tweepy.parsers import RawParser
import sys
#import cld

fhLog = codecs.open("LOG.txt",'a','UTF-8')
def logPrint(s):
	fhLog.write("%s\n"%s)
	print s

#Update this line with the terms you want to search for
terms =  ["term1","term2","term3"]


from auth import TwitterAuth

auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

rawParser = RawParser()
api = tweepy.API(auth_handler=auth, parser=rawParser)

fhOverall=None
allTweets = {}

termCnt=0
for term in terms:
	termCnt+=1
	logPrint("Getting term %s (%s of %s)"%(term,termCnt,len(terms)))
	minid=None #Lowest id we've seen so far, start at None
	count=1
	while True:
		try:
			fh=open("output/"+term+"_" + str(count) + ".json","r")
			result=fh.read()
			fh.close()
			wait=0
		except:	
			if minid==None:
				result=api.search(count=100,q=term,result_type="recent")
			else:
				result=api.search(count=100,q=term,max_id=minid,result_type="recent")
			#The following will produce errors if the filesystem doesn't support characters used in the search term! (also above in try block)
			fh=open("output/"+term+"_" + str(count) + ".json","w")
			fh.write(result)
			fh.close()
			wait=5
			
		result=json.loads(result)
		if "statuses" in result and len(result["statuses"])>0:
			logPrint("\nThere are %s results."%len(result["statuses"]))
			for status in result["statuses"]:
				if minid==None or status["id"]<minid:
					minid=status["id"]
			count+=1
			logPrint("Another page to get. Minimum id is %s"%minid)
		else:
			minid=None
			break
		
		#Deal with slight bug, if <=1 also quit
		if "statuses" in result and len(result["statuses"])<=1:
			minid=None
			break

		
		time.sleep(wait)

logPrint("\nDONE! Completed Successfully")
fhLog.close()
