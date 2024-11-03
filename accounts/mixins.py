from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_role == 'author'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Only authors can access this page.")
        return redirect('login')