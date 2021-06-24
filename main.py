import requests
import json
import re

from requests import api

#UPDATE THESE THREE VALUES!!
apikey = '000000000000' #YOUR API KEY
url = 'http://192.168.1.208' #YOUR SONARR URL
port = '8989' #YOUR SONARR PORT
#END

z=0

def process_season(series_id):
    global z
    response_episode = requests.get(f'{url}:{port}/api/episode?apikey={apikey}&seriesid={series_id}')
    json_episode = json.loads(response_episode.text)

    print("Processing: " + str(series_id) + " | " + series_name)
    
    n=0
    write_title = False

    for element_episode in json_episode: 
            title = json_episode[n]['title'] #the text name of the episode
            has_file = json_episode[n]['hasFile'] #Boolean value as to whether there is a file associated with the episode

            
            if has_file: #If we don't already have a file associated with the episode, we won't need to check it
                file = json_episode[n]['episodeFile']['relativePath'] #file name we currently have for the episode

                # The next thing we need to do is sompare the Titles. Files usually contain series/episode data
                # so we want to check the file name 'contains' the episode title.
                # However... because file names can't contain certain punctuation which might exist in an 
                # episode name, we need to strip out this punctuation. This also ensure your files can use periods 
                # instead of spaces, and it will still match.
                #
                # There are two ways we can strip out this. the built in function e.alpha() keeps only alpha characters.
                # I found this too loose, as it also removed numeric values, which I didn't want. Comment this out if you'd
                # prefer this stricter approach. Instead Regex is easier to use and is the default choice

                # LOOSE
                #file_conv = str.lower(''.join(e for e in file if e.alpha()))
                #title_conv = str.lower(''.join(e for e in title if e.alpha()))

                # SNUG
                file_conv = str.lower(re.sub('[^A-Za-z0-9]+', '', file))
                title_conv = str.lower(re.sub('[^A-Za-z0-9]+', '', title))

                # TIGHT (Don't recommend)
                #file_conv = file
                #title_conv = title

                if title_conv not in file_conv:
                
                    if not write_title:
                        with open("Output.txt", "a") as text_file:
                            text_file.write("\nFound Issues For: %s" % series_name + "\n")
                            write_title = True

                    #print('Mismatch Found: ' + title + " | " + file) # just for debugging

                    with open("Output.txt", "a") as text_file:
                        text_file.write("Mismatch Found: %s" % title + " | " + file + "\n")
                    z=z+1
#                else: #just for debugging
#                    print('Looks Good: ' + title + " | " + file)
#            else: #just for debugging
#                print('Skipped:' + title)
            n=n+1 # iterate



print("STARTED!")

with open("Output.txt", "w") as text_file:
    text_file.write("Output for for today...\n")

response_series = requests.get(f'{url}:{port}/api/series?apikey={apikey}')
json_series = json.loads(response_series.text)



y=0
for element in json_series:
    series_id = json_series[y]['id']
    series_name = json_series[y]['title']
    #print(str(series_id) + ' | ' + series_name)
    #if y <=3:
    process_season(series_id)
    y=y+1

print("DONE! " + str(z) + " issues found!")

if z > 0:
    print("Check your output.txt file for details")