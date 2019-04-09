import pickle


movie_database_file = "../data/fifty_movies.pickle"
movie_index_file = "../data/movie_indexes.pickle"

final_indexed_file = "../data/indexed.pickle"

index_dict = dict()

def read_data(movie_database_file, movie_index_file):
    file = open(movie_database_file,'rb')
    all_movies_dict = pickle.load(file)
    file.close()
    

    #print (all_movies_dict)
    file = open(movie_index_file ,'rb')
    movie_index_dict = pickle.load(file)
    file.close()
 
    return all_movies_dict, movie_index_dict   


def store_index_dictionary(index_dict):
   with open(final_indexed_file, 'wb') as handle:
        pickle.dump(index_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def add( entity, movie_index):
    global index_dict

    if entity not in index_dict:
        index_dict[entity] = set()
        index_dict[entity].add(movie_index)
    else:
        index_dict[entity].add(movie_index)
    

def index_entity(entity, movie_index):
    global index_dict

    original_entity = entity.lower()

    #print ("entity is ", original_entity)
    add(original_entity, movie_index)
    entity_list = original_entity.split()
    

    for entity in entity_list:
        #print ("Doing for entity", entity)
        add( entity, movie_index)


def index_movies(all_movies_dict, movie_index_dict):
    global index_dict

    for movie_index in all_movies_dict:
        movie_name = movie_index_dict[movie_index]
        index_entity(movie_index_dict[movie_index], movie_index )
         

def index_entities(all_movies_dict, movie_index_dict):
    global index_dict

    things_to_index = ['actor', 'creator', 'director', 'genre']

    for thing_to_index in things_to_index:
        for movie_index in all_movies_dict:
            movie_name = movie_index_dict[movie_index]
            #print ("111111   movie is ", movie_name, "movie index is ", movie_index)
            thing_to_index_list = all_movies_dict[movie_index][thing_to_index]
            #print ("INDEXING---", thing_to_index_list, "for movie index", movie_index)
            if isinstance(thing_to_index_list, (list, )):
                for thing in thing_to_index_list:
                    index_entity(thing, movie_index)
                    #thing = thing.lower()
                    #if thing not in index_dict:
                    #    index_dict[thing] = list()
                    #    index_dict[thing].append(movie_index)
                    #else:
                    #    index_dict[thing].append(movie_index)
            else:
                index_entity(thing_to_index_list, movie_index)
            
                #if thing not in index_dict:
                #    index_dict[thing] = list()
                #    index_dict[thing].append(movie_index)
                #else:
                #    index_dict[thing].append(movie_index)



if __name__ == "__main__":


    file = open(movie_database_file,'rb')
    all_movies_dict = pickle.load(file)
    file.close()
    
    
    
    
    
    #print ("all_movies_dict", all_movies_dict)
    
    
    file = open(movie_index_file,'rb')
    movie_index_dict = pickle.load(file)
    file.close()
    
    #print ("movie_index_dict", movie_index_dict)
    
    
    index_entities(all_movies_dict, movie_index_dict)
    index_movies(all_movies_dict, movie_index_dict)
    
    
    #print ("xxxxxxxxxxxxxxxxxxxx\n\n\n")
    #print (index_dict)
    
    #print ("\n\n\n", index_dict['drama'])
    
    
    store_index_dictionary(index_dict)
    
    
    #print (index_dict)
