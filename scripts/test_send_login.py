import os
import sys
proj_root = r'C:\Users\Administrator\Desktop\project website'
sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sahwira_project.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.test.client import RequestFactory

User = get_user_model()
# find any user with an email
u = None
for user in User.objects.all():
    if user.email:
        u = user
        break
if not u:
    u = User.objects.create_user('testlocal', password='x', email='test@example.com', first_name='Test')
    print('created test user:', u.username)
req = RequestFactory().get('/')
print('sending user_logged_in signal for', u.email)
user_logged_in.send(sender=u.__class__, request=req, user=u)
print('done')
