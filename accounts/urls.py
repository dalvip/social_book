from django.urls import path
from accounts import views 
from .views import UserFilesView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('upload-books/', views.upload_books, name='upload_books'),
    path('author_dashboard/', views.author_dashboard, name='author_dashboard'),
    path('api/user/files/', UserFilesView.as_view(), name='user-files'),
    path('my-books/', views.my_books_dashboard, name='my_books'),
    path('get_token/', views.get_auth_token, name='get_token'),
    path('authors/', views.author_list, name='author_list'),
    path('sellers/', views.seller_list, name='seller_list'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('dashboard/', views.author_dashboard, name='author_dashboard'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/books/', views.BookListView.as_view(), name='book_list'),
    path('dashboard/books/add/', views.BookCreateView.as_view(), name='book_add'),
    path('dashboard/books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('dashboard/books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('dashboard/profile/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('seller/<int:seller_id>/', views.seller_profile, name='seller_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)