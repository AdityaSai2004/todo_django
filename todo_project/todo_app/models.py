from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length = 100)
    memo = models.TextField(blank = True , max_length = 200)
    created = models.DateTimeField(auto_now_add = True)
    datecompleted = models.DateTimeField(null = True , blank = True )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.title