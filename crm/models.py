from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def is_in_group(self, grp):
        return grp in [g.name for g in self.groups.all()]
