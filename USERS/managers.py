from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class MyUserManager(UserManager):
    def create_user(self, 
                    email: str,
                    first_name: str = "",
                    last_name: str = "",
                    username: str = None,
                    password: str = None) -> User:
        
        if not email:
            raise ValidationError('Users must have email')
        if '@' not in email:
            email = f"{email}@gmail.com"
        

        email = self.normalize_email(email=email)
        existing_user = self.model.objects.filter(email=email).first()
        
        if existing_user:
            return existing_user  # Return the existing user if it already exists
        

        if not username:
            username = email[:email.index('@')]

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name: str,
                         last_name: str,
                         email: str,
                         password: str) -> User:
        superuser = self.create_user(first_name, last_name, email, password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser
