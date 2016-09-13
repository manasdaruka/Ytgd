from django.shortcuts import *
from .models import *
import urllib2, json,os
from urlparse import urlparse

# Create your views here.

key = "AIzaSyCd29eRHalUyu0KaQ0wCiaC1rUY6DZxs2o"


def index(request):
    all_songs = Song.objects.all()
    if request.method != "POST":
        return render(request, 'downloader/index.html', {'songs': all_songs})
    try:
        songs = Song.objects.filter(url=request.POST['url'])
        if len(songs) == 0:
            url = request.POST['url']
            if len(url)==0:
                return render(request, 'downloader/index.html', {'error': True, 'error_value': 'Please Enter an URL','songs': all_songs})
            name = get_name(url)
            song = Song(name=name, url=url)
            song.mp3 = True
            download_song(song)
            song.save()
            all_songs = Song.objects.all()
            response = render(request, 'downloader/index.html', {'songs': all_songs})
            return response
        else:
            return render(request, 'downloader/index.html', {'songs': all_songs})
    except Exception as E:
        return render(request, 'downloader/index.html', {'error': True, 'error_value': E,'songs': all_songs})


def download_song(song):
    curr_dir=os.getcwd()
    download_dir = "'" + curr_dir + '/songs/%(title)s.%(ext)s' + "'"
    command = 'youtube-dl -o ' + download_dir + ' --extract-audio --audio-format mp3 --audio-quality=320k ' + song.url
    os.system(command)


def get_name(url):
    video_id = urlparse(str(url)).query.split('=')[1]
    data_url = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&key=" + key + "&part=snippet"
    response = urllib2.urlopen(data_url)
    video_data = json.loads(response.read())
    return video_data['items'][0]['snippet']['title']
