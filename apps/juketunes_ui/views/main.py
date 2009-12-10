from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings

def view_main(request):
    """
    Main view for the music player.
    """
    pagevars = {
        "page_title": settings.PROGRAM_NAME,
    }

    context_instance = RequestContext(request)
    return render_to_response('juketunes_ui/index.html', pagevars, 
                              context_instance)