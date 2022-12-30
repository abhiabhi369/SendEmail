import pandas as pd
from datetime import datetime
import pytz
import requests
import time
import re
import smtplib
from email.mime.text import MIMEText

create = open('test.txt','w')
file = open('test.txt','a')

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False


def sendText(Number,Text,Country):
    endpoint = 'https://api.txtbox.in/v1/sms/send'
    headers = {
        'apiKey': "9f81fddf27be1aa3e73a0619392cbc0c",
        'content-type': "application/x-www-form-urlencoded",
    }
    payload = {
        'sms_text': Text,
        'sender_id': 'smsMagic',
        'mobile_number': Number
    }
    if (len(Text)>1 and len(Text)<=160) and len(str(Number)) == 10:
        t = time.localtime()
        current_time = time.strftime("%H", t)
        if Country == 'INDIA':
            if int(current_time)>10 and int(current_time)<17:
                print('everything is fine we can send message now')
                res = requests.post(url=endpoint,data=payload,headers=headers)
                print('res',res)
                if res.json()['status'] == 'submitted':
                    file.write('SMS sent successfully\n')
                    return True
                else:
                    file.write('SMS sent failed\n')
                    return False
            else:
                print('cannot send text in this time')
                file.write('cannot send text in this time\n')
                return False
        else:
            Us_time = datetime.now(pytz.timezone('America/New_York'))
            Hour = Us_time.strftime("%H")
            if int(Hour)>10 and int(Hour)<17:
                print('everything is fine now we can send message now')
                res = requests.post(url=endpoint, data=payload, headers=headers)
                print('res', res)
                if res.json()['status'] == 'submitted':
                    file.write('Text sent successfully')
                    return True
            else:
                print('cannot send text in this time')
                file.write('cannot send text in this time\n')
                return False
    else:
        file.write('Length of message is invalid')
        return 'Length not valid'


def sendEmail(Email,Text):
    msg = MIMEText(_text=Text)
    msg['Subject'] = 'Hello Abhi'
    msg['From'] = 'abhilashgangula370@gmail.com'
    msg['To'] = Email

    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('abhilashgangula370@gmail.com','thnmrfzpklvmebvb')
    print('login')
    try:
        server.send_message(msg,'abhilashgangula370@gmail.com',Email)
        file.write('Email sent successfully, ')
        return True
    except Exception as e:
        file.write(str(e)+' ')
        print(e)
        return e

def dateFormate(Schedule):
    original_schedule = Schedule[:-2] + '20' + Schedule[-2:]
    dat = original_schedule[:2]
    month = original_schedule[3:5]
    year = original_schedule[6:]
    return year+'/'+month+'/'+dat

def ReadCsvv(path):
    df = pd.read_csv(path)
    for i in range(len(df)):
        Email = df.iloc[i]['Email']
        Number = df.iloc[i]['Phone']
        Text = df.iloc[i]['Message']
        Country = df.iloc[i]['Country']
        Schedule = df.iloc[i]['Schedule On']
        original_schedule = dateFormate(Schedule)
        current_date = datetime.today().strftime('%Y/%m/%d')
        file.write(str(i)+') '+Email+'  ')
        print(original_schedule,current_date)
        if original_schedule<current_date:
            print('in if........')
            file.write('schedule date is future cannot send message\n')
            continue
        else:
            print('in else......')
            is_valid = isValid(Email)
            print('is_valid',is_valid)
            if is_valid:
                email_res = sendEmail(Email,Text)
            else:
                file.write('Email is not valid, ')
                print('Email is not valid one')
            text_res = sendText(Number, Text, Country)

# path = "C:/Users/abhi/OneDrive/Desktop/Sample.csv"
path = input('Please enter path of the csv file: ').replace('\\','/')
print(path)
ReadCsvv(path)




