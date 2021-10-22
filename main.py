import requests, os # written by idiots for idiots in idiot language - tounge twister
# we need to ditch python and learn JS
token = 'secret_l7tSLCs7mRtv31z2RuG1bU3W62qZc80bmILqLtk3M60'
database_id = os.environ['database_id']
headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2021-08-16"
}

def read_databases():
    #token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YTg3MDFkMzcyYmMzNGFmZWZlMjUxNjJhNGI3MWNmZiIsInN1YiI6IjYxNmU4Y2E3YmYzMWYyMDA0M2U0YzNhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FPtoY9oIg9Q6VVNBTyxQAbw9ulhEtK_f6nkgO8dyI-c"
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    #start_cursor = "692c743f-67af-4518-bbf8-de0bc3a56a14"
    #json_cursor = {"start_cursor":f"{start_cursor}"}
    res = requests.request("POST", url, headers=headers)
    results = res.json()["results"]
    dramas = {}
    movie_list = []
    for result in results:
        if result["properties"]["Type"]["select"]["name"] == 'Movie':
            movie_list.append(result["properties"]["Drama Title"]["title"][0]["plain_text"])
        elif result["properties"]["Type"]["select"]["name"] == 'Drama':
            dramas[result["properties"]["Drama Title"]["title"][0]["plain_text"]] = (result["id"], None, None)
        else:
            pass
    
    # This is how I toggle on what I would like to do
    fetch_posters(dramas)
    fetch_genres(dramas)

    
    final_drama_list = []
    for drama_name, drama in dramas.items():
        # if the drama has a genre OR a poster, keep data
        # this is because any results w/o this information are useless to us
        if drama[1] != None or drama[2] != None:
            final_drama_list.append((drama_name, drama[0], drama[1], drama[2]))

    return final_drama_list

def fetch_posters(dramas):
    for drama_name in dramas.keys():
        drama_url = f"https://api.themoviedb.org/3/search/tv?api_key=4a8701d372bc34afefe25162a4b71cff&language=ko&query={drama_name}"
        drama_res = requests.request("GET", drama_url)
        results = drama_res.json()['results']
        if results and results[0]['poster_path']:
            dramas[drama_name] = (dramas[drama_name][0], results[0]['poster_path'], dramas[drama_name][2])

# Change_genre and change_poster only one can be called at a time thats because I want it that way

def fetch_genres(dramas):
    # I have setup the genres they output a list of numbers which corelate to a genre which I have put in a dict below
    genre_options = {
        35:"Comedy",
        18:"Drama",
        9648:"Mystery",
        10751:"Family",
        80:"Crime",
        10759:"Action & Adventure",
        10765:"Sci-Fi & Fantasy",
        10749:"Romance",
        10768:"War & Politics",
        10762:"Kids",
        None: None
    }
    for drama_name in dramas.keys():  # so slow
        drama_url = f"https://api.themoviedb.org/3/search/tv?api_key=4a8701d372bc34afefe25162a4b71cff&language=ko&query={drama_name}"
        drama_res = requests.request("GET", drama_url)
        
        results = drama_res.json()['results'] #ohh ok
        if results and results[0]['genre_ids']: # 
            genres = [genre_options.get(i) for i in results[0]['genre_ids'] if i is not None]
            dramas[drama_name] = (dramas[drama_name][0], dramas[drama_name][1], genres)

def update_pagecover(dramas):
    #testing if one cover updates
    for drama in dramas:
        url = f"https://api.notion.com/v1/pages/{drama[1]}"
        cover_json = {"cover":{"type":"external","external":{"url":f"https://image.tmdb.org/t/p/original/{drama[2]}"}}}
        updated_response = requests.patch(url, headers=headers, json=cover_json)
    print(updated_response)
def update_pagegenre(dramas):
    for drama in dramas:
        if drama[3]:
            url = f"https://api.notion.com/v1/pages/{drama[1]}"
            genre_json = {"properties":{"Genres":{"multi_select":[{"name": g} for g in drama[3]]}}}
            updated_response = requests.patch(url, headers=headers, json=genre_json)
    print(updated_response)

dramas = read_databases()
#print("updating pagecover...")
#update_pagecover(dramas)
print("updating pagegenre")
update_pagegenre(dramas)