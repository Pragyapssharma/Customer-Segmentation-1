import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Load the data
#customers = pd.read_csv('./data/customers.csv')
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers.csv')
customers = pd.read_csv(data_path)

# Preprocess the data
customers_selected = customers[['total_spend', 'num_orders']]
scaler = StandardScaler()
customers_scaled = scaler.fit_transform(customers_selected)

# Perform K-Means clustering
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(customers_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

# Determine the optimal number of clusters (in this case, 3)
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
kmeans.fit(customers_scaled)

# Predict the cluster labels
labels = kmeans.labels_

# Add the cluster labels to the original data
customers['cluster'] = labels

# Analyze the clusters using descriptive statistics
print(customers.groupby('cluster')[['total_spend', 'num_orders']].describe())

# Visualize the clusters using a scatter plot
plt.scatter(customers['total_spend'], customers['num_orders'], c=customers['cluster'])
plt.title('Customer Segmentation')
plt.xlabel('Total Spend')
plt.ylabel('Number of Orders')
plt.show()