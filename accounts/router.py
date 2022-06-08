from fastapi import APIRouter, Depends, Form, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse
from .schema import UserBase
from .models import UserModel
from datetime import datetime
from .utils import check_user_healthy, send_sms, get_current_user
from config.settings import SECRET_KEY
from random import randint
import jwt
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix='/accounts', tags=['accounts'])


@router.post('/signin/')
async def sign_in(request:Request, background_tasks:BackgroundTasks, phone:UserBase=Depends()):

    user , obj = await UserModel.objects.get_or_create(phonenumber=phone.phonenumber)

    user.otp = randint(10000, 100000)
    user.time_otp = datetime.now()
    await user.update()

    request.session['my_phone'] = user.phonenumber

    #background_tasks.add_task(send_sms, phonenumber, user.otp)
    #return RedirectResponse("https://typer.tiangolo.com")

    return user


@router.post('/check/sms/')
async def check_otp(request:Request,data:OAuth2PasswordRequestForm=Depends()):
    my_phone = request.session.get('my_phone')
    sms = data.password
    user = await UserModel.objects.get_or_none(phonenumber=my_phone)

    if user is None or not check_user_healthy(user.otp, sms, user.time_otp):
        return JSONResponse(status_code = 404, content='please again signin')

    user_dict = {
        'id': user.id,
        'phonenumber': user.phonenumber,
    }
    access_token = jwt.encode(user_dict, SECRET_KEY)

    return {'access_token': access_token, 'token_type': 'bearer'}

