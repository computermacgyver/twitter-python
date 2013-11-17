twitter-python
==============

Simple example scripts for Twitter data collection with [Tweepy](http://www.github.com/tweepy/tweepy) in Python

#Getting started
To collect data you need a Twitter account and a Twitter application. Assuming you already have a Twitter account use the following instructions to create a Twitter application

##Twitter application

1. Open a web browser and go to http://dev.twitter.com/
2. Click “Sign in” in the top right corner and sign in with your normal Twitter username and password
3. Hover on your username in the top-right corner and click "My Applications"
4. Click the "Create a new application" button
5. Read and accept the terms and conditions – note principally that you agree not to distribute any of the raw tweet data and to delete tweets from your collection if they should be deleted from Twitter in the future.
6. Enter a name, description, and temporary website (e.g. http://coming-soon.com)
7. Read and accept the developer rules of the road, enter the CAPTCHA
8. Click "Create your Twitter application"
9. Scroll to the bottom of the page and click "Create my access token"
10. Wait a minute or two and press your browser's refresh button (or ctrl+r / cmd+r)
11. You should now see new fields labeled "Access token" and "Access token secret" at the bottom of the page.
12. You now have a Twitter application that can act on behalf of your Twitter user to read data from Twitter.

##Connect your Twitter application to these scripts
1. Download the code in the repository if you haven't already
2. Open the auth_example.py file in a text editor (gedit, kate, notepad, textmate, etc.)
3. Update the following lines with the information displayed in the web browser for your application: 
   consumer_key="..."
   consumer_secret="..."
   access_token="..." 
   access_token_secret="...."
   #Replace the … with whatever values are shown in your web browser. Be sure to keep the quotation marks.
4. Save the file as auth.py (not the same name as before)

You are now ready to run a simple example.

##First run (streaming_simple.py)
1. Open your terminal/console and go to the folder you saved the files (e.g. cd "/absolute path/to/my/files")
2. Run streaming_simple.py by typing
   python streaming_simple.py
3. You should see text of tweets appearing. Press ctrl+c to stop collecting tweets.

If you do not see tweets appearing, check that you have [Tweepy](http://www.github.com/tweepy/tweepy) installed correctly and that the information in auth.py is correct.

In addition to printing out the text of tweets, streaming_simple.py also saves the results to output.json

##Convert json to csv (json2tsv.py) -- Coming soon
Twitter supplies tweets in JSON format. See the [Twitter documentation](https://dev.twitter.com/docs/platform-objects/tweets) for what fields are available. To create a spreadsheet of collected tweets, we can select certain fields and include these. This is what the json2csv.py file does.

The following steps assume you've run either streaming_simple.py or streaming.py and have file(s) of tweets with one tweet per line.

1. Open the terminal/console and go to the folder with the files
2. Run the following (assuming output.json is name of the file with tweets)
   python json2tsv.py output.json
3. This will produce output.tsv which can be opened in OpenOffice Calc, Excel, etc. If prompted select that columns (fields) are separated with a tab character.

##Production (streaming.py)
streaming.py is a more production ready file. It does not print tweets as they are recieved, but simply stores them to a files with the name of the day they are recieved on. It starts a new file at midnight every day. It also has additional error checking / recovery code.

1. Create a directory (folder) to store the tweets in
2. Within the directory, create a file called FILTER (all uppercase)
3. Open FILTER in a text editor and enter the terms you wish to track one per line. Save and close it.
4. Open streaming.py and set the name of the directory you created
5. Copy streaming.py, the output directory (outputDir), tweepy, and anything else to a server that is always on and connected
6. Start collecting tweets with
    nohub python streaming.py
    

