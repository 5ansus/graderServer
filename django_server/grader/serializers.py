from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Challenge, Submission, UserProfile


class UserSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    challenges_completed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'total_score', 'challenges_completed']
        read_only_fields = ['id']

    def get_total_score(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.total_score
        return 0

    def get_challenges_completed(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_challenges_completed()
        return 0


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChallengeSerializer(serializers.ModelSerializer):
    best_score = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = [
            'id', 'name', 'description', 'max_score', 'difficulty',
            'best_score', 'completed', 'is_active', 'completion_rate'
        ]

    def get_best_score(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            best = Submission.objects.filter(
                user=user,
                challenge=obj
            ).aggregate(models.Max('score'))
            return best['score__max'] or 0
        return 0

    def get_completed(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return Submission.objects.filter(
                user=user,
                challenge=obj,
                passed=True
            ).exists()
        return False

    def get_completion_rate(self, obj):
        return round(obj.get_completion_rate(), 2)


class SubmissionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    challenge_name = serializers.CharField(source='challenge.name', read_only=True)
    is_best_score = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'id', 'username', 'challenge', 'challenge_name', 'code',
            'score', 'passed', 'feedback', 'submitted_at',
            'execution_time', 'error_message', 'is_best_score'
        ]
        read_only_fields = ['id', 'submitted_at', 'username', 'challenge_name']

    def get_is_best_score(self, obj):
        return obj.is_best_score()


class SubmitCodeSerializer(serializers.Serializer):
    challenge_id = serializers.IntegerField()
    code = serializers.CharField()

    def validate_challenge_id(self, value):
        if not Challenge.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Challenge not found or not active")
        return value

    def validate_code(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Code is too short")
        return value


class LeaderboardSerializer(serializers.Serializer):
    username = serializers.CharField()
    total_score = serializers.IntegerField()
    challenges_completed = serializers.IntegerField()
    rank = serializers.IntegerField()


class ProgressSerializer(serializers.Serializer):
    total_score = serializers.IntegerField()
    challenges_completed = serializers.IntegerField()
    total_challenges = serializers.IntegerField()
    total_submissions = serializers.IntegerField()
    rank = serializers.IntegerField()


from django.db import models
