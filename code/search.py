import sys
import pickle

indexed_file = "../data/indexed.pickle"
movie_indexed_file = "../data/movie_indexes.pickle"




def check_if_and_exists(movie_indexed, movie_index_dict, search):
    
    movie_set = set()

    #print ("this is and case!")
    search_terms_list = search.split()
    new_search_term_list = list()
    for s in search_terms_list:
        new_search_term_list.append(s.strip())

   
    #print ("searching for", new_search_term_list)

    for search_term in new_search_term_list:
        #print ("searching for ", search_term)
        movies_returned = return_movies_search(movie_indexed, movie_index_dict, search_term)
        #print ("searched for ", search_term, " and movies returned is ", movies_returned)
        if not movies_returned:
            return []
        else:
            #print ("movies set is ", movie_set)
            if len(movie_set) == 0:
                movie_set = set(movies_returned)
 
            else:
                movie_set =  movie_set.intersection(set(movies_returned))
                if len(movie_set) == 0:
                    return []

        #print ("after searching for", search_term, "movie set is ", movie_set)
        
    return list(movie_set)


def check_if_or_exists(movie_indexed, movie_index_dict, search):
    movie_set = set()

    #print ("this is or case!")
    search_terms_list = search.split()
    new_search_term_list = list()
    for s in search_terms_list:
        new_search_term_list.append(s.strip())

   
    print ("searching for", new_search_term_list)

    for search_term in new_search_term_list:
        print ("searching for smaller term", search_term)
        movies_returned = return_movies_search(movie_indexed, movie_index_dict, search_term)
        print ("searched for ", search_term, " and movies returned is ", movies_returned)
        movie_set.update(movies_returned)

        
    return movie_set


def regex_search(movie_indexed, movie_index_dict, search):
    movies_returned_indexes = set()
    movies_returned_names = set()
    for key in movie_indexed:
        if search in key:
            movies_returned_indexes.update(movie_indexed[key]) 


    
    movies_returned_list = [movie_index_dict[k] for k in movies_returned_indexes]
    return movies_returned_list   


def return_movies_search(movie_indexed, movie_index_dict, search_term):
    movies_returned = set()
    if search_term in movie_indexed:
        t =  [k for k in movie_indexed[search_term]]
        #print ("-- Indexes", t)

        movies_returned_list =  [movie_index_dict[k] for k in movie_indexed[search_term]]
        #print ("--- Movies", t)
        movies_returned.update(movies_returned_list)


    else:
        movies_returned_list = regex_search(movie_indexed, movie_index_dict, search_term)
        
    return list(movies_returned_list)
        
    




def get_search_terms_list(search_terms):
    search_terms_list = search_terms.trim().split("\\s+")
    search_term_l = list()
    for search in search_terms_list:
        search_term_l.append(search.lower())


    return search_term_l


if __name__ == "__main__":
    search_terms = sys.argv[1]
    
    file = open(indexed_file,'rb')
    movie_indexed = pickle.load(file)
    file.close()
    
    file = open(movie_indexed_file,'rb')
    movie_index_dict = pickle.load(file)
    file.close()
    
    #print movie_indexed
    
    
    #get_search_terms_list(search_terms)
    
    
    user_search = search_terms.lower()
    
    
    if user_search not in movie_indexed:
        movies_returned = check_if_and_exists(movie_indexed, movie_index_dict, user_search)
        if len(movies_returned) > 0:
            print (movies_returned)
        else:
            l = list()
            print (l)
            #print ("No Movie Found! :(")
        
        #if not movies_returned:
        #    print "No movie found"
    
        #else:
        #   print movies_returned
    else:
        print (return_movies_search(movie_indexed, movie_index_dict, user_search))
        
    
    
