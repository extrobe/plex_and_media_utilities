import requests
import praw
import json
import re
import os
import glob

sonarr_apikey = 'abc' ## Add your Sonarr API Key
sonarr_url = 'http://192.168.1.8' ## Add your Sonarr URL
sonarr_port = 8989 ## Add your Sonarr Port (Default 8989)

limit = 0 # set to 0 for no limit

####################################################################################
# Root path for your assets. Allows us to check if there are already any assets    #
####################################################################################
ASSET_ROOT = '/Volumes/Plex Thumbs/PlexMetaManager/assets/tv'
ASSET_FILTER = True

####################################################################################
# Settings for scanning for missing episode files                                  #
####################################################################################
SCAN_FOR_MISSING = True # Scan for missing episode files when some assets exist
INCLUDE_SPECIALS = False # When scanning for missing episode files, include Specials/Season 00
PRINT_SOURCE = True # if you have a source.txt file, print for output for faster checking

####################################################################################
# Create a comma separate list of users you want to exclude from the results       #
####################################################################################
EXCLUDE_AUTH = ["extrobe"]

####################################################################################
# When set to True, ignores any submissions that appear to be for a single episode #
####################################################################################
FULL_PACK_ONLY = True


def process_season(series_id, series_name):

    print("scanning r/PlexTitleCards... for " + series_name)

    write_title = False
    y = 0

    reddit = praw.Reddit(
    client_id="abc", ## Add your Reddit Client ID
    client_secret="abc", ## Add your Reddit Secret
    redirect_uri="http://localhost:8080",
    user_agent="Plex Title Card Matcher",
    )

    reddit.read_only = True


    for submission in reddit.subreddit("PlexTitleCards").search(series_name, limit=None):

        author = submission.author.name
        flair = submission.link_flair_text
        if flair is not None and bool(re.search('request|discussion',str.lower(''.join(map(str, flair))))):
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

def missing_episode_assets(series_id, series_name, series_path):
    """compare assets with expected episdoes"""

    print("Local assets found... for " + series_name)
    print("scanning for missing files...")
    #print(series_id)

    validation_path = ASSET_ROOT + series_path[series_path.rfind('/'):]
    print("scanning path... " + validation_path)

    response_episode = requests.get(f'{sonarr_url}:{sonarr_port}/api/episode?seriesID={series_id}&apikey={sonarr_apikey}')
    json_episodes = json.loads(response_episode.text)

    e = 0

    for element in json_episodes:
        season = element['seasonNumber']
        episode = element['episodeNumber']
        hasfile = element['hasFile']

        if season > 0 and hasfile:
            search_string = 'S' + str(season).zfill(2) + 'E' + str(episode).zfill(2)

            f = glob.glob(validation_path+'/'+search_string+'.*')

            if len(f) == 0:
                asset_missing = True
            else:
                for g in f:
                    if g.lower().endswith(('.png', '.jpg', '.jpeg')):
                        asset_missing = False

            if asset_missing:

                with open("Output_Plex_TitleCards_Missing.txt", "a") as text_file:

                    if e == 0:
                        text_file.write("\n" + '### Missing Files For: ' + series_name + ' ###' + "\n")

                        if PRINT_SOURCE:
                            text_file.write("\n" + get_source_txt(validation_path) + "\n")
                            #get_source_txt(validation_path)

                        e=1

                    text_file.write('S' + str(season).zfill(2) + 'E' + str(episode).zfill(2))
                    text_file.write(" is missing" + "\n")

    print('')

def get_source_txt(validation_path):
    """get contents of a text file to append to assets_missing test file"""

    source_string = validation_path + '/source.txt'
    if bool(os.path.isfile(source_string)):
        with open(source_string,'r') as f:
            src = f.read()

        return src
        #with open("Output_Plex_TitleCards_Missing.txt", "a") as text_file:
            #text_file.write(src + "\n")


def main():
    """Kick off the primary process."""
    print("STARTED!")

    z = 0

    with open("Output_Plex_TitleCards.txt", "w") as text_file:
      text_file.write("Output for for today...\n")

    if SCAN_FOR_MISSING:
        with open("Output_Plex_TitleCards_Missing.txt", "w") as text_file:
            text_file.write("Output for for today...\n")

    response_series = requests.get(f'{sonarr_url}:{sonarr_port}/api/series?apikey={sonarr_apikey}')
    json_series = json.loads(response_series.text)

    for element in json_series:
        series_id = element['id']
        series_name = element['title']
        series_path = element['path']

        # For now, limit the number of files processed - remove this in the future #
        if limit == 0 or (limit > 0 and z < limit):
        ##

            if ASSET_FILTER and asset_exists(series_path):
                missing_episode_assets(series_id, series_name, series_path)
            else:
                process_season(series_id, series_name)
            z = z+1

    print("DONE! " + str(z) + " Shows scanned!")

    if z > 0:
        print("Check your Output_Plex_TitleCards.txt file for details")
    
    if SCAN_FOR_MISSING:
        print("Check your Output_Plex_TitleCards_Missing.txt file for details of missing files")

if __name__ == "__main__":
    main()