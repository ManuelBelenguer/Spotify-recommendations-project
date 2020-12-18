def if_not_hot(song):
########################## Ask the user for input
    print("Tell me a song that you like\n")
    
    state = True
    while state == True: ########## While loop to loop over it till the condition state = False. So it asks for input till the user enters a valid song in Spotify
        song = input()
        
    ########################## Call Spotify API to find input song   
        results = sp.search(q=song, limit=50)
        json_results = json.dumps(results, ensure_ascii=False)

    ########################### TEMPORAL: Create a list with the different artists for the song input. 
        artiste_list = []

        for i in range(len(results["tracks"]["items"])):
            artistas = results["tracks"]["items"][i]["artists"][0]["name"]
        
            if artistas not in artiste_list:
                artiste_list.append(artistas)

    ############################ While loop that will loop till the user inputs a song that's in the Spotify database.

        if len(artiste_list) != (0):            
            print("\nWhat's the artist?\n")      
            art = input() #### Ask the user to choose the artist for the entered song.
            print()
            words = art.split(' ') # Capitalization of user_input to fit with hot_list
            capi = [word.capitalize() for word in words]
            correction = ' '.join(capi)
            
            

            artist = True
            while artist == True: ### While loop to loop till the user enters a correct input for the artist of the song
                if correction in artiste_list:
                    i = artiste_list.index(correction)
                    features = sp.audio_features(results["tracks"]["items"][i]['uri']) # If the artist name is correct/in the database, it will return the features for the song.
                    artist = False
                    state = False
                   

                else:
                    print("Sorry, we don't have {} by {} in our dataset \n".format(song, art)) # Otherwise it will ask for another input, and will give an artist list for that song.
                    print("Why don't you try with a different artist from this list? \n")
                    print(artiste_list)
                    art = input()
                   
            state = False
        else:

            print("Sorry, the song you input is not in our database or it's misspelled. Please try again.\n")

############################ Remove unnecesary features
    to_remove =("type", "id", "uri", "track_href", "analysis_url","time_signature")
    unwanted_features = [features[0].pop(x) for x in to_remove]

############################ Import pickle 'scaler' + transform
    infile = open("scaling",'rb')
    scaler = pickle.load(infile)
    infile.close()
    
    transformed_features = scaler.transform(pd.DataFrame(features))
############################ Import picke model + prediction
    infile = open("model",'rb')
    model = pickle.load(infile)
    infile.close()
    
    recommendation = model.predict(transformed_features)
    return int(recommendation)




#############################################################################################################################################################################

def song_classify(song_cluster, clustered_data):
    to_recommend = clustered_data[clustered_data['cluster']==song_cluster]    
    print("Cool! See if you like:\n")
    
    nada = True
    while nada == True:
        recommendation = to_recommend.sample()
        print(recommendation['title'].to_string(index=False) +'  by '+ recommendation['artist'].to_string(index=False)+"\n")
        print('How do you find this recommendation? Good or bad?\n')
        response = input().lower()
        print()
        
    
        if response == 'good':
            print("Great! See you later!\n")
            nada = False
        elif response == 'bad':
            print("Sorry to hear that, see if you like this one then\n")
        else:
            print("Sorry I cannot understand. Try again later\n")
            break
            
            











#############################################################################################################################################################################

def hot_songs_spotify():
    playlist = sp.user_playlist_tracks("spotify", "6UeSakyzhiEt4NB3UAd6NQ")
    
    title, artist, song_id = [], [], []
    for n in range(len(playlist['items'])):
        title.append(playlist['items'][n]['track']['artists'][0]['name'])
        artist.append(playlist['items'][n]['track']['name'])
        song_id.append(playlist['items'][n]['track']['id'])
        
    df = pd.DataFrame({'artist' : artist, 'title': title, 'song_id':song_id})
    return df