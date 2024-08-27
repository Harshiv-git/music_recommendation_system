from django.shortcuts import render
import joblib
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='34b9c1cfda274b958b9ee8e3709cfb3d',client_secret='5c9dc4dc63f34ddf835f2fa9e214dfd7'))

#Load dataset with feature column
music_list = pickle.load(open(r'C:\Users\HV PAINTER\Desktop\Music_Recommendation_system\Search\Music_dict1.pkl','rb'))
music = pd.DataFrame(music_list)


# Create your views here.
@login_required
def recommend(request):
    if request.method == 'POST':
            searched = request.POST.get('songs')
            if searched is not None:
                distance = []
                song = music[(music.name.str.lower() == searched.lower())].head(1).values[0]
                rec = music[music.name.str.lower() != searched.lower()]
                
                for songs in tqdm(rec.values):
                    d = 0
                    for col in np.arange(len(rec.columns)):
                        if not col in [1, 3,8, 14, 16]:
                            d = d + np.absolute(float(song[col]) - float(songs[col]))
                    distance.append(d)
                rec['distance'] = distance
                rec = rec.sort_values('distance')
                columns = {}
                #name = rec['name'][:10]
                columns['name'] = rec['name'][:10].tolist()
                print("before track")
                track_image_urls = {}
                track_ids = []
                track_ids = rec['id'][:10]
                for track_id in track_ids:
                    track_data = spotify.track(track_id)
                    image_url = track_data['album']['images'][0]['url']  # Access highest resolution image
                    track_image_urls[track_id] = image_url
                track_img = list(track_image_urls.values())
                data = [{'names': name, 'image_url': image_url} for name, image_url in zip(columns['name'], track_img)]
                context = {'data': data}
                return render(request,'index.html',context)
    else:
        return render(request,'index.html')
@login_required
def index(request):
    
        
        if request.method == 'POST':
            searched = request.POST.get('query')
            if searched is not None:
                song = song.filter(Track_Name__icontains = searched)
                
                
                context = {
                
                    'qs': song,
                    'msg' : 'message is passed',
                    'pre' : '/#prediction',
                    }
                print("This is POST of Spotify search")
                return render(request,'index.html',context)
                
                
        else:
            print("This is GET")
            context = {'recomm': 'Recommends here!'}
            return render(request,'index.html',context)
        '''if request.method == 'POST':
            context = {'prediction' : '/#prediction'}
            return render(request,'index.html',context)
        else:
            return render(request,'index.html')'''

def prediction(request):
    
    print("Comes to prediction")
    
    model = joblib.load('Model1.sav')

    lis = []
    if request.method == 'POST':
        print("This is post")
        lis.append(request.POST.get('acousticness'))
        lis.append(request.POST.get('danceability'))
        lis.append(request.POST.get('duration_ms'))
        lis.append(request.POST.get('energy'))
        lis.append(request.POST.get('explicit'))
        lis.append(request.POST.get('instrumentalness'))
        lis.append(request.POST.get('key'))
        lis.append(request.POST.get('liveness'))
        lis.append(request.POST.get('loudness'))
        lis.append(request.POST.get('mode'))
        lis.append(request.POST.get('speechiness'))
        lis.append(request.POST.get('tempo'))
        lis.append(request.POST.get('valence'))
        
        print(lis)
        ans = model.predict([lis])
        print("goes to POST")
        return render(request,"index.html",{'ans':ans,'lis':lis}) 

    else:
        print("goes to GET")
        return render(request,"index.html")
def pre(request):
    response = redirect('/#prediction')
    return response


    