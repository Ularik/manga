from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True
    )
    name = models.CharField(
        max_length=30
    )
    image = models.ImageField(
        upload_to='media/users/',
        null=True,
        blank=True
        )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Менеджер')
        ),
        default=1
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    is_admin = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name

    # Дополнительные методы и свойства

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    def has_perm(self, perm, obj=None):
        """Does the myuser have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the myuser have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        """Is the myuser a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


