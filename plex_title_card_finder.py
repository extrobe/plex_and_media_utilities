import requests
import praw
import json
import re
import os

sonarr_apikey = 'xxx' ## Add your Sonarr API Key
sonarr_url = 'http://192.168.1.208' ## Add your Sonarr URL
sonarr_port = 8989 ## Add your Sonarr Port (Default 8989)

####################################################################################
# Root path for your assets. Allows us to check if there are already any assets    #
####################################################################################
ASSET_ROOT = '/Volumes/assets/tv'
ASSET_FILTER = True

####################################################################################
# Create a comma separate list of users you want to exclude from the results       #
####################################################################################
EXCLUDE_AUTH = ["user1","user2"]

####################################################################################
# When set to True, ignores any submissions that appear to be for a single episode #
####################################################################################
FULL_PACK_ONLY = True


def process_season(series_id, series_name):

    print("scanning... for " + series_name)

    write_title = False
    y = 0

    reddit = praw.Reddit(
    client_id="xxx", ## Add your Reddit Client ID
    client_secret="xxx", ## Add your Reddit Secret
    redirect_uri="http://localhost:8080",
    user_agent="Plex Title Card Matcher",
    )

    reddit.read_only = True


    for submission in reddit.subreddit("PlexTitleCards").search(series_name, limit=None):

        author = submission.author.name
        flair = submission.link_flair_text
        if flair is not None and bool(re.search('request',str.lower(''.join(map(str, flair))))):
            pass

        elif author not in EXCLUDE_AUTH:

            if FULL_PACK_ONLY and not is_fullpack(submission.title):
                pass
            else:
                if not write_title:
                    with open("Output_Plex_TitleCards.txt", "a") as text_file:
                        text_file.write("\n### Results Found For: %s" % series_name + " ###\n")
                        write_title = True

                with open("Output_Plex_TitleCards.txt", "a") as text_file:
                    text_file.write(submission.title + "\n")
                    text_file.write("     " + "https://www.reddit.com" + submission.permalink + "\n")
                    text_file.write("     " + author + "\n")
                
                y = y+1

    if y == 0:
        print("no results found")
    
    print("")

def is_fullpack(submission_name):
    """Audits the submission name to detirmine if it's a single episode or a full pack"""
    return not bool(re.search('(s\d{1,4}e\d{1,4})+',str.lower(submission_name)))

def asset_exists(series_path):
    """Check if the asset folder already has assets for this series"""
    validation_path = ASSET_ROOT + series_path[series_path.rfind('/'):]

    for files in os.walk(validation_path):
        return bool(re.search('(s\d{1,4}e\d{1,4})+', str.lower(''.join(map(str, files))) ))

def main():
    """Kick off the primary process."""
    print("STARTED!")

    z = 0

    with open("Output_Plex_TitleCards.txt", "w") as text_file:
      text_file.write("Output for for today...\n")

    response_series = requests.get(f'{sonarr_url}:{sonarr_port}/api/series?apikey={sonarr_apikey}')
    json_series = json.loads(response_series.text)

    for element in json_series:
        series_id = element['id']
        series_name = element['title']
        series_path = element['path']

        # For now, limit the number of files processed - remove this in the future #
        if z < 100:
        ##

            if ASSET_FILTER and asset_exists(series_path):
                pass
            else:
                process_season(series_id, series_name)
            z = z+1

    print("DONE! " + str(z) + " Shows scanned!")

    if z > 0:
        print("Check your output.txt file for details")

if __name__ == "__main__":
    main()