import requests
import praw
import json
import re

sonarr_apikey = 'xxx' ## Add your Sonarr API Key
sonarr_url = 'http://192.168.1.208' ## Add your Sonarr URL
sonarr_port = 8989 ## Add your Sonarr Port (Default 8989)

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

        if author not in EXCLUDE_AUTH:

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
                    #text_file.write(str(is_fullpack(submission.title))+"\n")
                
                y = y+1

    if y == 0:
        print("no results found")
    
    print("")

def is_fullpack(submission_name):
    """Audits the submission name to detirmine if it's a single episode or a full pack"""
    return not bool(re.search('(s\d{1,4}e\d{1,4})+',str.lower(submission_name)))

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

        # For now, limit the number of files processed - remove this in the future #
        if z < 50:
        ##

            process_season(series_id, series_name)
            z = z+1

    print("DONE! " + str(z) + " Shows scanned!")

    if z > 0:
        print("Check your output.txt file for details")

if __name__ == "__main__":
    main()