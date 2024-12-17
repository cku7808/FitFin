from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment

from django.contrib.auth import get_user_model
User = get_user_model()
# temp_user = User.objects.get(pk=1)

# 게시글 (조회, 생성)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = ArticleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # article = serializer.save(user=temp_user)
                article = serializer.save(user=request.user)
                return Response({'articleid': article.id}, status=status.HTTP_201_CREATED)
        
# 게시글 (상세 조회, 삭제, 수정)
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer.data)
        print(request.method)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        if request.user.is_authenticated and request.user == article.user:
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serializer = ArticleSerializer(article)
                return Response(serializer.data)
        
# 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:    
        article.like_users.add(request.user)
    return Response(status=status.HTTP_201_CREATED)

# 댓글 (생성, 조회)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comment(request, article_pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(article=article_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            article = get_object_or_404(Article, pk=article_pk)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                comment = serializer.save(user=request.user, article=article)
                # comment = serializer.save(user=temp_user, article=article)
                return Response({'commentid': comment.id}, status=status.HTTP_201_CREATED)

# 댓글 (삭제, 수정)
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def comment_edit(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
        
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        if request.user.is_authenticated and request.user == comment.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serializer = CommentSerializer(comment)
                return Response(serializer.data)