
from rest_framework.permissions import BasePermission, SAFE_METHODS
from app1.models import Review  

# class IsReadOnlyOrReview(BasePermission):
#     """
#     Custom permission to allow only review posting for users, and read-only for other APIs.
#     """

#     def has_permission(self, request, view):
#         # Allow read-only access for all users
#         if request.method in SAFE_METHODS:
#             return True

#         # Allow modifications only for the Review model
#         return view.basename == 'review'
    





# from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only the owner of the review to update it.
    Others can only read (GET) the data.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all users
        if request.method in SAFE_METHODS:
            return True
        # Allow update only if the user is authenticated and the review belongs to the user
        return request.user.is_authenticated and request.method in ['PUT', 'PATCH']

    def has_object_permission(self, request, view, obj):
        # For non-safe methods (i.e., PUT/PATCH), ensure the user can only modify their own review
        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user  # Allow modification only if the user is the owner of the review
        return True

class IsAuthenticatedOrOwnReview(BasePermission):
    """
    Custom permission to allow:
    - Unauthenticated users to view data (read-only operations)
    - Authenticated users to perform write operations
    - Authenticated users to give a new review or update their own review.
    """

    def has_permission(self, request, view):
        # Allow read-only operations for unauthenticated users
        if request.method in SAFE_METHODS:
            return True
        
        # For write operations, allow if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to modify or view the object (review).
        If the object is a review, allow the user to update their own review.
        """
        # Allow the user to edit their own review
        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user  # Only the user who created the review can edit it
        
        # If it's a read-only method, all users can view
        return request.method in SAFE_METHODS
    


class ReadOnlyForAuthenticatedUsers(BasePermission):
    """
    Allows authenticated users to only read book information.
    Only admin users can modify book data.
    """
    
    def has_permission(self, request, view):
        # Allow read-only methods (GET, HEAD, OPTIONS) for all authenticated users
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Allow modifications only for admin users
        return request.user.is_staff  # Checks if the user is an admin



class ReadOnlyForAllExceptAdmin(BasePermission):
    """
    - Allows everyone (authenticated & unauthenticated) to read book data.
    - Only admin users (is_staff=True) can create, update, or delete books.
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users (SAFE_METHODS = GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Allow modification (POST, PUT, DELETE) only for admin users
        return request.user.is_authenticated and request.user.is_staff
    

# class AllowAdminOrOwnerDelete(BasePermission):
#     """
#     Allows only the review owner or an admin to delete reviews.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Allow read-only access for everyone
#         if request.method in SAFE_METHODS:
#             return True

#         # Allow delete if the user is admin or the review owner
#         if request.method == 'DELETE':
#             return request.user.is_authenticated and (request.user.is_staff or obj.user == request.user)

#         return False  # Block all other actions explicitly



class AllowAdminOrOwnerEditDelete(BasePermission):
    """
    - Allows **owners** to update (`PUT`, `PATCH`) their reviews.
    - Allows **admins or owners** to delete (`DELETE`) reviews.
    - Everyone else gets read-only access (`SAFE_METHODS`).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # Allows GET, HEAD, OPTIONS
            return True

        # Allow update (PUT, PATCH) only if the user is the review owner
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_authenticated and obj.user == request.user

        # Allow delete only if the user is the owner or an admin
        if request.method == 'DELETE':
            return request.user.is_authenticated and (request.user.is_staff or obj.user == request.user)

        return False  # Block all other actions explicitly


    


