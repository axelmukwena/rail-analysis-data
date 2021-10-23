import pandas as pd
from tqdm import tqdm
import json
import random


def re(value):
    if pd.isna(value):
        return 'Unknown'
    else:
        return value


bitcoin = pd.read_csv('data/bitcoinotc.csv')  # way too many rows
# github = pd.read_csv('github_repos.csv')  # around 16000 rows
accidents = pd.read_csv('data/accidents/causes-of-accidents-by-severity-of-injury-sustained.csv')  # around 16000 rows

size = 5000  # len(bitcoin)  # len(github.index)
source = bitcoin.iloc[:, 0][:size]
target = bitcoin.iloc[:, 1][:size]
weight = bitcoin.iloc[:, 2][:size]
# name = github.iloc[:, 1][:size]
# message = github.iloc[:, 2][:size]
# repo_name = github.iloc[:, 3][:size]

accident_classification = accidents.iloc[:, 1][:size]
road_user_group = accidents.iloc[:, 2][:size]
causes_of_accident = accidents.iloc[:, 3][:size]
number_of_accidents = accidents.iloc[:, 4][:size]

trim = 0
data = []
processed = set()
for i in tqdm(range(size)):
    s = source[i]
    if s not in processed:
        targets = []
        weights = []
        for j in range(size):
            processed.add(s)
            if source[j] == s:
                targets.append(int(target[j]))
                weights.append(int(weight[j]))

        if len(targets) > 50 or len(targets) < 2:
            processed.remove(s)
            continue

        # So far only 4369 values exist
        # if trim == 5000:
        #    break
        # trim += 1
        rand = random.randint(0, len(accidents) - 1)
        data.append([int(s), targets, weights, re(accident_classification[rand]), re(road_user_group[rand]),
                     re(causes_of_accident[rand]), int(re(number_of_accidents[rand])), len(targets)])

with open("processed/graph_data_accidents_5000.json", "w") as f:
    json.dump(data, f)

print(trim)
