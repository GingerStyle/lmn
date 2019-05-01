from . import views, views_artists, views_venues, views_notes, views_users

from django.urls import path, re_path
from django.contrib.auth import views as auth_views


app_name = 'lmn'

urlpatterns = [

    path('', views.homepage, name='homepage'),

    # Path for autocomplete requests
    re_path(r'^ajax_calls/search/', views.autocompleteModel),

    # Venue-related
    path('venues/list/', views_venues.venue_list, name='venue_list'),
    path('venues/detail/<int:venue_pk>/', views_venues.venue_detail, name='venue_detail'),
    path('venues/artists_at/<int:venue_pk>/', views_venues.artists_at_venue, name='artists_at_venue'),

    path('shows/popular/', views_notes.popular_shows, name='popular_shows'),
    # Note related
    path('notes/popular/', views_notes.popular_notes, name='popular_notes'),
    path('notes/latest/', views_notes.latest_notes, name='latest_notes'),
    path('notes/detail/<int:note_pk>/', views_notes.note_detail, name='note_detail'),
    path('notes/for_show/<int:show_pk>/', views_notes.notes_for_show, name='notes_for_show'),
    path('notes/add/<int:show_pk>/', views_notes.new_note, name='new_note'),
    path('notes/like/<int:note_pk>/', views_notes.add_note_like, name='like_note'),
    path('notes/dislike/<int:note_pk>/', views_notes.add_note_dislike, name='dislike_note'),
    path('notes/delete/<int:note_pk>/', views_notes.delete_note, name='delete_note'),
    path('notes/edit/<int:note_pk>/', views_notes.edit_note, name='edit_note'),
    # Artist related
    path('artists/list/', views_artists.artist_list, name='artist_list'),
    path('artists/detail/<int:artist_pk>/', views_artists.artist_detail, name='artist_detail'),
    path('artists/venues_played/<int:artist_pk>/', views_artists.venues_for_artist, name='venues_for_artist'),

    # User related
    path('user/profile/<int:user_pk>/', views_users.user_profile, name='user_profile'),
    path('user/profile/', views_users.my_user_profile, name='my_user_profile'),
    path('user/profile/edit/', views_users.edit_profile, name='edit_profile'),

    # Account related

    path('accounts/login/', views_users.login_and_signup, name='login'),
    path('accounts/logout/', views_users.logout_user, name='logout'),
    path('register/', views_users.register, name='register'),
]
