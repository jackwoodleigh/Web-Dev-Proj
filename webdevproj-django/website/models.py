from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    cooking_time = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=50)
    image = models.ImageField(upload_to='recipes/')
    instructions = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
