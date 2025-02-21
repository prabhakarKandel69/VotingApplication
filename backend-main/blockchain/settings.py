INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'voters',
    'candidate',
    'votes',
    'user',
    'blockchain',  # 👈 Ensure this is included
    'rest_framework_simplejwt',
    'corsheaders',
]
