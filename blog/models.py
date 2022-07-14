from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('blog:category_list', args=[self.name])

    def __str__(self):
        return self.name


class Post (models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_directory_path, default='posts/default.jpg', blank=True)
    image_caption = models.CharField(max_length=100, default='Photo by Blog')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=options, default='draft')
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(User, related_name='thumbs', default=None, blank=True)

    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/posts/default.jpg"

    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.id])

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            image = self.image
            self.image = None
            super(Post, self).save(*args, **kwargs)
            self.image = image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Post, self).save(*args, **kwargs)

class Comment(MPTTModel):
    author = models.ForeignKey(
        User, related_name='author', on_delete=models.CASCADE, default=None, blank=True)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

class Vote(models.Model):
    post = models.ForeignKey(Post, related_name='postid', on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(User, related_name='userid', on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)

