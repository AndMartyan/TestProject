from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from django.contrib.auth.models import User
from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from .serializers import RegisterSerializer, UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PostView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        if request.user.is_authenticated:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.public_posts()

        serializer = PostSerializer(queryset, many=True)

        return Response({'data': serializer.data})

    def post(self, request):

        post = request.data
        serializer = PostSerializer(data=post)
        if serializer.is_valid(raise_exception=True):
            new_post = serializer.save(owner=self.request.user)
            return Response({"success": f"Post with id {new_post} created successfully"})


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })



