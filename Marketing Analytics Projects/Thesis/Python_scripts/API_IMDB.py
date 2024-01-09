# importing video titles
from webscraper_flixpatrol import titles
titles

#loading IMDBpy API
import csv
from imdb import IMDb
from imdb import IMDb, IMDbError
ia = IMDb(accessSystem='http', reraiseExceptions=True)

#retrieve all the needed information
def get_video_information(name):
    info = []
    i = 0
    for item in titles:
        try:
            genres_list = ""
            MPAA_list = ""
            search = ia.search_movie(item)
            movie_name = item
            id = search[0].movieID
            movie = ia.get_movie(id)
            movie_2 = ia.get_movie(id, info='parents_guide')
            #Video rating
            try:
                rating = movie["rating"]
            except:
                print("no rating")
            #MPAA rating
            try:
                for item in movie_2["certification"]:
                    if item["country_code"] == "US":
                        MPAA_list += item["certificate"] + ","
            except:
                print("no certification")
            #genres
            try:
                for item in movie["genre"]:
                    genres_list += item + ","   
            except:
                print("no genres")
            #appending everything to a list
            info.append({"name": movie_name,
                       "genre": genres_list,
                       "MPAA_rating": MPAA_list,
                       "rating": rating})
            # to follow progress and find moment of error, count every collected row so far
            i += 1
            print(i)
        # to ignore error and keep collecting, only print error
        except IMDbError as e:
            print(e)    
    return info

#applying the above created funtion to all the titles
video_information = get_video_information(titles)

#writing to a csv file 
with open("video_information4.csv", "w", encoding = 'utf-8', newline='') as csv_file: 
    writer = csv.writer(csv_file, delimiter = ";")
    writer.writerow(["name", "genre", "MPAA_rating", "rating"])
    for info in video_information: 
        writer.writerow([info['name'], info['genre'], info['MPAA_rating'], info["rating"]])
print('done!')

