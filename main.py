#!/usr/bin/env python
import os
from dotenv import load_dotenv
import schedule
import time
from bs4 import BeautifulSoup
import requests
import urllib3


def send_with_mailtrap(sender_email, receiver_email, subject, text):
    import smtplib
    from email.mime.text import MIMEText
    
    # Mailtrap Configuration
    port = 587 
    # Your Mailtrap password
    
    # Create email
    message = MIMEText(text, "plain")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email if isinstance(receiver_email, str) else ", ".join(receiver_email)
    
    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def hlavni_ukol():

    url = "https://nase-ambulance.cz/nsRezervace/NwfRezervace.aspx?cl=101"




    requests.packages.urllib3.disable_warnings()
    # requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    r=requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser') 
    table = soup.find('span',string='MUDr. Golla').find_all_next('input')
    #table = soup.find('span',string='MUDr. Oslizlová').find_all_next('input')
    volne_terminy = []
    for elem in table:
        if not elem.attrs['value']=='další týden >':
            if not elem.attrs['disabled']=='disabled':
                volne_terminy.append(elem.attrs['value'])

    if volne_terminy != []:
        send_with_mailtrap("admin@iservery.cz", "admin@iservery.cz", "Volné termíny Gola", str(volne_terminy))



load_dotenv()

smtp_server = os.getenv('smtp_server')
login = os.getenv('login')  
password = os.getenv('password') 

schedule.every().hour.do(hlavni_ukol)


while True:
    schedule.run_pending()
    time.sleep(1)