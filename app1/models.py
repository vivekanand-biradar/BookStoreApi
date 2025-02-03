from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


###############################     This is Signal Code To generate Tokenauthenetication   ###############################

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#############################################################################################################3



class Genre(models.Model):                                                          # Represents a genre to categorize books.

    name = models.CharField(max_length=100, unique=True)                            # Genre name                     
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name 



 
class Author(models.Model):                                                         # Represents an author of a book.

    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name      #### This is used to show direct author name instead of showing author id




class Book(models.Model):

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='books', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title                          #############   This will return Book Title




class Purchase(models.Model):
    
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='purchases', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure that the stock is sufficient for the purchase
        
        if self.book.stock < self.quantity:
            raise ValidationError(f"Not enough stock for the book: {self.book.title}")
        
        # Update the stock by subtracting the purchased quantity
        
        self.book.stock -= self.quantity
        self.book.save()

        super().save(*args, **kwargs)  



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    # rating = models.IntegerField(
    #     default=1,
    #     validators=[
    #         MinValueValidator(1),  # Minimum rating of 1
    #         MaxValueValidator(5)   # Maximum rating of 5
    #     ]
    # )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # Ensure each user can only review a specific book once

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"



#####################################################################
#####################################################################


#Signal auth Code   --- This signal creates auth Token for users automatically


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance = None,created = False,**kwargs):
    if created:
        Token.objects.create(user=instance)

