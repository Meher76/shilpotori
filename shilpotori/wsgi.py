import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'shilpotori' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shilpotori.settings')

application = get_wsgi_application()
