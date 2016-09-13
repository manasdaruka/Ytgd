from django.db import models


# Create your models here.

class Song(models.Model):
    name = models.CharField(blank=True, null=True,max_length=100)
    url = models.CharField(blank=True, null=True,max_length=100)
    mp3 = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.name) or u''
