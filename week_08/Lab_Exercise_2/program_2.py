import csv

with open('rainfall.csv', encoding='utf-8-sig') as f:
    f = csv.reader(f)

    f = list(f)
    print(f)

data = [int(x) for x in f[1]]

mean = sum(data)/len(data)
var = sum([x*x for x in data])/len(data) - (sum(data)/(len(data)))**2
std = var**0.5

print('mean:', mean)
print('std:', std)