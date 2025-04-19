from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, Booking, Category, Review, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# Existing serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'receiver', 'item', 'content', 'timestamp']
        read_only_fields = ['sender']  # Make sender read-only


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'item', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer']  # Make owner read-only

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    photo = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'location', 'available', 'category', 'category_id', 'price', 'photo','reviews', 'latitude', 'longitude']
        read_only_fields = ['owner']  # Make owner read-only

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        elif obj.photo:
            return obj.photo.url
        return None


class BookingSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'item', 'item_id', 'start_time', 'end_time', 'status', 'total_price']
        read_only_fields = ['renter']  # Make owner read-only

