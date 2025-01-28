import csv

N=5

with open('sensor_data.csv', encoding='utf-8-sig') as f:
    
    f = csv.reader(f)
    
    data = [float(line[1]) for line in list(f)[1:]]

    filtered = []
    for ii in range(0, len(data)-(N-1)):
        filtered.append([str(sum(data[ii:ii+N])/N)])
    print(filtered)

with open('filtered_sensor_data.csv','w') as f:

    f = csv.writer(f, lineterminator='\n')

    f.writerows(filtered)
