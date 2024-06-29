import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
# import seaborn as sns
import joblib

# scroll mentok ke bawah, ada tutor penting!!!

def do_generate_model():
  dataset = pd.read_csv('data/dataset.csv')
  features = ['kasus_dbd', 'temp_avg', 'humidity_avg', 'rainfall_rate', 'kepadatan_penduduk']
  x = dataset[features].values
  
  scaler = StandardScaler()
  x_scaled = scaler.fit_transform(x)
  joblib.dump(scaler, 'data/scaler.pkl')
  
  find_optimal_clusters(x_scaled)
  
  n_clusters = 3 # menyesuaikan dengan hasil Elbow Method
  kmeans = KMeans(n_clusters=n_clusters, random_state=42)
  kmeans.fit(x_scaled)
  clusters = kmeans.labels_
  
  dataset['cluster'] = clusters
  
  for cluster_id in range(n_clusters):
    cluster_data = dataset[dataset['cluster'] == cluster_id]
    print(f'\nCluster {cluster_id} statistics:')
    print(cluster_data.describe())

  # Labeling
  cluster_labels = {0: 'Medium Risk DBD', 1: 'Low Risk DBD', 2: 'High Risk DBD'}

  # Membagi data menjadi data latih dan data uji
  X_train, X_test, y_train, y_test = train_test_split(x_scaled, clusters, test_size=0.1,
  random_state=42)

  # Mencari jumlah tetangga optimal untuk KNN dengan crossvalidation/GridSearchCV
  param_grid = {'n_neighbors': np.arange(1, 30)}
  knn = KNeighborsClassifier()
  knn_gscv = GridSearchCV(knn, param_grid, cv=5)
  knn_gscv.fit(X_train, y_train)
  print("Best number of neighbors:", knn_gscv.best_params_)
  print("Best cross-validated accuracy:", knn_gscv.best_score_)

  # KNN application
  best_k = knn_gscv.best_params_['n_neighbors']
  knn = KNeighborsClassifier(n_neighbors=best_k)
  knn.fit(X_train, y_train)
  y_pred = knn.predict(X_test)

  # Evaluasi Model
  accuracy = accuracy_score(y_test, y_pred)
  print("{:.2f}%\n".format(accuracy * 100))

  # Menampilkan beberapa prediksi dari data test dengan label
  predicted_labels = [cluster_labels[label] for label in y_pred]
  actual_labels = [cluster_labels[label] for label in y_test]
  print("Predicted clusters:\n", predicted_labels[:10])
  print("Actual clusters:\n", actual_labels[:10])

  # Cross-validation untuk evaluasi model
  cv_scores = cross_val_score(knn, x_scaled, clusters, cv=5)
  print(f'\nCross-Validation Scores: {cv_scores}')
  print(f'Mean CV Score: {np.mean(cv_scores)}')

  # save model
  joblib.dump(knn, 'data/knn_model.pkl')
  print("model saved")

  # Prediksi
  # loaded_knn = joblib.load('data/knn_model.pkl')

  # # Data baru
  # new_data = [[10, 25.5, 80, 15, 15000],
  #  [15, 28.3, 75, 20, 15000],
  #  [8, 26.8, 82, 10, 16000]]
  # new_data_scaled = scaler.transform(new_data)
  # new_predictions = loaded_knn.predict(new_data_scaled)

  # # Menampilkan label untuk prediksi data baru
  # new_predictions_labels = [cluster_labels[label] for label in new_predictions]
  # print("Predictions for new data:", new_predictions_labels)

  # Simpan dataset ke file JSON
  dataset.to_json('data/dataset_with_clusters.json', orient='records')
  print("Dataset with clusters saved to JSON")

# membaca dataset dari csv
# dataset = pd.read_csv('data/dataset.csv')
# print(dataset.head())

# # memisahkan fitur yang akan digunakan untuk clustering
# features = ['kasus_dbd', 'temp_avg', 'humidity_avg', 'rainfall_rate', 'kepadatan_penduduk']
# x = dataset[features].values
# print(x)

# # standarisasi data
# scaler = StandardScaler()
# x_scaled = scaler.fit_transform(x)
# joblib.dump(scaler, 'data/scaler.pkl')
# print(x_scaled)

# menentukan jumlah cluster optimal menggunakan elbow method
def find_optimal_clusters(x):
  inertia = []
  for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(x)
    inertia.append(kmeans.inertia_)
    
   # Menampilkan tabel inertia
  inertia_df = pd.DataFrame({'Number of Clusters': range(1, 10), 'Inertia': inertia})
  print(inertia_df)
  # Menampilkan grafik Elbow Method
  # plt.plot(range(1, 10), inertia, marker='o')
  # plt.xlabel('Number of clusters')
  # plt.ylabel('Inertia')
  # plt.title('Elbow Method for Optimal k')
  # plt.show()

# find_optimal_clusters(x_scaled)

# # clustering k-means
# # Digunakan 3 cluster, karena setelah 3 penurunan inertianya sudah stabil
# n_clusters = 3 # menyesuaikan dengan hasil Elbow Method
# kmeans = KMeans(n_clusters=n_clusters, random_state=42)
# kmeans.fit(x_scaled)
# clusters = kmeans.labels_

# # Menambahkan hasil clustering ke dataset
# dataset['cluster'] = clusters

# # Analisis Hasil Clustering untuk Labeling
# for cluster_id in range(n_clusters):
#   cluster_data = dataset[dataset['cluster'] == cluster_id]
#   print(f'\nCluster {cluster_id} statistics:')
#   print(cluster_data.describe())

# # Labeling
# cluster_labels = {0: 'Medium Risk DBD', 1: 'Low Risk DBD', 2: 'High Risk DBD'}

# # Membagi data menjadi data latih dan data uji
# X_train, X_test, y_train, y_test = train_test_split(x_scaled, clusters, test_size=0.1,
# random_state=42)

# # Mencari jumlah tetangga optimal untuk KNN dengan crossvalidation/GridSearchCV
# param_grid = {'n_neighbors': np.arange(1, 30)}
# knn = KNeighborsClassifier()
# knn_gscv = GridSearchCV(knn, param_grid, cv=5)
# knn_gscv.fit(X_train, y_train)
# print("Best number of neighbors:", knn_gscv.best_params_)
# print("Best cross-validated accuracy:", knn_gscv.best_score_)

# # KNN application
# best_k = knn_gscv.best_params_['n_neighbors']
# knn = KNeighborsClassifier(n_neighbors=best_k)
# knn.fit(X_train, y_train)
# y_pred = knn.predict(X_test)

# # Evaluasi Model
# accuracy = accuracy_score(y_test, y_pred)
# print("{:.2f}%\n".format(accuracy * 100))

# # Menampilkan beberapa prediksi dari data test dengan label
# predicted_labels = [cluster_labels[label] for label in y_pred]
# actual_labels = [cluster_labels[label] for label in y_test]
# print("Predicted clusters:\n", predicted_labels[:10])
# print("Actual clusters:\n", actual_labels[:10])

# # Cross-validation untuk evaluasi model
# cv_scores = cross_val_score(knn, x_scaled, clusters, cv=5)
# print(f'\nCross-Validation Scores: {cv_scores}')
# print(f'Mean CV Score: {np.mean(cv_scores)}')

# # save model
# joblib.dump(knn, 'data/knn_model.pkl')
# print("model saved")

# # Prediksi
# # loaded_knn = joblib.load('data/knn_model.pkl')

# # # Data baru
# # new_data = [[10, 25.5, 80, 15, 15000],
# #  [15, 28.3, 75, 20, 15000],
# #  [8, 26.8, 82, 10, 16000]]
# # new_data_scaled = scaler.transform(new_data)
# # new_predictions = loaded_knn.predict(new_data_scaled)

# # # Menampilkan label untuk prediksi data baru
# # new_predictions_labels = [cluster_labels[label] for label in new_predictions]
# # print("Predictions for new data:", new_predictions_labels)

# # Simpan dataset ke file JSON
# dataset.to_json('data/dataset_with_clusters.json', orient='records')
# print("Dataset with clusters saved to JSON")


# jalanin manual pakai ctrl + alt + n
do_generate_model()