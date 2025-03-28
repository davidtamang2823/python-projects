from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Meta:
        default_permissions = ()
        permissions = (
            ("can_manage_users", "Can Manage Users"),
            ("can_view_users", "Can View Users")
        )