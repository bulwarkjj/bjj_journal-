from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """A topic the user is learning"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model"""
        return self.text

class Entry(models.Model):
    """Something specific learned about the topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:  # Meta holds extra info for managing models
        """tell django to use entries to refer to more than one entry"""
        verbose_name_plural = 'entries'

    def __str__(self):
        """Retrun a string representation of the model"""
        return f"{self.text}..."