from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
import json
import html2text
from datetime import datetime
import threading
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

from .models import Batch
def sendMessage(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            email = request.user.email
            message = request.POST['textarea']
            telegramFlag = request.POST['telegramFlag']
            mailFlag = request.POST['mailFlag']            
            if not message:
                messages.error(request, "Please enter a message to send!")
                return redirect("sendMessage")
            elif telegramFlag == "false" and mailFlag == "false":
                messages.error(request, "Please a social media to send!")
                return redirect("sendMessage")
            else:
                h = html2text.HTML2Text()
                plainText = h.handle(message)
                if telegramFlag == "true" and mailFlag == "true":
                    mediaType = "BOTH"
                elif telegramFlag == "true" and mailFlag == "false":
                    mediaType = "Telegram"
                else:
                    mediaType = "Mail"
                if telegramFlag == "true":
                    try:                  
                        t1 = threading.Thread(target=send_to_telegram,kwargs={"emailId":email, "text":plainText, "mediaType":mediaType})
                        t1.setDaemon(True)
                        t1.start()  
                        messages.info(request, "Successfully sent Telegram message!")
                    except Exception as e:
                        logger.debug("Error sending message through Telegram : {}".format(e))
                        return HttpResponse(e)
                if mailFlag == "true":
                    try:              
                        subject = request.POST['mailSubject']    
                        receiver_email = []
                        receiver_email.append("dineshkarthik1606@gmail.com")
                        receiver_email.append(request.POST['receiverEmailID'])
                        t2 = threading.Thread(target=send_to_mail,kwargs={"sender_email":email, "receiver_email":receiver_email, "sender_password":"fpepfgyhwgpkyxsa", "subject":subject, "body":plainText, "mediaType":mediaType})
                        t2.setDaemon(True)
                        t2.start()    
                        messages.info(request, "Successfully sent message!")
                    except Exception as e:
                        logger.debug("Error sending message through Mail : {}".format(e))
                        return HttpResponse(e)                
                return redirect("sendMessage")
        else:
            messages.info(request, "Please login to send message")
            
    else:
        return render(request, "sendMessage.html")

def send_to_telegram(emailId, text=None, image=None, mediaType="Telegram"):

    credentials_path = settings.CONFIG['telegram']
    apiToken = credentials_path['apiToken']
    chatID = credentials_path['chatID']
    
    # Send 'photo' using below url and add 'caption' parameter in the post request for image with text
    photoApiURL = f'https://api.telegram.org/bot{apiToken}/sendPhoto'

    # Send message using below url and use 'text' parameter to send text message instead of caption
    textApiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(textApiURL, json={'chat_id': chatID, 'text': text})
        print(response)
        batchDetails = {}        
        batchDetails['sender'] = emailId
        batchDetails['message'] = response.json()['result']['text'] if response.status_code == 200 else None
        batchDetails['time'] = datetime.now()
        batchDetails['mediaType'] = mediaType
        batchDetails['status'] = "success" if response.status_code == 200 else "failure"
        batchDetails['statusCode'] = response.status_code
        batchDetails['groupName'] = response.json()['result']['chat']['title'] if response.status_code == 200 else None
        batchDetails['messageID'] = response.json()['result']['message_id'] if response.status_code == 200 else None
        batchDetails['chatID'] = response.json()['result']['chat']['id'] if response.status_code == 200 else None
        batchDetails['errorCode'] = response.json()['error_code'] if response.status_code != 200 else None
        batchDetails['errorDescription'] = response.json()['description'] if response.status_code != 200 else None
        batch = Batch(**batchDetails)
        print(batchDetails)
        batch.save()
        logger.info("Saved batch to DB successfully")

    except Exception as e:
        logger.debug("Error sending message through Telegram : {}".format(e))
        print(e)

def send_to_mail(sender_email, receiver_email, sender_password, subject, body, mediaType="Mail"):
     
    try:
        import random
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        batchDetails = {}   
        batchDetails['messageID'] = random.randint(1, 1000000)
        batchDetails['chatID'] = random.randint(1, 1000000)

        for mailId in receiver_email:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = mailId
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            smtp_server = 'smtp.gmail.com'
            smtp_port = 587  
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)        
            server.sendmail(sender_email, mailId, msg.as_string())
            server.quit()

        logger.info("Message sent through mail successfully")
        batchDetails['status'] = "success"
        batchDetails['statusCode'] = 200
        batchDetails['errorCode'] = None
        batchDetails['errorDescription'] = None

    except Exception as e:
        logger.debug("Error sending message through Mail : {}".format(e))
        batchDetails['status'] = "failure"
        batchDetails['statusCode'] = 535
        batchDetails['errorCode'] = 535
        batchDetails['errorDescription'] = e

    else:
        batchDetails['sender'] = sender_email
        batchDetails['message'] = body
        batchDetails['time'] = datetime.now()
        batchDetails['mediaType'] = mediaType
        batchDetails['groupName'] = ' '.join([str(mailId) for mailId in receiver_email])        
        batch = Batch(**batchDetails)
        print(batchDetails)
        batch.save()
        logger.info("Saved batch to DB successfully")
