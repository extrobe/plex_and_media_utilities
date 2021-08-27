import requests
import json
import re
import argparse

from requests import api

# SET THE CLI ARGUMENTS
parser = argparse.ArgumentParser()

parser.add_argument("apikey",
                    help="Your Sonarr API Key")

parser.add_argument("-u", "--url",
                    help="URL to your Sonarr Instance (without Port Number)", default="http://localhost")

parser.add_argument("-p", "--port", type=int,
                    help="Port number for your Sonarr instance", default=8989)

parser.add_argument("--print_progress",
                    help="Print progress from the scan in the terminal", default=False, action='store_true')

args = parser.parse_args()
# END

# USER ARGUMENTS
# These now get populated by argparse, but could be overwritten here
apikey = args.apikey # User API Key
url = args.url #YOUR SONARR URL
port = args.port #YOUR SONARR PORT
print_progress = args.print_progress
# END

IGNORE_DEFAULT_EPISODE_NAME = True # Ignore files where the Episode uses default episode naming?
SCRUB__AND__STRINGS = True # scrub 'and' from file name strings. Fixes & vs 'and' mismatches

# If a file covers multiple episodes, but the episodes otherwise have the same (eg Part1 & Part2), this will allow these to be handled better
# Episode must be in the format SnnExx-yy)
ALLOW_MULIT_PART_EPISODE_FILES = True

def default_episode(title):
    """Check whether the episode title has generic naming applied."""
    #return (title[:7] == "episode" and str.isnumeric(title[8:]))
    return bool(re.search('(episode[ ][0-9])',title))


def is_multi_episode(file_string):
    """Check whether the file name covers multiple episdoes."""
    return bool(re.search('(s\d{1,4}e\d{1,4}-\d{1,4})+',file_string))


def process_season(series_id, series_name):
    """Process all episodes for a given seasonID."""
    response_episode = requests.get(f'{url}:{port}/api/episode?apikey={apikey}&seriesid={series_id}')
    json_episode = json.loads(response_episode.text)

    if print_progress: print("Processing: " + str(series_id) + " | " + series_name)
    
    write_title = False

    z = 0
    for element_episode in json_episode: 
            title = element_episode['title'] #the text name of the episode
            has_file = element_episode['hasFile'] #Boolean value as to whether there is a file associated with the episode

            if has_file: #If we don't already have a file associated with the episode, we won't need to check it
                file = element_episode['episodeFile']['relativePath'] #file name we currently have for the episode

                # The next thing we need to do is compare the Titles. Files usually contain series/episode data
                # so we want to check the file name 'contains' the episode title.
                # However... because file names can't contain certain punctuation which might exist in an 
                # episode name, we need to strip out this punctuation. This also ensure your files can use periods 
                # instead of spaces, and it will still match.

                file_conv = str.lower(re.sub('[^A-Za-z0-9]+', '', file))
                title_conv = str.lower(re.sub('[^A-Za-z0-9]+', '', title))

                if SCRUB__AND__STRINGS:
                    file_conv = file_conv.replace('dvd','') # bit of a workaround!
                    file_conv = file_conv.replace('and','')

                    title_conv = title_conv.replace('dvd','') # bit of a workaround!
                    title_conv = title_conv.replace('and','')
                
                if ALLOW_MULIT_PART_EPISODE_FILES and is_multi_episode(str.lower(file)):

                    if bool(re.search('(part[0-9])+',title_conv)):
                        title_conv = str.lower(re.sub('part[0-9]', '', title_conv))
                    else:
                        title_conv = title_conv[:-1] # remove the part ID from the end of the name (eg 'Epidode Name (1)' becomes 'Episode Name')
                    #title_conv = title_conv.replace('part','') # remove the string 'part' from the file name (eg 'Episode Name Part 1' becomes 'Episode Name' (as the 1 was removed above) )

                if default_episode(str.lower(title)) and IGNORE_DEFAULT_EPISODE_NAME:
                    # This function tests is the episode title is just 'default' naming. eg 'Episode 1'
                    # In these cases, the user might not want/need 'Episode 1' in the file name.

                    pass

                elif title_conv not in file_conv:
                
                    if not write_title:
                        with open("Output.txt", "a") as text_file:
                            text_file.write("\nFound Issues For: %s" % series_name + "\n")
                            write_title = True

                    with open("Output.txt", "a") as text_file:
                        if is_multi_episode(str.lower(file)):
                            text_file.write("MULTIFILE: ")
                        text_file.write("Mismatch Found: %s" % title + " | " + file + "\n")
                        #text_file.write("Mismatch Found: %s" % title_conv + " | " + file_conv + "\n")
                    z+=1
    return z

def main():
    """Kick off the primary process."""
    print("STARTED!")

    z = 0

    with open("Output.txt", "w") as text_file:
      text_file.write("Output for for today...\n")

    response_series = requests.get(f'{url}:{port}/api/series?apikey={apikey}')
    json_series = json.loads(response_series.text)

    for element in json_series:
        series_id = element['id']
        series_name = element['title']
        z += process_season(series_id, series_name)

    print("DONE! " + str(z) + " issues found!")

    if z > 0:
        print("Check your output.txt file for details")

if __name__ == "__main__":
    main()