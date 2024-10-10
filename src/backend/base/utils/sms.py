import requests
import json

from decouple import config


def send_sms(phone_no, body):
    is_sent = False
    result = {'detail': 'Unable to sent, please try again later'}
    try:
        res = requests.get(config('SMS_URL'),
                           params={'user': config('SMS_USERNAME'),
                                   'pwd': config('SMS_PASSWORD'),
                                   'mobileno': phone_no,
                                   'text': body,
                                   'sender': config('SMS_SENDER_ID'),
                                   'response': 'json'})
        result = json.loads(res.content)
        is_sent = True
    except Exception as e:
        print(e)
    return is_sent, result
