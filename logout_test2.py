import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_eventos.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.test import Client
from django.contrib.auth.hashers import make_password

User = get_user_model()
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
user.password = make_password('testpass')
user.save()

client = Client(HTTP_HOST='localhost')
print('GET /login/ =>', client.get('/login/').status_code)
response = client.post('/login/', {'username': 'testuser', 'password': 'testpass'}, follow=True)
print('POST /login/ =>', response.status_code)
print('login redirects:', response.redirect_chain)
print('login final path:', response.request.get('PATH_INFO'))
print('logged in:', '_auth_user_id' in client.session)

logout_resp = client.get('/logout/', follow=True)
print('GET /logout/ =>', logout_resp.status_code)
print('logout redirects:', logout_resp.redirect_chain)
print('logout final path:', logout_resp.request.get('PATH_INFO'))
print('logged in after logout:', '_auth_user_id' in client.session)
