from urllib import request
import json
import os
import os.path
import time
import importlib.resources

#cache_folder = os.getcwd().split('paises')[0] + 'paises/cache'
cache_folder = 'cache'
# 604800 is on week
max_age = 604800

def get_file_path(name):
    file_path = importlib.resources.path(__package__, "countries.json")
    return file_path
        
def check_age(name):
    if (os.path.getmtime(name) - time.time()) < - max_age:
        print("Updating " + str(name) + " from server.")
        retrieve_and_cache(name)

def check_cache(name):
    return (os.path.exists(name))

def write_cache(data, file_path):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()

def retrieve_and_cache(name):
    # Load country data from the worldbank
    # We fetch data from the World Bank
    url = "http://api.worldbank.org/v2/countries?format=json&per_page=304"
    response = request.urlopen(url)
    codec = response.info().get_param('charset', 'utf8')
    data = json.loads(response.read().decode(codec))

    f = get_file_path(name)
    write_cache(data, f)
    print("Files updated from server")

def load_cache(file_name):

    p = get_file_path(file_name)

    if check_cache("cache/" + p.name) == False:
        retrieve_and_cache(name=file_name)	
    else:
        check_age(file_name)    	
	    
    with open(p) as json_file:
        data = json.load(json_file)
        return (data)