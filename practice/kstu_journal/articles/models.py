from django.db import models

# Create your models here.

class Article(models.Model):
    title_ky = models.CharField(max_length=500)
    title_ru = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    
    annotation_ky = models.TextField()
    annotation_ru = models.TextField()
    annotation_en = models.TextField()
    
    keywords_ky = models.TextField()
    keywords_ru = models.TextField()
    keywords_en = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_ru  # Using Russian title as the default string representation

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']
