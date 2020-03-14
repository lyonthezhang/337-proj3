#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

import web_scraping
import parse_recipe
import os

app = Flask(__name__)
# ACCESS_TOKEN = 'EAAIG5gF2h3YBABYLooXsrreFI64wimmOQomdORM6XPLpH3kmgeao8QkBu3pMphY46JTMEERZBHajEvlkjhVhPEEzEmVy9wZB62ed1wW4nZCQTN4JCywjHctv7Rsoh4ZBSnnun6941hL5okcGCiB9MhzfCNL4K6r1wZBQpE85jwwZDZD'
# VERIFY_TOKEN = 'HIVICTOR'
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

expletives = ['fart','darn','heck','shut up','stupid','poop']
retrieval_keywords = ['show','get','display','let me see','gimme','give']
enumerations = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelfth']
negation = 'to last'

rf = web_scraping.RecipeFetcher()
res = False
res_index = -1

def remove_punctuation(text):
    text = text.replace(",", "")
    text = text.replace(".", "")
    text = text.replace("-", "")
    return text

def directionNavigator(userinput):
    global res
    global res_index
    global enumerations
    global negation

    counter = 0
    for word in enumerations:
        if word in userinput:
            if negation in userinput:
                res_index = len(res['directions']) - 1 - counter
            else:
                res_index = counter
            return '{}'.format(res['directions'][res_index])
        counter += 1
        if counter == len(res['directions']):
            break

    if 'next' in userinput or 'forward' in userinput:
        res_index += 1
        if res_index >= len(res['directions']):
            res_index = 0
            return 'No more steps buddy. Congrats!'
        return '{}'.format(res['directions'][res_index])

    if 'back' in userinput or 'previous' in userinput:
        res_index -= 1
        if res_index <= 0:
            res_index = 0
            return 'Cannot go before the first step, sadly.'
        return '{}'.format(res['directions'][res_index])

    if 'repeat' in userinput or 'again' in userinput:
        return res['directions'][res_index]

    if 'what' in userinput and 'directions' in userinput:
        directs = res['directions']

        response = 'Here are the directions:\n'
        for i in range(len(directs)):
            response += "Step {}: {}".format(i + 1, directs[i])
        return response

def parseInput(userinput):
    global res

    parsed_res = parse_recipe.parse_recipe(res)
    userinput = remove_punctuation(userinput.lower())

    ingredients = [x['name'] for x in parsed_res['ingredients']]
    parsed_ingredients = list(map(remove_punctuation, ingredients))
    parsed_ingredients = [x.split() for x in parsed_ingredients]
    ingredients_lst = [item for sublist in parsed_ingredients for item in sublist]

    # ingredients retrieval
    for word in expletives:
        if word in userinput:
            return "Please don't say bad words, I was born recently and am legally still a child."

    if 'ingredient' in userinput or 'ingredients' in userinput: # and any([x in userinput for x in retrieval_keywords]):
        response = 'Here is the ingredients list:\n\n'
        for i in res['ingredients']:
            response += i + '\n'
        return response

    if ('direction' in userinput or 'step' in userinput or 'directions' in userinput or 'steps' in userinput):# and any([x in userinput for x in retrieval_keywords]):
        response = directionNavigator(userinput)
        return response

    # 'how to' questions
    parsed_res = parse_recipe.parse_recipe(res)
    if 'how' in userinput:
        objects = parsed_res['methods'] + parsed_res['tools']
        search_url = False
        if any([x in userinput for x in objects]):
            search_base_url = 'https://www.youtube.com/results?search_query=%s'
            search_url = search_base_url % (userinput.replace(' ','+'))
        if search_url:
            return search_url
        else:
            return "That doesn't seem to be a part of this recipe! Please ask related questions only, my brain isn't huge."

    # 'what is' questions
    if 'what' in userinput:
        objects = parsed_res['tools'] + parsed_res['methods'] + ingredients_lst

        #[x['name'] for x in parsed_res['ingredients']]
        search_url = False
        if any([x in userinput for x in objects]):
            search_base_url = 'https://www.google.com/search?q=%s'
            search_url = search_base_url % (userinput.replace(' ','+'))
        if search_url:
            return search_url
        else:
            return "That doesn't seem to be a part of this recipe! Please ask related questions only, my brain isn't huge."

    return "Hmm, I'm sorry, but it seems I'm not smart enough to handle that. Please try asking me something else!"

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    global res

    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                userinput = message.get('message')['text']
                fresh = False
                if res == False:
                    try:
                        bot.send_text_message(recipient_id,"HEY THIS GETS CALLED")
                        res = rf.scrape_recipe(userinput)
                        fresh = True
                        bot.send_text_message(recipient_id,"BUT THIS DOES NOT")
                    except:
                        pass
                #Facebook Messenger ID for user so we know where to send response back to
                if message['message'].get('text'):
                    response_sent_text = get_message(userinput, fresh)
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message(userinput, fresh)
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(userinput, fresh):
    global res
    global res_index

    if res == False:
        return "I need you to input a valid recipe URL: HEY DOES THIS CHANGE"
    else:
        if fresh:
            return "Got the recipe! What would you like for me to do with it?"
        response = parseInput(userinput)
        return response
    # return selected item to the user

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()