import json


with open('sensor_data.json', encoding="utf-8-sig") as file:
    
    data = json.load(file)

    s1 = data['sensor_1']
    s2 = data['sensor_2']
    s3 = data['sensor_3']

    mean_1 = sum(s1)/len(s1)
    mean_2 = sum(s2)/len(s2)
    mean_3 = sum(s3)/len(s3)


mean_data =  {
    "mean_sensor_1": mean_1,
    "mean_sensor_2": mean_2,
    "mean_sensor_3": mean_3
}


with open('mean_sensor_data.json', 'w') as f:

    json.dump(mean_data, f)