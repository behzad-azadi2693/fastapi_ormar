from datetime import timedelta, datetime
from kavenegar import *
from config.settings import SENDING_NUMBER, API_KEY
import json
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi import Depends, Form, Request
from .models import UserModel
from .schema import UserSchema
from config.settings import SECRET_KEY
import jwt


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/accounts/signin')


def send_sms(phone, otp):

    api = KavenegarAPI(API_KEY, timeout=20)
    params = {
        'sender': SENDING_NUMBER,
        'receptor': phone,
        'message': f'otp  for sigin in site: {otp}'
    }   

    api.sms_send(params)



def check_user_healthy(otp, sms, time):
    print(otp, sms)
    if (otp == sms) :
        return True

    return False


async def get_current_user(token: UserSchema=Depends(oauth2_schema)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user_current = await UserModel.objects.get_or_none(id = payload.get('id'))
    if user_current is None:
        return HTTPException(status_code=401, detail='user is not found')

    return {
        'id':user_current.id, 
        'phonenumber':user_current.phonenumber,
        }


async def get_current_user_admin(token: UserSchema=Depends(oauth2_schema)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user_current = await UserModel.objects.get_or_none(id = payload.get('id'))

    if user_current is None and not user_current.is_admin:
        return HTTPException(status_code=401, detail='user is not found')

    return {
        'id':user_current.id, 
        'phonenumber':user_current.phonenumber,
        }
