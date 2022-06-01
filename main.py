from PIL import Image as im
import numpy as np
import itertools
import csv
import pickle
import math

# Choose the number of houses here :
# ----------------------
houses = 1
# ----------------------

if houses not in range(1, 12):
    raise ValueError(f"{houses} is not a valid number of houses.")

nwmap = im.open("Finished_map.png")  # B/W map with the pink dots.
# The map seen above has a single pink pixel on each spot where there's a city. The exact color of that pixel is of the form (255,x,255), where x is the city's index seen below.
s = nwmap.size
pix = np.array(nwmap)  # Transferring it to an array so I can see each pixel individually
table = csv.writer(open(f"results_{houses}_houses.csv", 'w', newline=''))
details = [f"Town {i + 1}" for i in range(houses)] + ["Maximum", "Average", "Standard deviation"]
table.writerow(details)
names = {
    0:"Mourningdale",
    1:"Brightwood",
    2:"Weaver's Fen",
    3:"Ebonscale",
    4:"Restless Shore",
    5:"Everfall",
    6:"Monarch's Bluffs",
    7:"Reekwater",
    8:"Windsward",
    9:"Cutlass Keys",
    10:"First Light"
}

# Opening the file for the cities' locations :
try:
    # Checking if the cities mapping has already been done.
    file = open("Cities.picl", "rb")
    cities = pickle.load(file)
except:
    print("Cities file not found, creating...")
    cities = {}
    for y in range(s[0]):
        for x in range(s[1]):
            if pix[x][y][0] == 255 and pix[x][y][2] == 255 and pix[x][y][1] <= 10:
                cities[pix[x][y][1]] = (x, y)
    file = open("Cities.picl", "wb")
    pickle.dump(cities, file)

possibilities = np.array(list(itertools.combinations(range(11), houses)),dtype='O')  # Basically 11 choose (houses).
n = math.comb(11, houses)  # REALLY 11 choose (houses)
possibilities = np.append(possibilities, np.zeros((n, 3)), axis=1)
c = 0
for row in possibilities:
    print(f"Doing row : {row[0:houses]}")
    if c % (n // 10) == 0:
        print(f"{10 * c // (n // 10)}% finished !")
    coords = [cities[i] for i in row[0:houses]]  # Associated coordinates for each city.

    distances = np.ones((np.shape(pix)[0], np.shape(pix)[1]))

    # Computing the min distance.
    for y in range(s[0]):
        for x in range(s[1]):
            if pix[x][y][1] > 0:
                # Making sure we only do calculations on white pixels, which are walkable points.
                distances[x][y] = min([((x - c[0]) ** 2 + (y - c[1]) ** 2) ** (1 / 2) for c in coords])

    for i in range(houses):
        row[i] = names[row[i]]
    row[houses] = np.amax(distances)
    row[houses + 1] = np.mean(distances)
    row[houses + 2] = np.std(distances)
    c += 1

print("Done !")
print(f"Result saved in results_{houses}_houses.csv")
table.writerows(possibilities)
