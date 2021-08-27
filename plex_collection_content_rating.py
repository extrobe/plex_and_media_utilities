from plexapi.server import PlexServer
#import datetime

baseurl = 'http://192.168.1.208:32400'
token = ' '
ratings_rank = {"gb/E":00 ,"gb/Uc": 10, "gb/U": 20, "gb/PGc": 30, "gb/PG": 40, "gb/12A":50,"gb/12": 60,"gb/15": 70,"gb/18": 80}

plex = PlexServer(baseurl,token)

collection_list = []


def update_collection_ratings():
    """tbc"""
    library = plex.library.section('Films')

    #Loop through each collection
    for collection in library.search(libtype='collection'):
        print()
        print("COLLECTION: " + collection.title + ": " + str(collection.contentRating))
        
        #Loop through each item in the collection
        for video in library.search(collection=collection.title):
            print("    FILM: " + video.title + ": " + str(video.contentRating) + " [rank:" + str(ratings_rank.get(video.contentRating,999)) +"]" )
            collection_list.append(ratings_rank.get(video.contentRating,999))
        
        #As long as >0 valid ratings were found, find the lowest from the collection
        if len(collection_list) > 0 :
            print("MIN RANK: " + str(min(collection_list)))
            
            for rating,rank in ratings_rank.items():
                if rank == min(collection_list):
                    target_rating_for_collection = rating

            #Apply this to the collection
            if collection.contentRating != target_rating_for_collection:
                
                print("READY TO UPDATE " + collection.title + " from " + collection.contentRating + " to " + target_rating_for_collection)

                collection.edit(**{
                "contentRating.value": target_rating_for_collection,
                "contentRating.locked": 1,
                })

                print("UPDATED")

            else:
                print("NO UPDATE NECESSARY")

        collection_list.clear()

def main():
    """Kick off the primary process."""

    update_collection_ratings()

if __name__ == "__main__":
    main()