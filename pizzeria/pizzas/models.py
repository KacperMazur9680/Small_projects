from django.db import models

class Pizza (models.Model):
    order = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.order

class Topping (models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    name = models.TextField()
    
    def __str__(self) -> str:
        return self.name
