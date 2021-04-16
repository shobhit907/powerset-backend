from django.core.mail import send_mail
import os

def SendVerificationMail(detail, recipientEmail, verified, coordinatorName, message):
    recepients = []
    recepients.append(recipientEmail)
    subject = detail + ' ' + verified
    message = 'Dear Student,\n\nYour ' + detail + ' have been ' + verified + ' by the coordinator - ' + coordinatorName + ' with the following message:\n\n' + message + '\n\nRegards\nPowerset team'
    send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)