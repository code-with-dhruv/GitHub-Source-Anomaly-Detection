
from git_automation import automate
from ascii_miner import repo_wise, population_repo_wise, html_repo_wise
import os, webbrowser

#github automation
gitfile = input("Enter the path of the text file containing github repo links: ")
if gitfile:
    automate(gitfile)
else:
    automate()

#repos basic data distribution computation
repo_path = input("\nEnter the directory containing repos: ")
if not(repo_path):
    repo_path = "./repos"
repo_wise(repo_path)
print("\Estimating Population parameters using CLT...\n")
population_repo_wise(repo_path)
print("\nGenerating HTML files...")
html_repo_wise(repo_path)

repos = os.listdir(repo_path)
print("\n\nRepo Numbers:")
for i in range(len(repos)):
    print(i, ".", repos[i])

while True:
    n = input("\nEnter a number to view its html report: ")
    if n == "exit" or n == "quit":
        break
    try:
        n = int(n) #negative easter-egg
        webbrowser.open(os.path.abspath(repo_path + "/" + repos[n] + "/file_wise.html"))
    except:
        print("Invalid value entered!")
