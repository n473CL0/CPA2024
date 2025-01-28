'''
Student	Question 1	Question 2	Question 3
Martin	6	1	4
Arthur	3	8	4
Hemma	7	4	5
Josh	4	7	3
'''

import math 
import csv

names = ["Martin", "Arthur", "Hemma", "Josh"]
Q1 = [6, 3, 7, 4]
Q2 = [1, 8, 4, 7]
Q3 = [4, 4, 5, 3]

#Paste your code from last week's exercise

mean_i = [0]

## question 1

Fmean = lambda x: sum(x)/len(x)
std = lambda data: (sum([v*v for v in data])/len(data) - (sum(data)/(len(data)))**2)**0.5

for (q1, q2, q3) in zip(Q1, Q2, Q3):
    mean_i.append(Fmean([q1, q2, q3]))

    
mean = Fmean(mean_i)
std_t = std(mean_i)

print("mean is", mean)
print("standard_deviation is", std_t)



normalize = lambda x, u: x - u
normalize_ls = lambda data, mu: [normalize(v, u) for v in data]

def Mark(mark, mu, std):
    mark_n = normalize(mark, mu)
    if mark_n > std:
        return 'A'
    if mark_n >= 0:
        return 'B'
    if mark_n >= -1 * std:
        return 'C'
    return 'Fail'

marks_i = []

for (name, mark) in zip(names, mean_i):
    marks_i.append(Mark(mark, mean, std_t))


#Write your code for saving the table to a csv file

headings = ['Student','Question 1','Question 2','Question 3','Grade']

with open('grades.csv','w') as f:

    f = csv.writer(f, lineterminator='\n')

    data = []

    data.append(headings)

    for (a,b,c,d,e) in zip(names, Q1, Q2, Q3, marks_i):
        data.append([a,b,c,d,e])

    f.writerows(data)