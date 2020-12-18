from untitled import user_input_correction
from untitled import if_not_hot
from untitled import song_classify
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

hot_data = pd.read_csv('./hot_data.csv')
not_hot_data = pd.read_csv('./to_work.csv')

print("Hi there! Let's see if I can recommend you some songs.")
print()
print("Tell me a song you like!")
print()
song = input()

user_input_correction(song)
hot_list = list(hot_data['song'])

if song in hot_list:
    print("Cool! See if you like: ")
    print()

    hot_list.remove(song)
    recommendation = hot_data.sample()
    nada = True
    while nada == True:
        print(recommendation['title'].to_string(index=False) +'  by '+ recommendation['artist'].to_string(index=False))
        print()
        hot_list.append(song)
        
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
        
else:
    song_classify(if_not_hot(song), not_hot_data)

