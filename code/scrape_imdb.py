import requests
from bs4 import BeautifulSoup
import ast
import pickle

all_movies_dict = dict()
movie_indexes = dict()

movie_index_file = 'movie_indexes.pickle'
movie_data_dump_file = 'fifty_movies.pickle'


def store_movie_indexes(movie_indexes):
    with open(movie_index_file, 'wb') as handle:
        pickle.dump(movie_indexes, handle, protocol=pickle.HIGHEST_PROTOCOL)
   


def store_movies_dictionary(all_movies_dict):
    with open(movie_data_dump_file, 'wb') as handle:
        pickle.dump(all_movies_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)



def store_movie(movie_dict, count, english_title):
     #print "entered............"   

     #print ("count is ", count)
     #print ("movie name is ", movie_dict['name'].encode('utf8'))
     if english_title is None:
         movie_name = movie_dict['name']
     else:
         movie_name = english_title
 

     movie_indexes[count] = movie_name
     

     attributes = dict()
     
     
     if isinstance(movie_dict['director'], (list, )):
         attributes['director'] = list()
         for director in movie_dict['director']:
             attributes["director"].append(director['name'])
 
     else:
         attributes["director"] = movie_dict['director']['name']

     attributes['creator'] = list()
     for creator in movie_dict['creator']:
         #print "creator is ", creator
         #print "typeee is ", type(creator)
         if creator['@type'] == 'Person':
             #print "name is ", creator['name']
             name = creator['name']
             attributes["creator"].append(name)


     attributes['actor'] = list()
     for actor in movie_dict['actor']:
         name = actor['name']
         attributes["actor"].append(name)


     attributes["genre"] = movie_dict['genre']
     attributes["description"] = movie_dict['description']
     

     all_movies_dict[count] =  attributes

     #print "xxxxxxx", all_movies_dict
     #print "yyyyyyyyy", movie_indexes


def get_movie_original_name(soup):
    all_div = soup.find_all("div")
    contains_orig_title = False
    for div in all_div:
        if div.get('class') is not None and 'originalTitle' in div['class']:
           contains_orig_title = True
    
           return True 
    return False

def find_name(soup):
    all_div = soup.find_all("div")
    for div in all_div:
        if div.get('data-title') is not None:
           #print "title is ", div['data-title']
           return div['data-title']
    


def store_url(movie_url, count):
    r = requests.get(movie_url)

    c = r.content
    soup = BeautifulSoup(c, "lxml")
    #print "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    english_title = None
    orig_name_exists = get_movie_original_name(soup)
    if orig_name_exists:
        english_title = find_name(soup)
 
    all_scripts  = soup.find_all('script')
    for s in all_scripts:
        if s.get('type') is not None:
            if s['type'] == 'application/ld+json':
                x = s.get_text()
                movie_dict = ast.literal_eval(x)
                store_movie(movie_dict, count, english_title)
                #print movie_dict
    
   

if __name__ == "__main__":

    i = 1
    count = 0
    number_of_movies = 1000
    
    
    
    while i < number_of_movies:
        base_url = 'https://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple'
        if i == 1:
            r = requests.get(base_url)
        else:
            s = base_url + '&sort=user_rating,desc&start='+str(i) + '&ref_=adv_nxt'
            r = requests.get(s)
            
        c = r.content
    
        soup = BeautifulSoup(c, "lxml")
        li =  soup.find_all("a", href=True)
        for x in li:
            url  = x['href']
            if 'title/' in url and "adv_li_tt" in url:
                #print url
                movie_url = 'https://www.imdb.com/' + url
                store_url(movie_url, count)
                if count % 25 == 0:
                    print ("count is ", count)
                count+=1
    
    
    
    
        i = i + 50
    
    
    store_movies_dictionary(all_movies_dict)
    store_movie_indexes(movie_indexes)
    
    
    #print ("count is ", count)
    #print ("movie_indexes is ", movie_indexes)
