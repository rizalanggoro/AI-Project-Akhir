import joblib

scaler = joblib.load('data/scaler.pkl') 
cluster_labels = {0: 'Medium Risk DBD', 1: 'Low Risk DBD', 2: 'High Risk DBD'}
loaded_knn = joblib.load('data/knn_model.pkl')

def do_prediction(x):
  # Data baru dalam bentuk array 2D untuk scaler
  x_scaled = scaler.transform([x])
  new_prediction = loaded_knn.predict(x_scaled)
  
  # Menampilkan label untuk prediksi data baru
  new_prediction_label = cluster_labels[new_prediction[0]]
  return new_prediction_label