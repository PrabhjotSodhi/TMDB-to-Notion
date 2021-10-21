import requests, json # written by idiots for idiots

token = 'secret_l7tSLCs7mRtv31z2RuG1bU3W62qZc80bmILqLtk3M60'
database_id = "973f2aa45f9b4b5fb7b475526c673132"
headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2021-08-16"
}

def read_databases():
    #token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YTg3MDFkMzcyYmMzNGFmZWZlMjUxNjJhNGI3MWNmZiIsInN1YiI6IjYxNmU4Y2E3YmYzMWYyMDA0M2U0YzNhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FPtoY9oIg9Q6VVNBTyxQAbw9ulhEtK_f6nkgO8dyI-c"
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    #start_cursor = {"start_cursor":"692c743f-67af-4518-bbf8-de0bc3a56a14"}
    res = requests.request("POST", url, headers=headers)
    results = res.json()["results"]
    dramas = {}
    for result in results:
        if result["properties"]["Type"]["select"]["name"] == 'Movie':
            #dramas[result["properties"]["Drama Title"]["title"][0]["plain_text"]] = (result["id"], None)
            pass
        elif result["properties"]["Type"]["select"]["name"] == 'Drama':
            dramas[result["properties"]["Drama Title"]["title"][0]["plain_text"]] = (result["id"], None)
        else:
            pass
            
    #drama_posters = {}
    for drama_name in dramas.keys():
        drama_url = f"https://api.themoviedb.org/3/search/tv?api_key=4a8701d372bc34afefe25162a4b71cff&query={drama_name}"
        drama_res = requests.request("GET", drama_url)
        results = drama_res.json()['results']
        if results and results[0]['genre_ids']:
            dramas[drama_name] = (dramas[drama_name][0], results[0]['genre_ids'])
    
    final_drama_list = []
    for drama_name, drama in dramas.items():
        # filter out dramas without posters
        if drama[1] != None:
            final_drama_list.append((drama_name, drama[0], drama[1]))

    return final_drama_list

def update_pagecover(drama_names):
    #testing if one cover updates
    for drama in drama_names:
        url = f"https://api.notion.com/v1/pages/{drama[1]}"
        cover_json = {"properties":{"Genres":{"multi_select":[{"name":f"{}"}]}}}
        updated_response = requests.patch(url, headers=headers, json=cover_json)
    print(updated_response)

drama_names = read_databases()
update_pagecover(drama_names)