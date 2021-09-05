from django.db import models

# Create your models here.
class ThreadModel(models.Model):
    name = models.CharField(max_length=40)
    next_id = models.IntegerField(default=1, blank=True)

class PostDataModel(models.Model):
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE)
    post_id = models.IntegerField(default=0)
    response = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.CASCADE)
    response_post_id = models.CharField(default="", max_length=10)
    name = models.CharField(max_length=40)
    postdate = models.CharField(max_length=20)
    content = models.CharField(max_length=200)
    good = models.IntegerField(default=0, blank=True)
    bad = models.IntegerField(default=0, blank=True)

