import numpy as np
from statistics import mean,pstdev,stdev
import os, json

def cal_file(file_loc, encoding="utf-8"):
    ex=file_loc.split(".")[-1]
    try:
        file = open(file_loc,"rt", encoding=encoding)
    except:
        #print("Open Error")
        return
    ascii_list=[]
    nrml_list=[]
    try:
        content = file.read()
    except:
        #print("Read Error")
        return
    for letter in content:
        ascii_list.append(ord(letter.encode(encoding).decode(encoding)))
    meann=mean(ascii_list) if len(ascii_list) else 0
    sd=pstdev(ascii_list) if len(ascii_list) else 0
    #print("ascii_list list : " ,ascii_list)
    #print("Mean : ",meann)
    #print("S.D : ", sd)
    for x in ascii_list:
        nrml = round((0.3989422804014327/sd) * np.exp(-0.5*((x-meann)/sd)**2), 6) if sd != 0 else 0
        nrml_list.append(nrml)
    #print(nrml_list)
    return {"file_loc":file_loc,"mean":meann,"sd":sd,"ascii_list":ascii_list,"nrml_list":nrml_list}

def get_population_param(path):
    #path: path to the repo
    repo_name = path.split("/")[-1]
    json_file = json.load(open(path + "/" + repo_name + "_stats.json"))
    means = [i["mean"] for i in json_file]
    return (mean(means), pstdev(means))

def get_per_file_z_score(path):

    print("Calculating z-scores of", path)
    repo_name = path.split("/")[-1]
    pop_mean, pop_std = get_population_param(path)
    json_file = json.load(open(path + "/" + repo_name + "_stats.json"))
    z_scores = {"population_mean": pop_mean, "population_sd": pop_std,
                "files":[{"file_loc": i["file_loc"], "z": (abs((i["mean"] - pop_mean) / pop_std) if pop_std != 0 else 1000) } for i in json_file]}
    return z_scores

def lp(p1, p2, t):
    return int(p1 + (p2 - p1)*t)

def lpc(c1, c2, t):
    a = lp(c1[0], c2[0], t)
    b = lp(c1[1], c2[1], t)
    return (a, b, 0)

def interpolate(z):
    if z < 0.1:
        return (lambda x: "#%02x%02x%02x" % x)((0, 255, 0))
    elif z > 1.5:
        return (lambda x: "#%02x%02x%02x" % x)((255, 0, 0))
    else:
        return (lambda x: "#%02x%02x%02x" % x)(lpc((0, 255, 0), (255, 0, 0), z/1.5))

def generate_html(path):

    repo_name = path.split("/")[-1]
    pop_data = json.load(open(path + "/" + repo_name + "_population.json"))
    values = [(i["file_loc"], i["z"]) for i in pop_data["files"]]

    html_string = """
    <!DOCTYPE html><html>
    <style>
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
<body style="text-align:center;">
"""
    html_string += "<h1>Anomaly Report of " + repo_name + "</h1>"
    html_string += "<h2>Scale (Anomaly Score): Higher the score higher the anomaly of the file object"
    for z in range(0, 15):
        html_string += "<h2 style='padding-right: 30px; display: inline-block; background-color:" + interpolate(0.1 * z) + "'>   " + str(round(0.1 * z, 2)) + "   "
    html_string += "<h2 style='padding-right: 30px; display: inline-block; background-color:" + interpolate(1.6) + "'>   > 1.5   </h2><hr>"
    for filepath, z in values:
        html_string += "<pre><div class=\"tooltip\"><h2 style='background-color:" + interpolate(z) + "'>" + filepath + "</h2></pre><span class='tooltiptext'>Anamoly Score: "+ str(round(z, 5)) + "</span></div><hr>\n"
    
    f = open(path + "/" + "file_wise.html", "w")
    f.write(html_string)
    f.close()

if __name__ == "__main__":
    path = "C:/Users/91889/AppData/Local/Programs/Python/Python39"
    for i in os.listdir(path):
        c = cal_file(path + "/" + i)
        print(c["file_loc"] if c is not None else i + " is binary")
