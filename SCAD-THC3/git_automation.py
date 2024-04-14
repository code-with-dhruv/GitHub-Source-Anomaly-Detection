
import os
from git import Repo

def store_record(url):
    f = open("../storedrecords.txt", "a")
    f.write(url+"\n")
    f.close()

def load_records():
    try:
        f = open("storedrecords.txt") 
        return [i.replace("\n", "") for i in f.readlines() if i != "" and i.split("/")[-1] in os.listdir("./repos")]
    except:
        return []

def automate(fname="github_table.txt"):
    f = open(fname)
    links = f.read().split("\n")
    pre_records = load_records()
    if "repos" not in os.listdir():
        os.mkdir("repos")
    os.chdir("./repos")
    for i in links:
        if i in pre_records: continue
        print("\nCloning", i)
        try:
            Repo.clone_from(i, i.split("/")[-1])
            store_record(i)
        except:
            print("Failed to clone", i)
    os.chdir("../")
    print("Done")