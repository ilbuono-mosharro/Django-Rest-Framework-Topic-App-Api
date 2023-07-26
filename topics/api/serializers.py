from rest_framework import serializers
from accounts.api.serializers import UserReadSerializer
from categories.api.serializers import CategoryReadSerializer
from ..models import Topic


class TopicReadSerializer(serializers.ModelSerializer):
    starter = UserReadSerializer(read_only=True)
    category = CategoryReadSerializer(read_only=True)
    upvote = serializers.SerializerMethodField()
    downvote = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d %b %Y')

    class Meta:
        model = Topic
        fields = ['id', 'starter', 'subject', 'body', 'category', 'upvote', 'downvote', 'created_at']
        read_only_fields = ['id', 'starter', 'subject', 'body', 'category', 'upvote', 'downvote', 'created_at']

    def get_upvote(self, obj):
        return obj.users_upvote.count()

    def get_downvote(self, obj):
        return obj.users_downvote.count()


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'starter', 'subject', 'category', 'body']
        read_only_fields = ['id', 'starter', 'category']

    def create(self, validated_data):
        starter = validated_data.pop('starter')
        subject = validated_data.pop('subject')
        body = validated_data.pop('body')
        category = validated_data.pop('category')
        return Topic.objects.create(starter=starter, subject=subject, body=body, category=category)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance

class TopicVoteSerializer(serializers.ModelSerializer):
    upvote = serializers.SerializerMethodField()
    downvote = serializers.SerializerMethodField()
    class Meta:
        model = Topic
        fields = ['upvote', 'downvote']
        read_only_fields = ['upvote', 'downvote']

    def get_upvote(self, obj):
        return obj.users_upvote.count()

    def get_downvote(self, obj):
        return obj.users_downvote.count()
