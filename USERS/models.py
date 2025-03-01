from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import MyUserManager as UserManager
# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(
        max_length=50,
        verbose_name="Last Name",
    )
    username = models.CharField(
        max_length=50, verbose_name="User Name", blank=True, null=True
    )
    email = models.EmailField(verbose_name="Email", unique=True, max_length=100)
    bio = models.TextField(blank=True, null=True, verbose_name="About")
    profile_image = models.ImageField(
        upload_to="profile_images/",
        default=  "profile-images/default-user.png",
        verbose_name="Profile Image",
    )

    location = models.CharField(
        max_length=50,
        verbose_name="Location",
    )
    occupation = models.TextField(blank=True, null=True)

    social_telegram = models.URLField(verbose_name="Telegram", blank=True, null=True)
    social_whatsapp = models.URLField(verbose_name="WhatsApp", blank=True, null=True)
    social_instagram = models.URLField(verbose_name="Instagram", blank=True, null=True)
    social_facebook = models.URLField(verbose_name="Facebook", blank=True, null=True)
    social_linkedin = models.URLField(verbose_name="LinkedIn", blank=True, null=True)
    social_youtube = models.URLField(verbose_name="YouTube", blank=True, null=True)
    social_git = models.URLField(verbose_name="GitHub", blank=True, null=True)
    social_website = models.URLField(verbose_name="Website", blank=True, null=True)
    objects =UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name','last_name']

    def __str__(self):
        return self.fullname
    

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def set_fullname(self, value):
        names = value.split()
        self.first_name, self.last_name = names[0], " ".join(names[1:])

    fullname = property(get_fullname, set_fullname)


class Skill(models.Model):
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    name =  models.CharField(max_length=50)
    discription = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'{self.owner} – {self.name}'