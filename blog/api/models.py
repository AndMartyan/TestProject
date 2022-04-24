from django.db import models


class PostManager(models.Manager):
    def public_posts(self, *args, **kwargs):
        return super(PostManager, self).filter(is_private=False)

    def private_posts(self, *args, **kwargs):
        return super(PostManager, self).filter(is_private=True)


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)

    objects = PostManager()

    class Meta:
        ordering = ['created']
