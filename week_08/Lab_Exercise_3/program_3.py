import csv


cities = ['London', 'Bristol', 'Manchester', 'Reading', 'Liverpool', 'Brighton']

populations = [8982000, 467000, 553000, 174224, 496000, 290000]


with open('data_1.csv','w') as f:

    f = csv.writer(f, lineterminator="\n")

    f.writerow(cities)


with open('data_2.csv','w') as f:

    f = csv.writer(f, lineterminator='\n')

    f.writerows([cities, populations])


with open('data_3.csv', 'w') as f:

    f = csv.writer(f, lineterminator='\n')

    lines = [[c,p] for (c,p) in zip(cities, populations)]

    f.writerows(lines)
