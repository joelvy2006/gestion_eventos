import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_eventos.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.test import Client
from django.contrib.auth.hashers import make_password
User = get_user_model()
user, created = User.objects.get_or_create(username='testuser', defaults={'email':'test@example.com'})
user.password = make_password('testpass')
user.save()
c = Client()
print('login page', c.get('/login/').status_code)
r = c.post('/login/', {'username': 'testuser', 'password': 'testpass'}, follow=True)
print('login status', r.status_code, 'path', r.request.get('PATH_INFO'), 'redirects', r.redirect_chain)
r2 = c.get('/logout/', follow=True)
print('logout status', r2.status_code, 'path', r2.request.get('PATH_INFO'), 'redirects', r2.redirect_chain)
