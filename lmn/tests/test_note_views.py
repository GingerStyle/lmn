from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import auth

from lmn.models import Venue, Artist, Note, Show, LikeNote
from lmn.models import CustomUser

import re, datetime
from datetime import timezone


class TestNotes(TestCase):
    fixtures = [ 'testing_likenotes', 'testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes']  # Have to add artists and venues because of foreign key constrains in show

    def test_latest_notes(self):
        response = self.client.get(reverse('lmn:latest_notes'))
        expected_notes = list(Note.objects.all())
        # Should be note 3, then 2, then 1
        context = response.context['notes']
        first, second, third = context[0], context[1], context[2]
        self.assertEqual(first.pk, 3)
        self.assertEqual(second.pk, 2)
        self.assertEqual(third.pk, 1)


    def test_notes_for_show_view(self):
        # Verify correct list of notes shown for a Show, most recent first
        # Show 1 has 2 notes with PK = 2 (most recent) and PK = 1
        response = self.client.get(reverse('lmn:notes_for_show', kwargs={'show_pk':1}))
        context = response.context['notes']
        first, second = context[0], context[1]
        self.assertEqual(first.pk, 2)
        self.assertEqual(second.pk, 1)


    def test_correct_templates_uses_for_notes(self):
        response = self.client.get(reverse('lmn:latest_notes'))
        self.assertTemplateUsed(response, 'lmn/notes/note_list.html')

        response = self.client.get(reverse('lmn:note_detail', kwargs={'note_pk':1}))
        self.assertTemplateUsed(response, 'lmn/notes/note_detail.html')

        response = self.client.get(reverse('lmn:notes_for_show', kwargs={'show_pk':1}))
        self.assertTemplateUsed(response, 'lmn/notes/note_list.html')

        # Log someone in
        self.client.force_login(CustomUser.objects.first())
        response = self.client.get(reverse('lmn:new_note', kwargs={'show_pk':1}))
        self.assertTemplateUsed(response, 'lmn/notes/new_note.html')

    def test_no_notes_for_user(self):
        self.client.force_login(CustomUser.objects.get(pk="3"))
        response = self.client.get(reverse('lmn:user_profile', kwargs={'user_pk': 3}), follow=True)
        self.assertContains(response, 'No notes.')
        self.assertEqual(response.status_code, 200)

    def test_most_popular_notes(self):
        response = self.client.get(reverse('lmn:popular_notes'), follow=True)
        context = response.context['notes'][0]
        self.assertEqual(context.pk, 3)


class TestAddNotesWhenUserLoggedIn(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)


    def test_save_note_for_non_existent_show_is_error(self):
        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':100})
        response = self.client.post(new_note_url)
        self.assertEqual(response.status_code, 404)


    def test_can_save_new_note_for_show_blank_data_is_error(self):

        initial_note_count = Note.objects.count()

        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})

        # No post params
        response = self.client.post(new_note_url, follow=True)
        # No note saved, should show same page
        self.assertTemplateUsed('lmn/notes/new_note.html')

        # no title
        response = self.client.post(new_note_url, {'text':'blah blah' }, follow=True)
        self.assertTemplateUsed('lmn/notes/new_note.html')

        # no text
        response = self.client.post(new_note_url, {'title':'blah blah' }, follow=True)
        self.assertTemplateUsed('lmn/notes/new_note.html')

        # nothing added to database
        self.assertEqual(Note.objects.count(), initial_note_count)   # 2 test notes provided in fixture, should still be 2


    def test_add_note_database_updated_correctly(self):

        initial_note_count = Note.objects.count()

        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})

        response = self.client.post(new_note_url, {'text':'ok', 'title':'blah blah' }, follow=True)

        # Verify note is in database
        new_note_query = Note.objects.filter(text='ok', title='blah blah')
        self.assertEqual(new_note_query.count(), 1)

        # And one more note in DB than before
        self.assertEqual(Note.objects.count(), initial_note_count + 1)

        # Date correct?
        now = datetime.datetime.today()
        posted_date = new_note_query.first().posted_date
        self.assertEqual(now.date(), posted_date.date())  # TODO check time too


    def test_redirect_to_note_detail_after_save(self):

        initial_note_count = Note.objects.count()

        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})
        response = self.client.post(new_note_url, {'text':'ok', 'title':'blah blah' }, follow=True)
        new_note = Note.objects.filter(text='ok', title='blah blah').first()

        self.assertRedirects(response, reverse('lmn:note_detail', kwargs={'note_pk': new_note.pk }))


class TestAddLikeNotes(TestCase):
    fixtures = ['testing_likenotes', 'testing_users', 'testing_artists', 'testing_venues', 'testing_shows',
                'testing_notes']  # Have to add artists and venues because of foreign key constrains in show

    def test_add_like_notes(self):
        self.client.force_login(CustomUser.objects.get(pk="3"))
        response = self.client.post(reverse('lmn:like_note', kwargs={'note_pk': 3}), follow=True)
        self.assertEqual(response.status_code, 200)
        note = Note.objects.get(pk="3")
        self.assertNotEqual(note.likes, 23)
        self.assertEqual(note.likes, 24)
        query = LikeNote.objects.filter(user=3)
        like = get_object_or_404(query, note=3).value
        self.assertEqual(like, 1)
        self.assertContains(response, 'Likes: 24')
    def test_add_dislike_note_already_disliked(self):
        self.client.force_login(CustomUser.objects.get(pk="3"))
        response = self.client.post(reverse('lmn:dislike_note', kwargs={'note_pk': 3}), follow=True)
        self.assertEqual(response.status_code, 200)
        note = Note.objects.get(pk="3")
        self.assertNotEqual(note.likes, 22)
        self.assertEqual(note.likes, 23)
        query = LikeNote.objects.filter(user=3)
        dislike = get_object_or_404(query, note=3).value
        self.assertEqual(dislike, -1)
        self.assertContains(response, 'Likes: 23')


class TestEditNotes(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']
    def test_edit_note_user_not_logged_in(self):
        response = self.client.get(reverse('lmn:edit_note', kwargs={'note_pk':1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_edit_note_user_logged_in(self):
        user = CustomUser.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('lmn:edit_note', kwargs={'note_pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lmn/notes/edit_note.html')
    def test_post_edit_note(self):
        user = CustomUser.objects.get(pk=1)
        self.client.force_login(user)
        note = Note.objects.get(pk=1)
        text = note.text
        response = self.client.post(reverse('lmn:edit_note', kwargs={'note_pk': 1}),
                                    {'title': 'ok', 'text': 'not bad', 'rating': 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lmn/notes/note_detail.html')
        expected = Note.objects.get(pk=1)
        expectedText = expected.text
        self.assertNotEqual(text, expectedText)

    def test_post_edit_another_users_note(self):
        user = CustomUser.objects.get(pk=2)
        self.client.force_login(user)
        response = self.client.post(reverse('lmn:edit_note', kwargs={'note_pk': 1}),
                                    {'title': 'ok', 'text': 'not bad', 'rating': 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lmn/notes/note_list.html')

    def test_delete_note(self):
        user = CustomUser.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('lmn:delete_note', kwargs={'note_pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lmn/notes/note_list.html')

        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk__exact='1')
