from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()  # objects.all lay so luong ban ghi
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
class BookListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Book
    paginate_by = 1

    def get_queryset(self):
        return Book.objects.all()
class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 1

    def get_queryset(self):
        return Author.objects.all()

class AuthorDetailView(generic.DetailView):
    model = Author

class BookListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    model = Book
    paginate_by = 1
class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorsListView(LoginRequiredMixin,generic.ListView):
    model = Author
    paginate_by = 1
class AuthorsDetailView(LoginRequiredMixin,generic.DetailView):
    model = Author

def authors_detail_view(request, primary_key):
    author = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/author_detail.html', context={'author': author})
