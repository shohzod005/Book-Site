from django.shortcuts import get_object_or_404
from .serializers import GenreSerializer, AuthorSerializer, BookSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from library.models import Genre, Book, Author
from rest_framework import status, generics, mixins
from .models import Post


class GenreListCreateAPIView(APIView):
    serializer_class = GenreSerializer
    def get(self, request):
        genres = Genre.objects.all()
        serializer = self.serializer_class(genres, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class GenreRetrieveUpdateDeleteAPIView(APIView):
    serializer_class = GenreSerializer
    def get(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        serializer = self.serializer_class(genre)
        return Response(data=serializer.data)
    
    def put(self, request, slug):
        data = request.data
        genre = get_object_or_404(Genre, slug=slug)
        serializer = self.serializer_class(instance=genre, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def patch(self, request, slug):
        data = request.data
        genre = get_object_or_404(Genre, slug=slug)
        serializer = self.serializer_class(instance=genre, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def delete(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(data={"deleted": "Genre deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# class BookListApiView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class BookCreateAPIView(generics.CreateAPIView):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()

class BookListCreateApiView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

class AuthorUpdateDestroyAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,   mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()

class PostRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()