import json
import traceback
from datetime import datetime, timedelta

from celery import Celery

from bot import Bot
from nlp.nlp_rivescript import Nlp

#app = Celery('rogu_tasks', backend = 'amqp', broker = 'amqp://')
app = Celery('rogu_tasks', backend = 'amqp', broker = 'redis://localhost:6379/4')

LINE_TOKEN=""
DEBUG_MODE = "D" #I=Info, D=Debug, V=Verbose, E=Error
first_name=""

#--OPEN CONFIGURATION (For Linux) --#
# with open('RGCONFIG.txt') as f:
#     content = f.read().splitlines()
# f.close
# LINE_TOKEN=content[0].split('=')[1]

LINE_TOKEN="/IH+xie4ZI3UKUPxLJtOXhqPaVAp4ovgvTr2CGM9WX3xIpA+N+gNW82ip/Z7m8gfy+z7bnDUrCa9DmgG+8Zc+5/hg1KqpVDRUMOvYAWRW2gZ4krgE95VdlVrivLTYou8B6i72fzq0pF/KdrlWryTFgdB04t89/1O/w1cDnyilFU="
linebot = Bot(LINE_TOKEN)
lineNlp = Nlp()

def onMessage(replyToken,ask,first_name):

    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    print "--- Send asking to rivescript and get answer --->",logDtm,replyToken,ask

    answer = lineNlp.doNlp(ask, replyToken, first_name)

    print answer
    linebot.send_text_message(replyToken, answer)

@app.task(ignore_result=True)
def doworker(req):
    content = json.dumps(req)
    content = json.loads(content)
    print ""
    print "================================ INCOMING LINE MESSAGE REQUEST ============================================="
    print content

    if not content.has_key('events'):
        return

    for event in content["events"] :
        msisdn = ""
        ask = ""
        longitude = ""
        latitude = ""
        contentType = 0
        first_name = ""
        replyToken = ""

        try:
            if event["type"] == "message":
                contentType = event["message"]["type"]
                msisdn = str(event["source"]["userId"])
                replyToken = str(event["replyToken"])

                if contentType == "text":
                    ask = str(event["message"]["text"])
                    print "--- Message Type : Text ---", ask
                elif contentType == "location":
                    longitude = event["message"]["longitude"]
                    latitude = event["message"]["latitude"]
                    address = event["message"]["address"]
                    print "--- Message Type : Location ---", longitude, latitude, address
                elif contentType == "sticker":
                    sticker = event["message"]["packageId"]
                    stickerid = event["message"]["stickerId"]
                    print "--- Message Type : Sticker ---", sticker, stickerid
                elif contentType == "image":
                    print "--- Message Type : Image ---"
                else:
                    print "--->"+contentType.capitalize()
            else:
                opType = event["type"]
                if event["source"].has_key('userId'):
                    msisdn = str(event["source"]["userId"])
                elif event["source"].has_key('groupId'):
                    msisdn = str(event["source"]["groupId"])
                print "-->", opType, msisdn

        except:
            opType = content["result"][0]["content"]["opType"]
            msisdn = str(content["result"][0]["content"]["params"][0])
            print "-->", opType, msisdn

        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')

        if event["type"] == "message":
            if contentType == "text" or contentType == "location":  # request text location
                print "<<-- Incoming Message -->>", logDtm, msisdn, ask, replyToken, longitude, latitude,
                incomingClient = lineNlp.redisconn.get("status/%s" % (msisdn))

                #print incomingClient

                if incomingClient is None:
                    lineNlp.redisconn.set("status/%s" % (msisdn), 0)
                    incomingClient = "0"
                if longitude != "":
                    ask = "[LOC]" + str(latitude) + ";" + str(longitude)
                    print "<<-- Incoming Message -->>", longitude, ask
                try:
                    print 'replyToken : ' + replyToken
                    onMessage(str(replyToken), ask,first_name)
                    lineNlp.redisconn.set("status/%s" % (msisdn), 0)
                except Exception as e:
                    # print e
                    traceback.print_exc()
                    print "ERROR HAPPEN!!!"
                    lineNlp.redisconn.set("status/%s" % (msisdn), 0)
                    lineNlp.redisconn.delete("rs-users/%s" % (msisdn))