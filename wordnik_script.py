from wordnik import*
import praw
import time
# setting up wordnik API
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'YOUR WORDNIK API KEY HERE'
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

#setting up reddit API
r = praw.Reddit (user_agent='HELPFUL INFO HERE')
r.login('REDDIT USERNAME', 'REDDIT PASSWORD')
subreddits = r.get_subreddit('test') # defines which subreddits to crawl
subreddits_comments = subreddits.get_comments() #s separates out flattened comments





def gather_definitions(word): # takes a string

    definition = wordApi.getDefinitions(word,useCanonical="True",)
    Y=0
    speech_used=[]
    
    # for loop that iterates list and parts of speech
    for x in range(len(definition)):
    	
        if Y < (len(definition)-1):
            if definition[Y].partOfSpeech not in speech_used:            
                speech_used.append(definition[Y].partOfSpeech)
                # this formats a string for reddit markdown and appends to a list
                definitions_list.append("- " + "**"+definition[Y].word+"**: *"+definition[Y].partOfSpeech+"* "+definition[Y].text)
            Y+=1


# removes the word from the body
def word_remover(body):
    first_pass = body.split("define ",1)[1]
    word = first_pass.replace(".","")
    return word





# formats the comment with bold and italics
def comment_formatter(word):
# not necessarily final
    gather_definitions(word)
    Z=0
    response=""
    # prints list, more for purposes of class display
    for W in range(len(definitions_list)):
    	if Z <= (len(definitions_list)-1):
    	    response += definitions_list[Z]
    	    Z += 1
    	else:
    	    break
    return response



cache=[] # to prevent doing the same work many times
keep_alive= True # keeps the program running
while (keep_alive):

    for submission in subreddits_comments:
        if submission.id not in cache:
            if "wordnik_bot" in submission.body.lower():
            	body = submission.body
            	word = word_remover(body)
            	definitions_list=[]
            	response = comment_formatter(word)
            	submission.reply(response)
            	cache.append(submission.id)
    time.sleep(1800) # sleep and re-loop
