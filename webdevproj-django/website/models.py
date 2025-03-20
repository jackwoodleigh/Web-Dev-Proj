from django.db import models

class Recipe(models.Model):
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes/')
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=50)
    instructions = models.TextField()

    def __str__(self):
        return self.title
    
