from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QuestionManager(models.Manager):                                          
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')
    
    
class Question (models.Model):                                                 
    objects = QuestionManager() 
    title = models.CharField(default="", max_length=1024)
    text = models.TextField(default="")
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="question_like_user")
    
    def __str__(self):
        return self.title

    def get_url(self):
        return "/question/{}/".format(self.id)
    
class Answer (models.Model):
    text = models.TextField(default="")
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

class Session(models.Model):
    key = models.CharField(unique=True)
    user = models.ForeignKey(User)
    expires = models.DateTimeField()

def do_login(login, password):
    try:
        user = User.objects.get(username=login)
    except User.DoesNotExist:
        return None
    if password != user.password
        raise Exception
        return None
    session = Session()
    session.key = generate_long_random_key(255)
    session.user = user
    session.expires = datetime.now() + timedelta(days=5)
    session.save()
    return session.key