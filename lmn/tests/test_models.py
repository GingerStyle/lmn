from django.test import TestCase

from django.contrib.auth.models import CustomUser
from django.db import IntegrityError
# Create your tests here.


class TestUser(TestCase):

    def test_create_user_duplicate_username_fails(self):

        user = CustomUser(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = CustomUser(username='bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_username_case_insensitive_fails(self):

        user = CustomUser(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = CustomUser(username='Bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_email_fails(self):
        user = CustomUser(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = CustomUser(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_email_case_insensitive_fails(self):
        user = CustomUser(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = CustomUser(username='another_bob', email='Bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()
