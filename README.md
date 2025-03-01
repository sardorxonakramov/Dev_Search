<h2>Assalomu aleykum Bugun 
<strong style='color:red'>DevSearch</strong>
Loyihasini boshlaymiz va tugallaymiz </h2>

1. loyihani va virtula muhitni sozlaymiz va kerakli templatelarni torib olib biz ishlayotgan loyiha ichiga qo'shamiz
devsearch template va unga mos <small style='color:green'> MAIN va USERS </small> applarni qo'shib olamiz

```bash
    python -m venv .venv
    .venv\scripts\activate

    python3 -m venv .venv
    source .venv/bin/activate
```
- djangoni yuklash
```bash
    pip install django==version or django >=3.2.1
    django-admin startproject PROJECT .
    python manage.py startapp app_name 
    python manage.py runserver
```

2. Loyihadagi barcha kerakli bo'lgan narsalarni settingsda to'g'irlaymiz key va tokenlarni  <span style='color:red'> .env </span> file ichiga database ni ham sozlaymiz

+ .env fileda quydagi keylar bo'ladi asosiylarni yozaman va yana tokenlarni ham sozlash kerak bo'ladi
  ```txt
        #Django key
        DJANGO_SECRET_KEY=''

        # for database
        DB_NAME=batabasenomi
        DB_USER=postgres
        DB_PASSWORD=parol
        DB_PORT=5432
        DB_HOST=localhost
    ```

+ settings ichini sozlash 
+ POSGRE SQLGA O'TQAZISH CONFIGURATSIYASI ham bor
  
```python
import os
from pathlib import Path
from environs import Env
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

env = Env()
env.read_env()

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
    
# for database
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.posgresql',
    'NAME': env.str('DB_NAME'),
    'USER':env.str('DB_USER'),
    'PASSWORD':env.str('DB_PASSWORD'),
    'PORT': env.int('DB_PORT'),
    'HOST':env.str('DB_HOST'),
    }
}

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR/'staticfiles']
STATIC_ROOT = BASE_DIR/'static'

MEDIA_URL ='media/'
MEDIA_ROOT = BASE_DIR/'media/'
```
- Agar django key yo'qolib qolsa BU site orqali <a href= 'https://djecrety.ir/'> Djecrety </a> key olsa bo'ladi 
- environs moduli bu .env file ichidagi keylarni olib beradigan modul hosoblanadi bundan boshqa modullar ham bor olish uchun   

+ Postgres sql ni ishga tushirish uchun quydagi servis (modul) yordam beradi
```bash 
pip install psycopg2-binary 
```
+ media dan rasimlarni olish uchun quydagi larni urlga qo;shish kerak
```python

from django.conf import settings
from django.conf.urls.static import static
...
if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
Barcha configuriyatsalar tugagandan so'ng 



# Django model translation:

Bu djnago modeltranslation bizga djangodagi barcha static matinlarni tarjima qilishga yordam beradi i18n- modeli asosan static matinlarni tarjima qiladi 
1. <span style='color:yellow'>settings.py</span>ni sozlaymiz
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    #i18n tillar uchun middlewhere
    "django.middleware.locale.LocaleMiddleware",
]


USE_I18N = True

LANGUAGES = [
    ("en", _("English")),
    ("uz", _("Uzbek")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = BASE_DIR/'locale'

```
hozircha barcha html va static o'zgaruvchilarni tarjima qilish uchun shu conf ni o'zi yetarli va config.urls.py ni ichiga i18n-urlsni qo'shish kifoya

# Django-ModelTranslation
Ana endi modeldagi userning hamma malumotlarini tarjima qilish uchun qilish 
1. translate qilish uchun tarjima qilib beradigan translate kutubhonasini yuklab olamiz
    ``` bash
     pip install django-modeltranslation
    ```
2. keyin esa uni <span style='color:green'>requirements.txt </span> ga qo'shin ketamiz
   ```bash
    pip freeze > requirements.txt
   ```
3. <code>settings.py</code> ni sozlaymiz yani install_app ga qo'shamiz
    ```python
      INSTALLED_APPS = [
       'modeltranslation',  # bu yerga qo'shiladi
       'django.contrib.admin',
       ...
   ]
   ```
3. tarjima qilinadigan model joylashgan app'ga <code style='color:blue'> translation.py </code> yaratamiz ichiga esa
   ```python 
   # translation.py

   from modeltranslation.translator import register, TranslationOptions
   from .models import Book

   @register(Book)
   class BookTranslationOptions(TranslationOptions):
       fields = ('title', 'description')
    ```
    va migratsiya qilamiz shu bilan tayyor

4. Signin SignUp va logOut qismini bajardik 
   sign inda loginView class dan foydalandik voris olib logoutview da foydalandik tayyor modeldan
   + Asosiy qilgan ishimiz users app daasosiy <code>forms.py</code> yaratib oldim
    ``` python 
    # forms.py
    class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]

    def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)

            for _ , field in self.fields.items():
                field.widget.attrs.update({'class':'input input--text',})

    # views.pyclass SignUpView(CreateView):
    model = User
    template_name = 'USERS/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    #urls.py
    from django.urls import path
    from django.contrib.auth.views import LoginView, LogoutView
    from . import views

    urlpatterns = [
        path('signup/',views.SignUpView.as_view(),name='signup'),
        path('signin/',LoginView.as_view(template_name='USERS/login.html'),name='login'),
        path('logout/',LogoutView.as_view(),name='logout')
        ]
    ```
