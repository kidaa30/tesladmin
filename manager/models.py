from tinymce.models import HTMLField
from django.db import models
import sys

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    #text = models.TextField()
    text = HTMLField()
    path = models.CharField(max_length=300, default='')
    date = models.DateTimeField('Date published', blank=True)

    if sys.version_info.major == 3:
        def __str__(self):
            return self.title
    else:
        def __unicode__(self):
            return unicode(self.title)
