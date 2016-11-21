from itertools import chain
from django.http import HttpResponse
from rest_framework import generics, permissions, views, response, status
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from . import permissions as my_permissions
from .models import Post, Comment
from .serializers import PostSerializer, CreatePostSerializer, CommentSerializer, CreateCommentSerializer
import json


# Create your views here.


def index(request):
	return HttpResponse("204 No Content")


# POST a new Post. Requires authentication (Prove you are the owner by sending object)
class PostCreateView(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = CreatePostSerializer
	permission_classes = [permissions.IsAuthenticated]

	@detail_route(methods=['post'])
	def create_post(self, request):
		data = request.data
		author = request.user.author
		serializer = CreatePostSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			post = serializer.save()
			post.author = author
			post.host = "http://127.0.0.1:8000/socialnet/posts/" + str(post.id) + "/"
			post.save()
			return response.Response(status=status.HTTP_201_CREATED)
		return response.Response(status=status.HTTP_400_BAD_REQUEST)


# List of posts that are visible for the user
class PostListView(generics.ListAPIView):
	# queryset = Post.objects.all()
	serializer_class = PostSerializer

	def get_queryset(self):
		public_posts = Post.objects.filter(visibility=True)
		try:
			my_private_posts = Post.objects.filter(author=self.request.user.author, visibility=False)
			result_list = list(chain(public_posts, my_private_posts))
		except AttributeError:
			result_list = public_posts
		return result_list


# List of Posts of the user or the visible posts of other users
class PostByAuthorListView(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		author = self.kwargs['pk']
		if author == self.request.user.author.id:
			result_list = Post.objects.filter(author=self.request.user.author)
		else:
			result_list = Post.objects.filter(author=author, visibility=True)
		return result_list


# Return a single post if the post is public or if you are the owner
class PostRetrieveView(generics.RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [my_permissions.IsPostPublicOrOwner]


# PUT an Update. Requires authentication (Prove you are the owner by sending object)
class PostUpdateView(generics.UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = CreatePostSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyPost]


# DELETE an post. Requires authentication (Prove you are the owner by sending object)
class PostDestroyView(generics.DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyPost]


# POST a new comment in the post designated in the URL.
class CommentCreateView(generics.CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CreateCommentSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsPostPublicOrOwner]

	def perform_create(self, serializer):
		currentPost = Post.objects.get(id=self.kwargs['pk'])
		serializer.save(author=self.request.user.author, post=currentPost)


# GET all the comments. Admin only function
class CommentListView(generics.ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


# GET a single comment. Admin only function
class CommentRetrieveView(generics.RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


# DELETE a comment. Requires authentication and owner of comment or post
class CommentDestroyView(generics.DestroyAPIView):
	queryset = Comment.objects.all()
	serializer_class = CreateCommentSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyComment]
