import requests
import json

from requests import api
#response = requests.get('http://192.168.1.208:8989/api/episode?apikey={apikey}&seriesid={series}&episodenumber={episodenumber}')

apikey = ''
url = 'http://192.168.1.208'
port = '8989'

def process_season(series_id):
    response_episode = requests.get(f'{url}:{port}/api/episode?apikey={apikey}&seriesid={series_id}')
    json_episode = json.loads(response_episode.text)

    print(series_id)
    #print(response_episode.text)

    n=0
    for element_episode in json_episode: 
            title = json_episode[n]['title']
            has_file = json_episode[n]['hasFile']
            #print(has_file)

            if has_file:

                file = json_episode[n]['episodeFile']['relativePath']
                if str.lower(title) not in str.lower(file):
                    print('Mismatch Found: ' + title + " | " + file)
#                else:
#                    print('Looks Good: ' + title + " | " + file)
#            else:
#                print('Skipped:' + title)
            n=n+1


response_series = requests.get(f'{url}:{port}/api/series?apikey={apikey}')
json_series = json.loads(response_series.text)

y=0
for element in json_series:
    series_id = json_series[y]['id']
    series_name = json_series[y]['title']
    print(str(series_id) + ' | ' + series_name)
    if y <=3:
        process_season(series_id)
    y=y+1






#response = requests.get(f'http://192.168.1.208:8989/api/episode?apikey={apikey}&seriesid={series}&episodenumber={episodenumber}')

#response = requests.get(f'http://192.168.1.208:8989/api/episode?apikey={apikey}&seriesid={series}')

#print(response.text)

#n=0
#json_object = json.loads(response.text)
#for element in json_object: 
#        title = json_object[n]['title']
#        file = json_object[n]['episodeFile']['relativePath']
#        if title not in file:
#            print('Mismatch Found: ' + title + " | " + file)
#        n=n+1

#print(response.json())

#if response:
#  print('Request is successful.')
#else:
#  print('Request returned an error.')

  #data = response.json()