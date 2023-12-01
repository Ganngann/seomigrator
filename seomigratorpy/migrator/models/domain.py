# seomigratorpy/migrator/models/domain.py
from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)

    # save on init
    def __init__(self, *args, **kwargs):
        super(Domain, self).__init__(*args, **kwargs)
        # self.save()

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        try:
            super(Domain, self).save(*args, **kwargs)
        finally:
            return
