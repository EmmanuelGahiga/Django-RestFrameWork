from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .models import Post
from .serializers import PostsSerializers
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from auths.serializers import CurrentUserPostsSerializer
from .permissions import ReadOnly, AuthorOrReadOnly

# ===================================================================

"""
USE OF @api_view
# READ
@api_view(http_method_names=["GET"])
def get_posts(request:Request):
    try :
        posts  = Post.objects.all()
        
    except Post.DoesNotExist:
        return Response(
            data={"message": "Posts not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = PostsSerializers(instance=posts,many=True)
    return Response(data=serializer.data,status=status.HTTP_200_OK)

#POST
@api_view(http_method_names=["POST"])
def create_posts(request: Request):

    serializer = PostsSerializers(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            data={"data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    return Response(
        data={"errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )

# POST_DETAILS MODIFY_POST DELETE_POST
@api_view(http_method_names=["GET","PUT","DELETE"])
def post_detail_modify_delete(request: Request, post_id: int):
    
    try:
        post = Post.objects.get(pk=post_id)

    except Post.DoesNotExist:
        return Response(
            data={"message": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        
    #get details of post
    if request.method == "GET":
        serializer = PostsSerializers(instance=post)
        return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        
    #get change a post
    elif request.method == "PUT":
        serializer = PostsSerializers(
                instance=post,
                data=request.data
            )
    
        if serializer.is_valid():
            serializer.save()
    
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
    
        return Response(
            data={"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    #delete a post
    elif request.method == "DELETE":
        post.delete()
        return Response(
                {"message":"Post deleted"},
                status=status.HTTP_200_OK,
            )
"""
# ===================================================================

"""
#USE OF APIView MODULE
#GET AND CREATE
class PostListCreate(APIView):
    serializer_class = PostsSerializers
    def get(self,request:Request):
        posts = Post.objects.all()
        serializer = self.serializer_class(instance=posts, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request:Request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        
#GET post details,UPDATE and DELETE
class PostRetrieveUpdateDeleteView(APIView):
    serializer_class = PostsSerializers

    def get(self,request:Request,post_id:int,):
        post = get_object_or_404(Post, pk=post_id)
        serializer = self.serializer_class(instance=post)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request:Request,post_id:int,):
        post = Post.objects.get(pk=post_id)
        serializer = self.serializer_class(instance=post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(
        data=serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self,request:Request,post_id:int,):
        post = Post.objects.get(pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# ===================================================================


# USE OF GENERICAPIVIEW AND queryset
# POST AND GET ALL
class PostListCreate(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = PostsSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # Mixins hooks for related fonctionnality
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# GET post details,UPDATE and DELETE
class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PostsSerializers
    permission_classes = [AuthorOrReadOnly]
    queryset = Post.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user
    serializer = CurrentUserPostsSerializer(instance=user, context={"request": request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)
