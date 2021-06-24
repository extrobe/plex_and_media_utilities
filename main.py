import requests
import json
import re

from requests import api

#UPDATE THESE THREE VALUES!!
apikey = '000000' #YOUR API KEY
url = 'http://192.168.1.208' #YOUR SONARR URL
port = '8989' #YOUR SONARR PORT
#END

ignore_default_episdode_name = True # Ignore files where the Episode uses default episode naming?
scrub__and__strings = True # scrub 'and' from file name strings. Fixes & vs 'and' mismatches
z=0




def default_episode(title):
    if title[:7] == "Episode" and str.isnumeric(title[8:]):
        return True
    
    return False

def process_season(series_id):
    global z
    response_episode = requests.get(f'{url}:{port}/api/episode?apikey={apikey}&seriesid={series_id}')
    json_episode = json.loads(response_episode.text)

    print("Processing: " + str(series_id) + " | " + series_name)
    
    write_title = False

    for element_episode in json_episode: 
            title = element_episode['title'] #the text name of the episode
            has_file = element_episode['hasFile'] #Boolean value as to whether there is a file associated with the episode

            
            if has_file: #If we don't already have a file associated with the episode, we won't need to check it
                file = element_episode['episodeFile']['relativePath'] #file name we currently have for the episode

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

                if scrub__and__strings:
                    file_conv = file_conv.replace('and','')
                    title_conv = title_conv.replace('and','')

                if default_episode(title) and ignore_default_episdode_name:
                    #print("default episdode ordering")
                    #chk_string = "E" + title[:8]

                    # This function tests is the episode title is just 'default' naming. eg 'Episode 1'
                    # In these cases, the user might not want/need 'Episode 1' in the file name.
                    # What I'd like to do is then test the S01E01 matches, but for now, we'll just test for it with the option to skip these files

                    1==1

                elif title_conv not in file_conv:
                
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


print("STARTED!")

with open("Output.txt", "w") as text_file:
    text_file.write("Output for for today...\n")

response_series = requests.get(f'{url}:{port}/api/series?apikey={apikey}')
json_series = json.loads(response_series.text)

for element in json_series:
    series_id = element['id']
    series_name = element['title']
    process_season(series_id)

print("DONE! " + str(z) + " issues found!")

if z > 0:
    print("Check your output.txt file for details")