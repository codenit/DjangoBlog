from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
#to specify image upload location we define a function

#def upload_location(instance, filename):
   # return "%s/%s" % (instance.pk, filename)

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    image = models.ImageField(null=True,
                              blank=True,)
                              #upload_to=upload_location)

    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    objects = PostManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})


    # for latest posts on top of page
    class Meta:
        ordering = ['-timestamp', 'updated']

    def get_markdown(self):
        content = self.content
        return markdown(content)
