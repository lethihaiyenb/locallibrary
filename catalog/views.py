from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author

import datetime

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
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllborrowerListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/allborrower.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrower') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

from catalog.models import Book

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
