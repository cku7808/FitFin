from rest_framework import serializers
from .models import Article, Comment

class ArticleListSerializer(serializers.ModelSerializer):
    
    like_counts = serializers.IntegerField(source='like_users.count', read_only=True)
    comment_counts = serializers.IntegerField(source='comment_set.count', read_only=True)
    
    class Meta:
        model = Article
        # fields = ('id' , 'title', 'content', 'user',)
        exclude = ('created_at', 'updated_at', 'like_users')
        read_only_fields = ('user',)


class ArticleSerializer(serializers.ModelSerializer):
    
    like_counts = serializers.IntegerField(source='like_users.count', read_only=True)
    comment_counts = serializers.IntegerField(source='comment_set.count', read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users',)
        
        
class CommentSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article',)
