import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.contrib.auth import get_user_model
import django_filters
from accounts.utils.db_engine import fetch_data
from .models import UploadFile
from .forms import UploadFileForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UploadFileSerializer  
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.decorators import api_view
from accounts.forms import LoginForm
from django.contrib.auth import login as auth_login
from .models import CustomUser
from .models import Book
from django.core.paginator import Paginator
from django.shortcuts import  get_object_or_404
from accounts.models import Genre
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm, AuthorProfileForm
from .mixins import AuthorRequiredMixin
from .models import SellerProfile


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request)
                return redirect('login')  
            else:
                messages.error(request, 'User authentication failed.')
                return redirect('register')  # Optional: Redirect back to register page on failure

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def home(request):
    return render(request, 'accounts/home.html')

def check_auth(request):
    """Debug view to check authentication status"""
    data = {
        'is_authenticated': request.user.is_authenticated,
        'has_access_token': 'access_token' in request.session,
        'username': str(request.user),
    }
    return JsonResponse(data)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Check the user role and redirect accordingly
                if user.user_role == 'author':
                    return redirect('author_dashboard')  # Replace with the URL name for the author list
                elif user.user_role == 'seller':
                    return redirect('seller_list')  # Replace with the URL name for the seller list
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

User = get_user_model()

@login_required
def get_auth_token(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    return JsonResponse({'token': token.key})

def logout_view(request):
    # Clear tokens from session
    request.session.pop('token', None)
    request.session.pop('token', None)
    
    # Regular Django logout
    logout(request)
    return redirect('home')

def authors_sellers(request):
    users = User.objects.filter(public_visibility=True)
    return render(request, 'authors_sellers.html', {'users': users})

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['public_visibility']

def author_list(request):
    authors = CustomUser.objects.filter(user_role='author')
    return render(request, 'accounts/author_list.html', {'authors': authors})

def seller_list(request):
    sellers = CustomUser.objects.filter(user_role='seller')
    return render(request, 'accounts/seller_list.html', {'sellers': sellers})
def upload_books(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user  
            uploaded_file.save()
            return redirect('accounts/upload_books.html')
    else:
        form = UploadFileForm()

    files = UploadFile.objects.filter(user=request.user) 
    return render(request, 'accounts/upload_books.html', {
        'form': form,
        'files': files
    })

def some_view(request):
    fetch_data()
    return HttpResponse("Data fetched!")

class UserFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        files = UploadFile.objects.filter(user=user)  # Assuming you have a foreign key to user
        serializer = UploadFileSerializer(files, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def user_files(request):
    if request.user.is_authenticated:
        return Response({"message": "User authenticated successfully."})
    else:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)   
@login_required
def my_books_dashboard(request):
    user_files = UploadFile.objects.filter(user=request.user)
    if user_files.exists():
        return render(request, 'my_books.html', {'files': user_files})
    return redirect('upload_books')
@csrf_exempt
def send_test_email(request):
    subject = 'Welcome to Social Book!'
    message = 'Thank you for registering with Social Book!'
    recipient_list = ['rathodvishal9850@gmail.com']  # Replace with the recipient's email

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    return HttpResponse("Test email sent successfully.")
def landing_page(request):
    featured_books = Book.objects.filter(is_public=True).order_by('-created_at')[:6]
    return render(request, 'accounts/landing.html', {'books': featured_books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_public=True)
    similar_books = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:3]
    return render(request, 'accounts/book_detail.html', {
        'book': book,
        'similar_books': similar_books
    })

def book_list(request):
    # Get all genres (consider caching this if it doesn't change often)
    genres = Genre.objects.all()
    
    # Get filter parameters
    selected_genre = request.GET.get('genre', '')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')  # Default sorting by newest
    
    # Start with base queryset
    books = Book.objects.filter(is_public=True)
    
    # Apply genre filter
    if selected_genre:
        try:
            # Convert selected_genre to integer for comparison
            genre_id = int(selected_genre)
            books = books.filter(genre_id=genre_id)
        except (ValueError, TypeError):
            # Handle invalid genre ID
            pass
    
    # Apply search if provided
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply sorting
    valid_sort_fields = ['title', '-title', 'created_at', '-created_at', 'author', '-author']
    if sort_by in valid_sort_fields:
        books = books.order_by(sort_by)
    
    # Optimize query with select_related for foreign keys
    books = books.select_related('author', 'genre')
    
    # Pagination
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        page_obj = paginator.get_page(paginator.num_pages)
    
    # Convert selected_genre to integer for template comparison
    try:
        selected_genre_id = int(selected_genre) if selected_genre else None
    except (ValueError, TypeError):
        selected_genre_id = None
    
    # Mark selected genres for easier template handling
    for genre in genres:
        genre.is_selected = genre.id == selected_genre_id
    
    # Prepare template context
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'selected_genre': selected_genre_id,  # Now passing the integer ID
        'search_query': search_query,
        'sort_by': sort_by,
        'total_books': books.count(),
        'current_page': page_number or 1,
        'items_per_page': items_per_page,
    }
    
    return render(request, 'accounts/book_list.html', context)
@login_required
def author_dashboard(request):
    user_books = Book.objects.filter(author=request.user)
    return render(request, 'accounts/author_dashboard.html', {'books': user_books})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_template_names(self):
        if self.request.user.user_role == 'author':
            return ['accounts/author_dashboard.html']
        return ['accounts/seller_dashboard.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.user_role == 'author':
            context['books'] = Book.objects.filter(author=user)
            context['total_books'] = context['books'].count()
            # Add any author-specific context here
        else:
            # Add seller-specific context here
            pass
        
        return context

class BookListView(LoginRequiredMixin, AuthorRequiredMixin, ListView,CustomUser):
    model = Book
    template_name = 'accounts/book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)

class BookCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'accounts/book_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'accounts/book_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('dashboard')
    template_name = 'accounts/book_confirm_delete.html'
    
    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_form.html'
    form_class = AuthorProfileForm
    success_url = reverse_lazy('dashboard')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

def seller_profile(request, seller_id):
    seller = get_object_or_404(SellerProfile, user__id=seller_id)
    books = seller.user.book_set.filter(is_public=True)  # assuming seller has a related `book_set` with `Book` model
    context = {
        'seller': seller,
        'books': books
    }
    return render(request, 'accounts/seller_profile.html', context)