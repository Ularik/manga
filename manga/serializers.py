from rest_framework import serializers
from .models import Rating, Manga, Likes, Image, Watched, Bookmarks, Comments


class RatingCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = ('user', 'manga', 'grade')

    def create(self, validated_data):
        user = validated_data['user']
        manga = validated_data['manga']
        mark = validated_data['grade']

        example = Rating.objects.filter(user=user, manga=manga).first()
        if not example:
            example = Rating.objects.create(**validated_data)
        else:
            example.grade = mark
            example.save()

        return example


class LikesCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Likes
        fields = ('user', 'manga')

    def create(self, validated_date):

        like = Likes.objects.filter(**validated_date).first()
        if not like:
            return Likes.objects.create(**validated_date)

        return like


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comments
        fields = ('user', 'manga', 'text')


class BookmarksSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Bookmarks
        fields = ('user', 'manga')

    def create(self, validated_data):

        bookmark = Bookmarks.objects.filter(**validated_data).first()
        if not bookmark:
            return Bookmarks.objects.create(**validated_data)

        return bookmark


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comments
        fields = ('user', 'text')


class RatingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('user', 'grade')


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('file',)


class MangaCreateSerializer(serializers.ModelSerializer):
   # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Manga
        fields = ('user', 'title', 'genre', 'images', 'comix_file')


class MangaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manga
        fields = ('id', 'title', 'images', 'grades', 'created_date')


class MangaDetailSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True)

    class Meta:
        model = Manga
        fields = ('id', 'user', 'title', 'images', 'description', 'genre',
                  'comix_file', 'comments', 'likes', 'grades', 'watches', 'bookmarks')


class WatchedCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watched
        fields = ('manga',)

    def create(self, validated_data):

        my_data = Watched(**validated_data)
        my_data.save()
        return my_data