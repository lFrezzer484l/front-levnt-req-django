from django.db import models

class Requirement(models.Model):
    requester = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    requirement_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    titulo = models.CharField(max_length=20, default="Sin titulo")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
