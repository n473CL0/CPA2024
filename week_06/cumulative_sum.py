
# Cumulative sum

list_of_numbers = [1,3,6,10]

def cumulativeSum(ls):
    return [sum(ls[:ii+1]) for ii in range(len(ls))]

print(cumulativeSum(list_of_numbers))

f = lambda x, ls: sum(ls[:x+1])
g = lambda x: [f(ii, x) for ii in range(len(x))]

print(g(list_of_numbers))

