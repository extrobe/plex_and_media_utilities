from plexapi.server import PlexServer
import datetime

baseurl = 'http://192.168.1.208:32400'
token = ' '

plex = PlexServer(baseurl,token)

def generate_yml_films():
    """Gernate yaml file for films"""
    movies = plex.library.section('Films')
    for video in movies.all():
        if len(video.fields) == 1 and video.fields[0].name == 'thumb':
            pass # if the only custom content is the img, then skip - at least until I know a way to extract the image and save to assets folder
        elif len(video.fields) > 0:
            with open("films.yml", "a") as text_file:
                text_file.write(' '*4 + '"' + video.title + '":\n')
                text_file.write(' '*8 + 'title: "' + video.title + '"\n')
                text_file.write(' '*8 + 'year: ' + str(video.year) + '\n')

            for field in video.fields:
                if field.name == 'genre':
                    with open("films.yml", "a") as text_file:
                        text_file.write(' '*8 + field.name + ": ")    
                        genrelist = [genre.tag for genre in video.genres]
                        text_file.write(",".join(genrelist))
                        text_file.write('\n')  

                elif field.name == 'collection':
                    with open("films.yml", "a") as text_file:
                        text_file.write(' '*8 + field.name + ": ")    
                        collectionlist = [collection.tag for collection in video.collections]
                        text_file.write(",".join(collectionlist))
                        text_file.write('\n')  
                
                elif field.name == 'country':
                    with open("films.yml", "a") as text_file:
                        text_file.write(' '*8 + field.name + ": ")    
                        countrylist = [country.tag for country in video.countries]
                        text_file.write(",".join(countrylist))
                        text_file.write('\n')  
                
                elif field.name == 'label':
                    with open("films.yml", "a") as text_file:
                        text_file.write(' '*8 + field.name + ": ")    
                        labellist = [label.tag for label in video.labels]
                        text_file.write(",".join(labellist))
                        text_file.write('\n') 

                elif field.name == 'originallyAvailableAt':
                     with open("films.yml", "a") as text_file:
                         text_file.write(' '*8 + field.name + ": ")
                         tm = getattr(video,field.name)
                         text_file.write(tm.strftime('%d/%m/%Y') + '\n')
                elif field.name == 'thumb':
                    pass # I don't think this has a use in PMM, as it needs a locally stored file
                elif field.name == 'title':
                    pass # we already include the title
                elif field.name == 'year':
                    pass # we already include the year
                else:
                    with open("films.yml", "a") as text_file:
                        text_file.write(' '*8 + field.name + ": ")
                        text_file.write(getattr(video,field.name) + "\n")

def main():
    """Kick off the primary process."""

    with open("films.yml", "w") as text_file:
      text_file.write("metadata:\n")

    generate_yml_films()

if __name__ == "__main__":
    main()