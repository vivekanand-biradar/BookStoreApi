from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import viewsets,permissions,serializers
from app1.models import Author,Book,Genre,Purchase,Review
from app1.api.serializers import AuthorSerializer,BookSerializer,ReviewSerializer,GenreSerializer,PurchaseSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied 

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser
from app1.permission import ReadOnlyForAllExceptAdmin
#IsOwnerOrReadOnly,AllowAdminOrOwnerDelete,IsAuthenticatedOrOwnReview,ReadOnlyForAuthenticatedUsers,
# Create your views here.

#ModelViewSet
# @method_decorator(csrf_exempt, name='dispatch')

class AuthorModelViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    search_fields = ['id','name']
    permission_classes = [IsAdminUser]



class BookModelViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    search_fields = ['id','title']
    permission_classes = [ReadOnlyForAllExceptAdmin]




    def perform_create(self, serializer):
        # Restrict creating new books to only admin users
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to create a new book.")
        super().perform_create(serializer)


     # Custom action to fetch reviews for a specific book
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def reviews(self, request, pk=None):
        """
        Get all reviews for a specific book.
        Example URL: /books/{book_id}/reviews/
        """
        book = get_object_or_404(Book, pk=pk)
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    


class GenreModelViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    search_fields = ['id','name']
    permission_classes = [IsAdminUser]



class PurchaseModelViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    search_fields = ['id']
    permission_classes = [IsAdminUser]




class ReviewModelViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Show all reviews for any book.
        But, users can only create a review for the books they've purchased.
        """
        user = self.request.user
        if user.is_authenticated:
            # If the user is authenticated, show all reviews.
            return Review.objects.all()
        return Review.objects.none()
    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']

        # Validate if the buyer has purchased the book
        if not Purchase.objects.filter(buyer=user, book=book).exists():
            raise serializers.ValidationError("You can only review books you have purchased.")
        
        # Save the review
        serializer.save(user=user)



# class ReviewModelViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     permission_classes = [AllowAdminOrOwnerEditDelete]

#     def get_queryset(self):
#         """
#         Show all reviews for any book.
#         But, users can only create a review for the books they've purchased.
#         """
#         user = self.request.user
#         if user.is_authenticated:
#             # If the user is authenticated, show all reviews.
#             return Review.objects.all()
#         return Review.objects.none()
    


#     def perform_create(self, serializer):
#         user = self.request.user
#         book = serializer.validated_data['book']

#         # Validate if the buyer has purchased the book
#         if not Purchase.objects.filter(buyer=user, book=book).exists():
#             raise serializers.ValidationError("You can only review books you have purchased.")

#         # Save the review with the authenticated user
#         serializer.save(user=user)

#     # def perform_update(self, serializer):
#     #     """
#     #     Only allow a user to edit their own review.
#     #     """
#     #     review = self.get_object()
#     #     if review.user != self.request.user:
#     #         raise PermissionDenied("You can only edit your own review.")
        
#     #     # Save the review after validation
#     #     serializer.save()


#     def perform_update(self, serializer):

#         ##  Only allow a user to edit their own review.
    
#         review = self.get_object()
#         if review.user != self.request.user:
#             raise PermissionDenied("You can only edit your own review.")
    
#         serializer.save()


#     def perform_destroy(self, instance):
    
#            ### Allow review owners and admins to delete reviews.
    
#         user = self.request.user
#         if not user.is_staff and instance.user != user:
#             raise PermissionDenied("Only the review owner or an admin can delete this review.")

#         instance.delete()
