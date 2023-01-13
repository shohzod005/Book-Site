from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from .forms import BookForm, Genres, AuthorForm
from .models import Book, Genre, Author
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def add_genres(request):
    form = Genres()
    if request.method == "POST":
        form = Genres(request.POST)
        if form.is_valid():
            Genre.objects.create(**form.cleaned_data)
            return redirect('list')
    return render(request, "library/add_genres.html", {'form': form})

@login_required
def add_author(request):
    form = AuthorForm()
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list')
    return render(request, "library/add_author.html", {"form": form})


def books_list(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    authors = Author.objects.all()
    return render(request, "library/index.html", {"books": books, 'genres': genres, 'authors': authors})

class BooksListView(ListView):
    model = Book
    # context_object_name = "books"
    template_name = "library/index.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all().order_by('-created')
        context['genres'] = Genre.objects.all()
        context['authors'] = Author.objects.all()
        return context


class BooksList(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all().order_by('-created')
        genres = Genre.objects.all()
        authors = Author.objects.all()
        return render(request, "library/index.html", {"books": books, 'genres': genres, 'authors': authors})

    def post(self, request, *args, **kwargs):
        pass


def book_detail(request, pk):
    book = Book.objects.get(id=pk)
    return render(request, "library/detail.html", {"book": book})


class BookDetailView(DetailView):
    model = Book
    template_name = "library/detail.html"
    context_object_name = "book"
    queryset = Book.objects.all()

   
class BookDetail(View):
    def get(self, request, pk, *args, **kwargs):
        book = Book.objects.get(id=pk)
        return render(request, "library/detail.html", {"book": book})

@login_required
def add_new_book(request):
    form = BookForm()

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("list")

    return render(request, "library/add.html", {"form": form})

class AddBook(LoginRequiredMixin, View):
    template_name = "library/add.html"

    def get(self, request, *args, **kwargs):
        form = BookForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("list")
        else:
            return render(request, self.template_name, {"form": form})


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = "library/add.html"
    form_class = BookForm
    success_url = reverse_lazy("list")


def update_book(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            # book.title = form.cleaned_data.get("title")
            # book.desc = form.cleaned_data.get('desc')
            # book.image = form.cleaned_data.get('image')
            # book.genres = form.cleaned_data.get('genres')
            # book.author = form.cleaned_data.get('author')
            # book.stars = form.cleaned_data.get('stars')
            # book.isbn_number = form.cleaned_data.get('isbn_number')
            # book.save()
            return redirect("list")

    return render(request, "library/edit.html", {"form": form})


class UpdateBook(View):
    def get(self, request, pk, *args, **kwargs):
        book = Book.objects.get(id=pk)
        form = BookForm(instance=book)
        return render(request, "library/edit.html", {"form": form})

    def post(self, request, pk, *args, **kwargs):
        book = Book.objects.get(id=pk)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list")

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "library/edit.html"
    form_class = BookForm
    success_url = reverse_lazy("list")


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("list")

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "library/delete.html"
    success_url = reverse_lazy("list")



class BookDelete(View):
    def get(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect("list")
