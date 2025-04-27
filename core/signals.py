# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User,EmailVerificationCode
# import random
# from django.contrib.auth import get_user_model
# from foodordering import settings
# from django.utils import timezone
# from django.core.mail import send_mail

# User = get_user_model()
# @receiver(post_save,sender= User)
# def send_verification_code(sender,instance,created,**kwargs):
#     if created: 
#         instance.is_active = False
#         instance.save()

#         verification_code = str(random.randint(100000,999999))
#         EmailVerificationCode.objects.create(user=instance,code=verification_code)

#         subject = 'verify your email'
#         message = f'your verification code is: {verification_code}'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = ["ahmad.shamma093@gmail.com"]

#         send_mail(subject,message,from_email,recipient_list)
#         print("email sent")