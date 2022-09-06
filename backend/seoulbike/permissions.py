from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, SAFE_METHODS

class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser

class IsAuthenticatedOrReadAndWrite(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS + ('POST',) or
            request.user and
            request.user.is_authenticated):
            return True
        return False