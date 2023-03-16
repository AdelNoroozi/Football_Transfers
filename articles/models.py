from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


class Article(models.Model):
    TYPES = (('N', 'news'),
             ('A', 'analyze'),
             ('C', 'commentary'))
    title = models.CharField(max_length=100)
    text = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    type = models.CharField(max_length=20, choices=TYPES)

    def __str__(self):
        return self.title


class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pictures/articles/', null=True, blank=True)
    alt_text = models.CharField(max_length=50)

    def __str__(self):
        return self.alt_text
