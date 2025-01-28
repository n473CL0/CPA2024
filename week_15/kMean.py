import numpy as np 
import matplotlib.pyplot as plt 

import csv


def initialise_centroids(k, data):

    #Centroids should be a list of k points, where each point is a tuple (feature1, feature2).
    centroids = []

    for i in range(k):
        #We randomly select a data point to be the centroid
        centroid = data[:, np.random.randint(data.shape[1])]
        centroids.append(centroid)

    return centroids


def assign_data_to_clusters(centroids, data):
    
    #Clusters should be a list of numpy arrays. Each array should contain all data points assigned to a cluster
    clusters = [np.array([])] * len(centroids)

    #Your code goes here
    for i in range(data.shape[1]):
        #We need to find the closest centroid to the data point
        closest_centroid = 0
        closest_distance = np.inf

        for j in range(len(centroids)):
            distance = np.linalg.norm(data[:, i] - centroids[j])
            if distance < closest_distance:
                closest_distance = distance
                closest_centroid = j

        #We add the data point to the closest cluster
        if len(clusters[closest_centroid]) == 0:
            clusters[closest_centroid] = data[:, i]
        else:
            clusters[closest_centroid] = np.vstack((clusters[closest_centroid], data[:, i]))

    return clusters

def calculate_cluster_means(clusters):

    #Centroids should be a list of points (x, y, ... ), with each point representing the mean position of all data in a cluster
    centroids = []
    
    for cluster in clusters:
        #We calculate the mean of the cluster
        centroid = np.mean(cluster)
        centroids.append(centroid)

    return centroids

def plot_clusters(clusters):

    #Your code goes here. You should plot all data, using a different color to represent each cluster. 
    plt.figure()

    colors = ['red', 'blue', 'green', 'yellow']

    for cluster in clusters:
        plt.scatter(cluster[0,:], cluster[1,:])
    
    # Add labels and legend
    plt.xlabel("Age")
    plt.ylabel("Creatine Phosphokinase")
    plt.show()

def kMeans(k, data, max_iterations = 100):

    #We need to randomly initialise the means (or centroids) before we can start
    centroids = initialise_centroids(k, data)

    #kMeans doesn't always converge, so we set a maximum number of iterations to stop our code from running forever. 
    for iteration in range(max_iterations):
        #We start by assigning data to clusters
        clusters = assign_data_to_clusters(centroids, data)

        #Next we update our centroids
        centroids = calculate_cluster_means(clusters)

    #Once finished, let's plot the clusters
    plot_clusters(clusters)


def read_csv():

    file = "heart_data.csv"

    age = []
    creatine = []

    with open(file, 'r') as csvfile:
        
        file = csv.DictReader(csvfile)

        for row in file:
            creatine.append(float(row['creatinine_phosphokinase']))
            age.append(float(row['age']))


    #Store the data as a 2 x 297 numpy array.
    return np.array([age,creatine])

data = read_csv()

kMeans(4, data)