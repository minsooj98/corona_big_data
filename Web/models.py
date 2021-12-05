from django.db import models

class Graph(models.Model):
    userid = models.CharField(max_length=20)
    image = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'graph'


class Members(models.Model):
    userid = models.CharField(primary_key=True, max_length=20)
    passwd = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    birth = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'members'