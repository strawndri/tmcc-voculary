from django.core.mail import send_mail
from django.conf import settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "voculary.projeto@gmail.com"
EMAIL_HOST_PASSWORD = "tdlj amtt eiae gglb"

try:
    send_mail(
        'Test Email',
        'This is a test email.',
        'voculary.projeto@gmail.com',
        ['andrieliluci@gmail.com'],
        fail_silently=False,
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")
