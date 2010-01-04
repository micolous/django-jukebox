"""
Views for Music Player interface.
"""
from django.conf import settings
from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.core.urlresolvers import reverse
from apps.music_db.models import Song, SongRating, SONG_RATINGS
from apps.music_player.models import SongRequest
from includes.json import JSMessage

class SongUploadForm(ModelForm):
    """
    File Upload form.
    """
    class Meta:
        model = Song
        fields = ('file',)

def music_player_main(request):
    """
    Main view for the music player.
    """
    pagevars = {
        "page_title": settings.PROGRAM_NAME,
        "song_upload_form": SongUploadForm(),
    }

    context_instance = RequestContext(request)
    return render_to_response('index.html', pagevars, 
                              context_instance)
    
def process_song_upload(request):
    """
    Processes the form data from the upload section of the index
    page. 
    """
    if request.POST:
        form = SongUploadForm(request.POST, request.FILES)
    else:
        return HttpResponse("No data")
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('music_player-edit_song',
                                            args=[form.instance.id]))
    else:
        return HttpResponse("Invalid data")

class SongEditForm(ModelForm):
    """
    File Upload form.
    """
    class Meta:
        model = Song
        fields = ('artist', 'album', 'title', 'disc_number', 'track_number')

def edit_song(request, song_id):
    """
    Renders the song editing page.
    """
    pagevars = {}
    song = get_object_or_404(Song, id=song_id)
    
    if request.POST:
        form = SongEditForm(request.POST, instance=song)
    else:
        form = SongEditForm(instance=song)
    pagevars['form'] = form

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('music_player_main'))

    context_instance = RequestContext(request)
    return render_to_response('song_edit_form.html', pagevars, 
                              context_instance)

class SongRatingForm(ModelForm):
    """
    This form is used in the Currently Playing bar at the top. It is only
    really used for rendering, not validation.
    """
    class Meta:
        model = SongRating
        fields = ('rating',)
        
    def __init__(self, *args, **kwargs):
        super(SongRatingForm, self).__init__(*args, **kwargs)
        
        # In very rare instances, we might not have a current song playing.
        # Rather than throw server errors, just send a -1, which the
        # Javascript understands means no song.
        if self.instance:
            song_id = self.instance.song.id
        else:
            song_id = -1
        
        # Set the JavaScript event handler for sending ratings.
        self.fields["rating"].widget.attrs = {
            'onchange': 'javascript:rating_change_handler(%s)' % song_id
        }
    
def display_currently_playing(request):
    """
    The logic for the "CURRENTLY PLAYING" header at the top. Also renders the
    drop-down for rating songs.
    """
    try:
        currently_playing_track = SongRequest.objects.filter(time_played__isnull=False).order_by('-time_played')[0]
    except IndexError:
        currently_playing_track = None
        
    pagevars = {
        "currently_playing_track": currently_playing_track,
    }
    
    if currently_playing_track and request.user.is_authenticated():
        # Only allow logged in users to rate songs.
        rating, created = SongRating.objects.get_or_create(
                                        song=currently_playing_track.song,
                                        user=request.user)
        # Make this a bound form.
        form = SongRatingForm(instance=rating)
    else:
        form = None
        
    pagevars["rating_form"] = form

    context_instance = RequestContext(request)
    return render_to_response('currently_playing.html', pagevars, 
                              context_instance)
    
def rate_song(request, song_id, rating):
    """
    Rates a song.
    """
    song = get_object_or_404(Song, id=song_id)

    request_user = request.user
    if not request.user.is_authenticated():
        # Can't store AnonymousUser objects in a ForeignKey to User.
        # Only allow auth'd users to rate.
        return HttpResponse(JSMessage("User not authenticated.", 
                                      is_error=True))
    else:
        rating_obj, created = SongRating.objects.get_or_create(song=song, 
                                                           user=request.user)
        if rating < 0:
            # A rating of 0 means no rating. Let them un-rate songs they
            # have rated, like iTunes.
            rating = None

        rating_obj.rating = rating
        rating_obj.save()
        return HttpResponse(JSMessage("Rating sent."))

def display_song_queue(request):
    """
    Display the song queue. Previously played, currently playing, upcoming
    user requests, then upcoming random requests.
    """
    try:
        currently_playing_track = SongRequest.objects.filter(time_played__isnull=False).order_by('-time_played')[0]
        recently_played_tracks = SongRequest.objects.filter(time_played__isnull=False).exclude(id=currently_playing_track.id).order_by('-time_played')[:settings.NUMBER_OF_PREVIOUS_SONGS_DISPLAY]
    except IndexError:
        currently_playing_track = None
        recently_played_tracks = SongRequest.objects.filter(time_played__isnull=False).order_by('-time_played')[:settings.NUMBER_OF_PREVIOUS_SONGS_DISPLAY]
    
    """
    Determine total number of songs being displayed. Display as many songs as
    have been requested by users, but if that number is less than the 
    LIMIT_UPCOMING_SONGS_DISPLAY setting, fill out with randomly generated requests
    until that number is reached.
    """
    total_displayed_songs = settings.LIMIT_UPCOMING_SONGS_DISPLAY
    upcoming_requested_tracks = SongRequest.objects.get_pending_user_requests()    
    if upcoming_requested_tracks.count() < total_displayed_songs:
        random_song_display_limit = total_displayed_songs - upcoming_requested_tracks.count()
        upcoming_random_tracks = SongRequest.objects.get_pending_anonymous_requests()[:random_song_display_limit]
    else:
        upcoming_random_tracks = None

    pagevars = {
        "page_title": "Song Queue",
        "recently_played_tracks": recently_played_tracks,
        "currently_playing_track": currently_playing_track,
        "upcoming_requested_tracks": upcoming_requested_tracks,
        "upcoming_random_tracks": upcoming_random_tracks,
    }

    context_instance = RequestContext(request)
    return render_to_response('song_list.html', pagevars, 
                              context_instance)

class SongSearchForm(forms.Form):
    """
    Search form model. Only one field that will search across multiple columns.
    """
    keyword = forms.CharField()

def song_search(request):
    """
    Search form for songs. Find songs, request them... pretty basic.
    """
    total_songs = Song.objects.all().count()
    pagevars = {
        "page_title": "Song Search",
        "form": SongSearchForm(),
        "total_songs": total_songs,
    }
    
    context_instance = RequestContext(request)
    return render_to_response('song_search.html', pagevars, 
                              context_instance)
        
def song_upload(request):
    """
    Upload form for songs.
    """    
    pagevars = {
        "page_title": "Song Upload",
        "form": SongUploadForm(),
    }
    
    context_instance = RequestContext(request)
    return render_to_response('song_upload.html', pagevars, 
                              context_instance)
        
def song_search_results(request, qset=Song.objects.all()):
    """
    Query Song model based on search input.
    """
    form = SongSearchForm(request.POST)
    
    if request.POST and form.is_valid():
        s_search = form.cleaned_data.get("keyword", None)
        if s_search:
            qset = qset.filter(Q(artist__icontains=s_search) |
                               Q(title__icontains=s_search) |
                               Q(album__icontains=s_search) |
                               Q(genre__icontains=s_search)).order_by('artist', 
                                                                      'title')
    else:
        qset = qset.order_by('?')[:10]
        
    pagevars = {
        "qset": qset,
    }
    
    context_instance = RequestContext(request)
    return render_to_response('song_results.html', pagevars, 
                              context_instance)
            
def request_song(request, song_id):
    """
    Create a new SongRequest object for the given song id.
    """
    request_user = request.user
    if not request.user.is_authenticated():
        # Set this to None to avoid storing an AnonymousUser in the
        # SongRequest (this would raise an exception).
        request_user = None
        # You can allow anonymous user requests in settings.py.
        if not settings.ALLOW_ANON_REQUESTS:
            # Anonymous user requests not allowed, error out.
            message = JSMessage("You must be logged in to request songs.", 
                                is_error=True)
            return HttpResponse(message)

    # Look the song up and create a request.
    song = Song.objects.get(id=song_id)
    if SongRequest.objects.get_active_requests().filter(song=song):
        # Don't allow requesting a song that is currently in the queue.
        return HttpResponse(JSMessage("Song has already been requested.", 
                                      is_error=True))
    else:
        # Song isn't already in the SongRequest queue, add it.
        request = SongRequest(song=song, requester=request_user)
        request.save()
        return HttpResponse(JSMessage("Song Requested."))