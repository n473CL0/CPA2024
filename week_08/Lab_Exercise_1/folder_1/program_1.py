import csv

with open('rainfall.csv', encoding='utf-8-sig') as f:
    
    f = csv.reader(f)

    f = list(f)
    print(f)


with open('../unit_description.txt', encoding='utf-8-sig') as f:

    f = f.readlines()
    print(f[2])


with open('./data/xyz_data.csv', encoding='utf-8-sig') as f:

    f = csv.reader(f)

    f = list(f)
    print(f)

    values = [[int(val) for val in line] for line in f[1:]]
    xz_sum = [v[0] + v[2] for v in values]
    print(xz_sum)