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
    artist_qset = Song.objects.values_list('artist', flat=True).distinct().order_by('artist')
    artist_count = artist_qset.count()
    artist_list = list(artist_qset)
    
    response_dict = {"results": artist_list, "record_count": artist_count}
    message = JSMessage("Success.", contents=response_dict)

    return HttpResponse(message)