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


#Just used to highlight matches in tweets. This file does not query anything from Twitter!
queries=["term1","term2"] 

outputDir = "output/" #Output directory
os.system("mkdir -p %s"%(outputDir)) #Create directory if doesn't exist


fhLog = codecs.open("LOG.txt",'a','UTF-8')
def logPrint(s):
	fhLog.write("%s\n"%s)
	print(s)


class Tweet:	
	def __init__(self):# word, url, hits, trackback, score, author, text):
		self.keywords=[]
		self.links=["","",""]
		self.lang=""
		self.langConf=""
	
	@staticmethod
	def csvHeader():
		row = "\"\t\"".join(("URL", "Keywords", "Keyword Count", "DateTime", "Favorite Count", "Retweet", "Lang", "LinkCount", "Link1", "Link2", "Link3", "Author", "Text","Followers","Friends","Location","Timezone","UTC Offset"))
		row = "\"%s\"\n"%row
		return row

	def csvRow(self):
		row = "\"\t\"".join((
			str(self.url),
			",".join(self.keywords),
			str(len(self.keywords)),
			#str(datetime.datetime.fromtimestamp(self.date).strftime('%Y-%m-%d %H:%M:%S')),
			str(self.date),
			str(self.favorite),
			str(self.retweet),
			str(self.lang),
			str(self.urlCount),
			self.links[0],
			self.links[1],
			self.links[2],
			self.author,
			self.clean_text(),
			str(self.followers),
			str(self.friends),
			self.location,
			self.timezone,
			str(self.utc)
			))
		row = "\"%s\"\n"%row
		return row
		
	def clean_text(self):
		t = self.text.replace("\"","")
		t = self.text.replace("\n"," ")
		return t
			
	def parse(self,json):
			self.url="http://twitter.com/{0}/status/{1}".format(json["user"]["id_str"],json["id_str"])
			self.date=json["created_at"]
			self.favorite=json["favorite_count"]
			self.retweet=json["retweet_count"]
			self.author=json["user"]["screen_name"]
			#"%s - Twitter"%json["trackback_author_name"] #This is retweet author's name
			self.text=json["text"]
			
			self.lang=json["lang"]
			
			self.followers=json["user"]["followers_count"]
			self.friends=json["user"]["friends_count"]
			self.location=json["user"]["location"]  if json["user"]["location"] else ""
			self.timezone=json["user"]["time_zone"] if json["user"]["time_zone"] else ""
			self.utc=json["user"]["utc_offset"]  if json["user"]["utc_offset"] else ""
			
			#Links
			text = self.text
			self.urlCount = text.count("http://") + text.count("https://")

			count=0
			words=text.split()
			for w in words:
				if w.count("http://") or w.count("https://"):
					w=w[(w.find("http")):]
					w=w.strip("():!?. \t\n\r")
					if count>2:
						self.links[2]=self.links[2]+","+w
					else:
						self.links[count]=w
					count=count+1
						
	def __hash__(self):
		return hash(self.url, self.location)

	def __eq__(self, other):
		return (self.url)==(self.url)

allTweets={}
def parse(tweet):
	tw=Tweet()
	tw.parse(tweet)
			
	if not (tw.url in allTweets):
		txt=tw.text.lower()
		for query in queries:
			if query in txt:
				tw.keywords.append(query)
		#if len(tw.keywords)>0:
		allTweets[tw.url]=tw

fhOverall=None

for file in sys.argv[1:]:
	print(file)
	fhb = codecs.open(file,"r")
	
	firstLine=fhb.readline()
	
	j=json.loads(firstLine)
	if "statuses" in j:
		#We have search API. The first (and only line) is a json object
		for tweet in j["statuses"]:
			parse(tweet)
	else:
		parse(j)
		for line in fhb:
			#We have search API, each line is a json object
			parse(json.loads(line))
	fhb.close()
		
fhOverall=codecs.open(outputDir+"overall_%s.tsv"%int(time.time()),"w","UTF-8")
fhOverall.write(Tweet.csvHeader())
for url in allTweets:
	tweet=allTweets[url]
	fhOverall.write(tweet.csvRow())

fhOverall.close()

logPrint("\nDONE! Completed Successfully")

fhLog.close()
