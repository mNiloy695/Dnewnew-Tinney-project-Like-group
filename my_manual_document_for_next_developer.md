
#Hi brother This is my own document not made by ai so first read this .It will help you to understand the project in details

------------------
------------------

Point 1 : I keep every sensitive data in .env file and also import them in setting.py 

SECRET_KEY=
DEBUG=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
CELERY_BROKER_URL = 
------------------
------------------

Point 2 : I handle all authentication part in accounts app 
  Login ,Logout , Registration , Forgot password , Account Activate ,Reset password


------------------
------------------

Point 3 :

  I used twilio for mobile phone verification 
  here the twilio link : https://console.twilio.com/



Point 4: 
   
   The otp send in background and for this i used celery ,redis 




