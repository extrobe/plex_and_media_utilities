from plexapi.server import PlexServer

baseurl = 'http://192.168.1.208:32400'
token = ''
ratings_rank = {
    "gb/E"   : 00,
    "gb/Uc"  : 10,
    "gb/U"   : 20,
    "gb/PGc" : 30,
    "gb/PG"  : 40,
    "gb/12A" : 50,
    "gb/12"  : 60,
    "gb/15"  : 70,
    "gb/18"  : 80
    }

DRY_RUN = True
LIMIT = None # Set to None to scan all collections

plex = PlexServer(baseurl,token)
collection_list = []
update_list = []

def update_collection_ratings():
    """Scan and update collections"""
    library = plex.library.section('Films')

    #Loop through each collection
    for collection in library.search(libtype='collection',limit=LIMIT):
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

                if not DRY_RUN:
                    collection.edit(**{
                    "contentRating.value": target_rating_for_collection,
                    "contentRating.locked": 1,
                    })

                    print("UPDATED")
                else:
                    print("DRY RUN - NO CHANGES MADE")
                
                update_list.append(collection.title)

            else:
                print("NO UPDATE NECESSARY")

        collection_list.clear()
    
    # Print out summary of what changed / would have been changed
    print()
    if not DRY_RUN:
        print('COLLECTIONS UPDATED:')
    else:
        print('COLLECTIONS TO BE UPDATED')
    for item in update_list:
        print(item)
    print()

def main():
    """Kick off the primary process."""

    update_collection_ratings()

if __name__ == "__main__":
    main()