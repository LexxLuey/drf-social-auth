from django.db import models
from django.core.validators import MinValueValidator

class Movie(models.Model):
    class Status_Choices(models.IntegerChoices):
        COMING_UP = 1
        STARTING = 2
        RUNNING = 3
        FINISHED = 4

    name = models.CharField(max_length=200, null=True)
    protagonists = models.CharField(max_length=200, null=True)
    poster = models.ImageField(upload_to ='posters/', null=True)
    trailer = models.FileField(upload_to ='trailers/', null=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    status = models.IntegerField(choices=Status_Choices.choices, default=Status_Choices.COMING_UP)
    ranking = models.IntegerField(validators=[MinValueValidator(0, message="Cannot have ranking below 0")], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "movie"
        verbose_name_plural = "movies"

    def __str__(self):
        return self.name
