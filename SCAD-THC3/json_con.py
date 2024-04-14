import json
def strrepo(data_array,repo_path):
    print("Writing to", repo_path)
    repo_name = repo_path.split("/")[-1] if repo_path.split("/")[-1] != "" else repo_path.split("/")[-2]
    f = open(repo_path + "/" + repo_name + "_stats.json", "w")
    json.dump(data_array, f)
    f.close()

def store_population_data(data, repo_path):

    #[{filename, z-score},]

    repo_name = repo_path.split("/")[-1]
    print("Writing population data to", repo_path)
    f = open(repo_path + "/" + repo_name+"_population.json", "w")
    json.dump(data, f)
    f.close()
