import json
import traceback
import urlparse
import MySQLdb
import random
import string

from datetime import datetime, timedelta
from celery import Celery
from email_validator import validate_email, EmailNotValidError

from bot import Bot
from nlp.nlp_rivescript import Nlp

#app = Celery('rogu_tasks', backend = 'amqp', broker = 'amqp://')
app = Celery('milki_tasks', backend = 'amqp', broker = 'redis://localhost:6379/4')

LINE_TOKEN=""
DEBUG_MODE = "D" #I=Info, D=Debug, V=Verbose, E=Error
first_name=""

#--OPEN CONFIGURATION (For Linux) --#
# with open('RGCONFIG.txt') as f:
#     content = f.read().splitlines()
# f.close
# LINE_TOKEN=content[0].split('=')[1]

##########OPEN CONFIGURATION#######################
#--Mysql--#
MYSQL_HOST="us-cdbr-iron-east-04.cleardb.net"
MYSQL_USER="b8891eaa7d84f1"
MYSQL_PWD="f5c5dbef"
MYSQL_DB="heroku_a23c62e0062b156"

LINE_TOKEN="sajVouljE8GHl8BAFPcsJfy/Zy0GTPtubgsYQlkB+YQCT4pHawfMnIWUthlf00OfWlqo21sKbtQa2okJ3UCkYMqsm+zSV9HOVnMRDNVnREEcxoD/7BJQdjm/1ppdjhBrkfEAZwOg+/cj0ebV6ErjdQdB04t89/1O/w1cDnyilFU="
linebot = Bot(LINE_TOKEN)
lineNlp = Nlp()

#=============================================== Function Addon ===============================================#
def request(sql):
    try:
        db_connect = MySQLdb.connect(host = MYSQL_HOST, port = 3306, user = MYSQL_USER, passwd = MYSQL_PWD, db = MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        sqlout = cursor.fetchall()

        return sqlout
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def insert(sql):
    try:
        db_connect = MySQLdb.connect(host = MYSQL_HOST, port = 3306, user = MYSQL_USER, passwd = MYSQL_PWD, db = MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def update(sql):
    try:
        db_connect = MySQLdb.connect(host = MYSQL_HOST, port = 3306, user = MYSQL_USER, passwd = MYSQL_PWD, db = MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def delete(sql):
    try:
        db_connect = MySQLdb.connect(host = MYSQL_HOST, port = 3306, user = MYSQL_USER, passwd = MYSQL_PWD, db = MYSQL_DB)
        # Create cursor
        cursor = db_connect.cursor()
        cursor.execute(sql)
        db_connect.commit()
    except MySQLdb.Error, e:
        logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
        print e.args
        print "ERROR: %d: %s" % (e.args[0], e.args[1])

def create_katalog(msisdn):

    sql = "SELECT * FROM barang"
    sqlout = request(sql)

    columns = []
    for row in sqlout:
        id_brg = row[0]
        rasa = row[1]
        harga = row[3]
        img = row[5]

        column = {}
        column['thumbnail_image_url'] = img
        column['title'] = rasa.upper()
        column['text'] = formatrupiah(harga)
        column['actions'] = [
            {'type': 'postback', 'label': 'Lihat Katalog', 'data': 'evt=katalog&id_brg=' + str(id_brg)},
            {'type': 'postback', 'label': 'Order', 'data': 'evt=order&id_brg=' + str(id_brg)}
        ]
        columns.append(column)

    return columns

def chartshop(msisdn):
    sql = "SELECT a.msisdn as msisdn,b.rasa as rasa,COUNT(b.id_brg) as total_brg,SUM(b.harga) as total_harga,a.id_brg as id_brg from chart_shop a INNER JOIN barang b on a.id_brg = b.id_brg where msisdn = '" + msisdn + "' group by msisdn,rasa,id_brg"
    sqlout = request(sql)

    sum_price = 0
    checkout_msg = "Keranjang Belanja Kamu :\n"
    checkout_msg += "=====================\n"
    for row in sqlout:
        item_name = row[1]
        count_item = row[2]
        price = row[3]
        sum_price = sum_price + price

        checkout_msg += item_name + " = " + str(count_item) + "\n"

    checkout_msg += "\nTotal Harga = " + str(formatrupiah(int(sum_price)))

    linebot.send_composed_confirm(
        msisdn, 'confirm_checkout', checkout_msg,
        {'label': 'Beli', 'type': 'postback', 'data': 'evt=beli'},
        {'label': 'Batal', 'type': 'postback', 'data': 'evt=cancelorder'}
    )

def cancelorder(msisdn):
    sql = "delete from chart_shop where msisdn = '" + msisdn + "'"
    delete(sql)

def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3 :
        return 'Rp ' + y
    else :
        p = y[-3:]
        q = y[:-3]
        return   formatrupiah(q) + '.' + p
        print 'Rp ' +  formatrupiah(q) + '.' + p

#=============================================== Function Worker ===============================================#

def onMessage(msisdn,ask,param):

    logDtm = (datetime.now() + timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
    print "--- Send asking to rivescript and get answer --->",logDtm,msisdn,ask

    status = lineNlp.redisconn.get("milkibot/%s/status" % (msisdn))

    if status == 'email_order':
        email = ask
        try:
            v = validate_email(email)
            email = v["email"]
            lineNlp.redisconn.set("milkibot/%s/orderemail" % (msisdn), email)
            answer = lineNlp.doNlp('email', msisdn, param)
        except EmailNotValidError as e:
            answer = lineNlp.doNlp(ask, msisdn, param)
    elif status == 'phone_order':
        try:
            phone = int(ask)
            lineNlp.redisconn.set("milkibot/%s/orderphone" % (msisdn), phone)
            answer = lineNlp.doNlp('phone', msisdn, param)
        except ValueError:
            answer = lineNlp.doNlp(ask, msisdn, param)
    elif status == 'pic_order':
        lineNlp.redisconn.set("milkibot/%s/orderpic" % (msisdn), ask)
        answer = lineNlp.doNlp(ask, msisdn, param)
    else:
        answer = lineNlp.doNlp(ask, msisdn, param)

    print answer

    #==== Statement Menu Milki ====#
    if answer[:7] == "mnMilki":
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'menu_milki')

        linebot.send_text_message(msisdn, answer[7:])
        linebot.send_text_message(msisdn, "Niih milki kasih varian susu sapi segar yang cocok banget buat kamu. Atau mau langsung cobain kalo gk percaya.")
        # linebot.send_carousel(msisdn, 'menu_minsu')
        linebot.send_composed_carousel(msisdn, "katalog_minsu", create_katalog(msisdn))
        print "-- answer reply send -->", answer, answer[:7]

    #==== Statement Order ====#
    elif answer[:7] == "mnOrder":
        id_brg = param

        # ----- Add item to chart -----#
        sql = "insert into chart_shop values('" + msisdn + "','" + id_brg + "')"
        insert(sql)
        chartshop(msisdn) #--> Display shoping chart

    #==== Statement Menu Katalog ====#
    elif answer[:9] == 'mnKatalog':
        id_brg = param

        sql = "SELECT description FROM barang where id_brg=%s" % (id_brg)
        sqlout = request(sql)

        for row in sqlout:
            description = row[0]
            linebot.send_text_message(msisdn, description)

    #==== Statement Shoping Chart ====#
    elif answer[:5] == 'mnBuy':

        sql = "SELECT c.id_brg as id_brg,c.rasa as rasa,c.stock as stock,(c.stock-c.tot_req) as status_stock FROM ( select a.id_brg as id_brg,b.rasa as rasa,b.stock as stock,count(*) as tot_req from chart_shop a INNER JOIN barang b on a.id_brg = b.id_brg WHERE a.msisdn = '" + msisdn + "' group by 1,2,3 ) c"
        sqlout = request(sql)

        empty_stock = []
        for row in sqlout:
            id_brg = row[0]
            rasa = row[1]
            stock = row[2]
            status_stock = int(row[3])

            if (status_stock < 0):
                empty_stock.append({'id': id_brg, 'rasa': rasa, 'stock': stock})
                sql = "delete from chart_shop where msisdn = '" + msisdn + "' and id_brg = '" + id_brg + "'"
                delete(sql)

        if not empty_stock:
            lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'location_order')

            onMessage(str(msisdn), 'belisuccess', first_name)
            # message = "Untuk pemesanannya mau dikirim kemana ?\nShare loc aja ya kak.."
            # linebot.send_text_message(msisdn, message)
        else:
            alert_msg = "Maaf kak, stock minsu untuk rasa :\n"
            for row in empty_stock:
                alert_msg += row['rasa'] + " (tinggal " + row['stock'] + ")\n"

            alert_msg += "\nuntuk tuker rasa lain , langsung pilih aja ya kak.."
            linebot.send_text_message(msisdn, alert_msg)
            linebot.send_composed_carousel(msisdn, "katalog_minsu", create_katalog(msisdn))
            chartshop(msisdn)

    # ==== Statement Shoping Chart ====#
    elif answer[:12] == 'mnBuySuccess':
        message = "Untuk pemesanannya mau dikirim kemana ?\nShare loc aja ya kak.."
        linebot.send_text_message(msisdn, message)

    #==== Statement Asking Location ====#
    elif answer[:4] == 'uLoc':
        lineNlp.redisconn.set("milkibot/%s/orderloc" % (msisdn), str(param))
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'pic_order')

        message = "Untuk pesanannya atas nama siapa kak ?"
        linebot.send_text_message(msisdn, message)

    # ==== Statement Asking Location ====#
    elif answer[:5] == 'uMail':
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'phone_order')

        message = "Share nomer telponnya ya kak.."
        linebot.send_text_message(msisdn, message)

    # ==== Statement Asking Email ====#
    elif answer[:5] == 'nmPic':
        lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'email_order')

        message = "Untuk proses pemesanan, masukin emailnya ya kak.."
        linebot.send_text_message(msisdn, message)

    #==== Statement Asking Pic Order ====#
    elif answer[:6] == 'uPhone':
        sql = "SELECT a.msisdn as msisdn,b.rasa as rasa,COUNT(b.id_brg) as total_brg,SUM(b.harga) as total_harga,a.id_brg as id_brg from chart_shop a INNER JOIN barang b on a.id_brg = b.id_brg where msisdn = '" + msisdn + "' group by msisdn,rasa,id_brg"
        sqlout = request(sql)

        picorder = lineNlp.redisconn.get("milkibot/%s/orderpic" % (msisdn))
        locorder = lineNlp.redisconn.get("milkibot/%s/orderloc" % (msisdn))
        emailorder = lineNlp.redisconn.get("milkibot/%s/orderemail" % (msisdn))
        phoneorder = lineNlp.redisconn.get("milkibot/%s/orderphone" % (msisdn))

        checkout_msg = "Untuk pesanan minsunya mohon dicek kembali ya kak..\n"
        checkout_msg += "- Nama Pemesan : " + picorder + "\n"
        checkout_msg += "- Email : " + emailorder + "\n"
        checkout_msg += "- Phone Number : " + phoneorder + "\n"
        checkout_msg += "- Detail Order :\n"

        sum_price = 0
        for row in sqlout:
            item_name = row[1]
            count_item = row[2]
            price = row[3]
            sum_price = sum_price + price

            checkout_msg += "   - " + item_name + " = " + str(count_item) + "\n"

        checkout_msg += "- Alamat Pengiriman : " + locorder
        checkout_msg += "\n======================="
        checkout_msg += "\nTotal Harga = " + str(formatrupiah(int(sum_price)))
        lineNlp.redisconn.set("milkibot/%s/orderprice" % (msisdn), sum_price)

        linebot.send_text_message(msisdn, checkout_msg)
        linebot.send_composed_confirm(
            msisdn, 'confirm_checkout', 'Tekan "beli" untuk konfirmasi pemesanan. Tekan "cancel" untuk membatalkan pesanan.',
            {'label': 'Beli', 'type': 'postback', 'data': 'evt=finbuy'},
            {'label': 'Cancel', 'type': 'postback', 'data': 'evt=cancelorder'}
        )

    #==== Statement Confirmation Order  ====#
    elif answer[:4] == 'uBuy':
        picorder = lineNlp.redisconn.get("milkibot/%s/orderpic" % (msisdn))
        locorder = lineNlp.redisconn.get("milkibot/%s/orderloc" % (msisdn))
        emailorder = lineNlp.redisconn.get("milkibot/%s/orderemail" % (msisdn))
        phoneorder = lineNlp.redisconn.get("milkibot/%s/orderphone" % (msisdn))
        priceorder = lineNlp.redisconn.get("milkibot/%s/orderprice" % (msisdn))
        unique_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        insert_order = "insert into `order` (id_order,nama,tgl,lokasi,status_payment,harga,email,phone) values('"+ unique_id +"','"+ picorder +"',CONVERT_TZ(NOW(),'+00:00','+07:00'),'"+ locorder +"',1,'"+priceorder+"','"+ emailorder +"','"+ phoneorder + "')"
        insert(insert_order)
        insert_tracker = "insert into `tracker` (id_order,datetime,status,description) values('" + unique_id + "',CONVERT_TZ(NOW(),'+00:00','+07:00'),'waiting payment','')"
        insert(insert_tracker)

        sql = "SELECT id_brg from chart_shop where msisdn = '"+ msisdn +"'"
        sqlout = request(sql)
        for row in sqlout:
            id_brg = row[0]
            insert_detorder = "insert into `detail_order` (id_order,id_brg) values('" + unique_id + "','" + id_brg + "')"
            insert(insert_detorder)
            update_stock = "UPDATE barang SET stock=stock-1 where id_brg = '" + id_brg +"'"
            update(update_stock)

        trunc_chart = "delete from chart_shop where msisdn = '" + msisdn + "'"
        delete(trunc_chart)

        linktracker = "https://milki.herokuapp.com/tracker/status/" + str(unique_id)

        message = "Terima kasih pesanannya segera kita proses. Untuk melakukan pembayaran dan memantau pesanan anda, klik aja link berikkut ya kak.\n" + linktracker
        linebot.send_text_message(msisdn, message)

    #==== Statement CancelOrder ====#
    elif answer[:9] == 'ordCancel':
        cancelorder(msisdn)
        linebot.send_text_message(msisdn, answer[9:])

    else:
        linebot.send_text_message(msisdn, answer)

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
                    if contentType == 'location':
                        onMessage(str(msisdn), contentType, address)
                    else:
                        onMessage(str(msisdn), ask,first_name)
                except Exception as e:
                    # print e
                    traceback.print_exc()
                    print "ERROR HAPPEN!!!"
                    lineNlp.redisconn.set("milki-status/%s" % (msisdn), 0)
                    lineNlp.redisconn.delete("milki-users/%s" % (msisdn))
        elif event["type"] == "postback":
            msisdn = str(event["source"]["userId"])
            parsed = urlparse.urlparse('?' + event["postback"]["data"])
            postback_event = urlparse.parse_qs(parsed.query)['evt'][0]

            if (postback_event == 'order'):
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'order')

                id_brg = urlparse.parse_qs(parsed.query)['id_brg'][0]
                onMessage(str(msisdn),'order',id_brg)

            #-- Checkout Order --#
            elif (postback_event == 'beli'):
                lineNlp.redisconn.set("milkibot/%s/status" % (msisdn), 'checkout order')

                onMessage(str(msisdn), 'beli', first_name)

            elif (postback_event == 'katalog'):
                id_brg = urlparse.parse_qs(parsed.query)['id_brg'][0]
                onMessage(str(msisdn), 'katalog', id_brg)

            elif (postback_event == 'finbuy'):
                onMessage(str(msisdn), 'finbuy', first_name)

            elif (postback_event == 'cancelorder'):
                onMessage(str(msisdn), 'cancelorder', first_name)
