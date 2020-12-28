from django.shortcuts import render
from django.http import HttpResponse
from .models import Album, Artist, Contact, Booking
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def index(request):
    # request albums
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    # then format the request.
    # note that we don't use album['name'] anymore but album.name
    # because it's now an attribute.
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    context = {
        'title': 'Mon super titre',
        'albums': albums
    }
    return render(request, 'store/index.html', context)

def listing(request):
    albums_list = Album.objects.filter(available=True)
    # Slice pages
    paginator = Paginator(albums_list, 3)
    # Get current page number
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    # Return only this page albums and not others
    # formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    # message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    context = {
        'albums': albums,
        'paginate': True
    }
    return render(request, 'store/listing.html', context)

def detail(request, album_id):
    id = int(album_id) # make sure we have an integer.
    album = get_object_or_404(Album, pk=album_id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album.title, artists)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)

    # if not albums.exists():
    #     message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    # else:
    #     albums = ["<li>{}</li>".format(album.title) for album in albums]
    #     message = """
    #         Nous avons trouvé les albums correspondant à votre requête ! Les voici :
    #         <ul>{}</ul>
    #     """.format("</li><li>".join(albums))
    title = "Résultats pour la requête %s"%query
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)
