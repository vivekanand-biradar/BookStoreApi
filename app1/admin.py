from django.contrib import admin
from .models import Author,Purchase,Book,Genre,Review

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','name','bio','created_at','updated_at']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id','buyer','book','quantity','purchase_date']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user','book','rating','comment','created_at']



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','genre','description','price','stock','created_at','updated_at']



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id','name','description']