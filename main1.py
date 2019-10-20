import csv
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np

myList = []

# 2.1 Exercise
with open("gltDB.csv") as file:

    for row in csv.reader(file):
        if len(row) == 7:
            temp = []
            for el in row:
                temp.append(el)

            myList.append(temp)

myList.pop() # remove headers

# 2.2 Exercise
for i, el in enumerate(myList): # enumerate gives index
    # avgTemp missing
    if el[1] == '':

        k = 1 # initialize at every iteration

        if myList[i + 1][1] != '' and myList[i+1][3] == el[3] and myList[i - 1][1] != '' and myList[i-1][3] == el[3]:
            myList[i][1] = (float(myList[i + 1][1]) + float(myList[i - 1][1]))/2

        # particular case
        else:
            while myList[i][1] == '':
                if myList[i+k][1] != '':
                    myList[i][1] = float(myList[i + k][1]) / 2

                else: k = k+1

# 2.3 Exercise
def hottestAndColdest(n, city):

    listOfTemperature = []
    # take only temperatures of that CITY
    for element in myList:
        if element[3] == str(city):
            listOfTemperature.append(float(element[1]))

    # re-ordinate list from coldest to hottest
    listOfTemperature.sort()

    coldest = listOfTemperature[:n]
    hottest = listOfTemperature[-n:]

    print("Hottest Temperature in "+city+": "+str(hottest))
    print("Coldest Temperature in "+city+": "+str(coldest))

# Go function
hottestAndColdest(5, "Bangkok")

# Exercise 2.4
Rome = []
Bangkok = []

for element in myList:
    if element[3] == str("Rome"):
        Rome.append(float(element[1]))

for element in myList:
    if element[3] == str("Bangkok"):
        Bangkok.append(((float(element[1])-32)/1.8)) # from Fahrenheit to Celsius

# mean value
def mean(x):
    return sum(x)/len(x)

# standard deviation
def std(x):
    m = mean(x)
    return (mean([(y - m) ** 2 for y in x])) ** 0.5 # (sqrt)

# HOW TO PLOT:
colors = ['b', 'r']
cities = ["Rome", "Bangkok"]
values = [Rome, Bangkok]

for city, color, value in zip(cities, colors, values):
    plt.hist(value, density=True, alpha=0.2, color=color)
    m = mean(value)
    st = std(value)

    # linespaces
    x = np.linspace(m-5*st, m+5*st, 100)
    plt.plot(x, scipy.stats.norm(m, st).pdf(x), label=city, color=color)

plt.legend()
plt.show()

