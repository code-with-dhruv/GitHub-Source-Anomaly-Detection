
import os
import threading as t

from hack import cal_file, get_per_file_z_score, generate_html
from json_con import strrepo, store_population_data

#cal_file = None #D cal_file(fpath)
#strrepo = None #d strrepo(data_array, repo_path)


def traverse_and_get_files(path, data=[], func=cal_file):

    #path: path to repo folder

    folders = []
    for i in os.listdir(path):
        if os.path.isfile(path + "/"+ i):
            data.append(func(path + "/" + i))
        else:
            folders.append(i)
    for i in folders:
        traverse_and_get_files(path + "/" + i, data)

def repo_wise(container_path):
    for repo in os.listdir(container_path):
        print("Started calculating for repo", repo)
        ret = clean_repo(container_path + "/" + repo) #clean
        if ret: 
            print("Continuing...")
            continue
        data = []
        traverse_and_get_files(container_path + "/" + repo, data)
        strrepo([i for i in data if i is not None], container_path + "/" + repo)
    
def clean_repo(path):
    if path.split("/")[-1]+"_stats.json" in os.listdir(path):
        print("skipping stats.json from", path)
        #os.remove(path + "/stats.json")
        return True
    return False

def clean_pop(path):
    if path.split("/")[-1] + "_population.json" in os.listdir(path):
        print("Skipping population calculation as it already exists")
        return True
    return False

def population_repo_wise(container_path):
    for repo in os.listdir(container_path):
        print("Starting Population data for", repo)
        ret = clean_pop(container_path + "/" + repo)
        if ret:
            continue
        data = get_per_file_z_score(container_path + "/" + repo)
        store_population_data(data, container_path + "/" + repo)

def html_repo_wise(container_path):
    for repo in os.listdir(container_path):
        print("Generating for:", repo)
        generate_html(container_path + "/" + repo)