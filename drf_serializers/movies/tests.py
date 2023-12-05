from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Resource, UserProfile, Comment, ModelA, ModelB, ModelC
from .serializers import MovieSerializer, ResourceSerializer, UserSerializer, CommentSerializer, ModelASerializer
from rest_framework.exceptions import ValidationError


class MovieSerializerTest(TestCase):
    
    def setUp(self):
        self.valid_data = {
            "title": "Example Movie",
            "description": "A description of the movie",
            "release_date": "2020-01-01",
            "rating": 5,
            "us_gross": 100000,
            "worldwide_gross": 200000
        }

    def test_valid_movie_data(self):
        serializer = MovieSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_rating(self):
        invalid_data = self.valid_data.copy()
        invalid_data['rating'] = 11  # Out of the valid range
        serializer = MovieSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_us_gross_higher_than_worldwide_gross(self):
        invalid_data = self.valid_data.copy()
        invalid_data['us_gross'] = 300000
        invalid_data['worldwide_gross'] = 200000
        serializer = MovieSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ResourceSerializerTest(TestCase):
    
    def setUp(self):
        # Creating users for testing
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.resource_data = {
            "title": "Test Resource",
            "content": "Some content"
        }
        self.resource = Resource.objects.create(title="Test Resource", content="Some content")
        self.resource.liked_by.set([self.user1.pk, self.user2.pk])

    def test_resource_serializer_representation(self):
        serializer = ResourceSerializer(instance=self.resource)
        data = serializer.data
        self.assertEqual(data['likes'], 2)

    def test_resource_serializer_internal_value(self):
        resource_data = {
            "info": {
                "extra": "data",
            },
            "resource": {
                "title": "Test Resource",
                "content": "Some content",
                "liked_by": [self.user1.pk]
            }
        }
        serializer = ResourceSerializer(data=resource_data['resource'])
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())


class UserSerializerTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com')
        UserProfile.objects.create(user=self.user, bio='This is my bio.', birth_date='1995-04-27')

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['active'], self.user.is_active)
        self.assertEqual(data['full_name'], self.user.get_full_name())
        self.assertEqual(data['bio'], self.user.userprofile.bio)
        self.assertEqual(data['birth_date'], '1995-04-27')
        

class NestedSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.comment = Comment.objects.create(author=self.user, content='A sample comment')
        self.model_c = ModelC.objects.create(content='Content C')
        self.model_b = ModelB.objects.create(model_c= self.model_c, content='Content B')
        self.model_a = ModelA.objects.create(model_b=self.model_b, content='Content A')
    
    def test_comment_serializer(self):
        serializer = CommentSerializer(instance=self.comment)
        self.assertEqual(serializer.data['author']['username'], 'testuser')

    def test_model_a_serializer_depth(self):
        serializer = ModelASerializer(instance=self.model_a)
        self.assertTrue('model_b' in serializer.data)
        self.assertIsInstance(serializer.data['model_b'], dict)
        self.assertTrue('model_c' in serializer.data['model_b'])  # Checks if 'model_c' is in the 'model_b' dictionary
        self.assertEqual(serializer.data['model_b']['content'], 'Content B')  # Check for content of ModelB
