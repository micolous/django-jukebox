from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from includes.json import JSMessage
from apps.music_db.models import Song

def ajax_get_artist_list(request):
    """
    Processes the AJAX request to search the catalog. Returns JSON results.
    """  
    artist_qset = Song.objects.values('artist').distinct().order_by('artist')
    artist_count = artist_qset.count()
    artist_list = list(artist_qset)
    
    response_dict = {"results": artist_list, "record_count": artist_count}
    message = JSMessage("Success.", contents=response_dict)

    return HttpResponse(message)

def ajax_get_album_list(request):
    """
    Processes the AJAX request to search the catalog. Returns JSON results.
    """  
    artist_qset = Song.objects.values('album').distinct().order_by('album')
    artist_count = artist_qset.count()
    artist_list = list(artist_qset)
    
    response_dict = {"results": artist_list, "record_count": artist_count}
    message = JSMessage("Success.", contents=response_dict)

    return HttpResponse(message)

def ajax_get_song_list(request):
    """
    Processes the AJAX request to search the catalog. Returns JSON results.
    """
    if not request.GET or not request.GET.get('query', False):
        artist_count = 0
        artist_list = []
    else:
        artist_qset = Song.objects.values('title').order_by('title')
        artist_count = artist_qset.count()
        artist_list = list(artist_qset)
    
    response_dict = {"results": artist_list, "record_count": artist_count}
    message = JSMessage("Success.", contents=response_dict)

    return HttpResponse(message)