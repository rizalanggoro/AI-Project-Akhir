import json
import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from lib.prediction import do_prediction
from lib.generate_model import do_generate_model

# # Inisialisasi scaler dan load model
# scaler = joblib.load('data/scaler.pkl') 
# cluster_labels = {0: 'Medium Risk DBD', 1: 'Low Risk DBD', 2: 'High Risk DBD'}
# loaded_knn = joblib.load('data/knn_model.pkl')

# # Fungsi prediksi
# def prediction(x):
#     # Data baru dalam bentuk array 2D untuk scaler
#     x_scaled = scaler.transform([x])
#     new_prediction = loaded_knn.predict(x_scaled)
    
#     # Menampilkan label untuk prediksi data baru
#     new_prediction_label = cluster_labels[new_prediction[0]]
#     return new_prediction_label

# Contoh penggunaan fungsi prediction
# new_data = [10, 25.5, 80, 15, 15000]
# predicted_label = prediction(new_data)
# print("Prediction for new data:", predicted_label)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins=["http://localhost:5174/"])
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # # endpoint untuk generate model
    # @app.route('/api/model', methods=['GET'])
    # def getModel():
    #     do_generate_model()
    #     # with open('data/dataset_with_clusters.json', 'r') as f:
    #     #     dataset_json = json.load(f)
    #     return jsonify({})
      
    # endpoint untuk prediksi data
    @app.route('/api/prediction', methods=['POST'])
    @cross_origin(origin='localhost', headers=['Content-Type','application/json'])
    def handlePrediction():
      # Mendapatkan data JSON dari request body
      data = request.get_json()
      
      # Mendapatkan nilai dari parameter yang diharapkan
      kasus_dbd = data.get('kasus_dbd')
      temp_avg = data.get('temp_avg')
      humidity_avg = data.get('humidity_avg')
      rainfall_rate = data.get('rainfall_rate')
      kepadatan_penduduk = data.get('kepadatan_penduduk')
      
      if None in [kasus_dbd, temp_avg, humidity_avg, rainfall_rate, kepadatan_penduduk]:
          return jsonify({"error": "Missing parameters"}), 400
      
      # Data baru dalam bentuk array satu dimensi
      new_data = [kasus_dbd, temp_avg, humidity_avg, rainfall_rate, kepadatan_penduduk]
      
      # Melakukan prediksi
      predicted_label = do_prediction(new_data)
      
      return jsonify({"prediction": predicted_label})

    # endpoint untuk mendapatkan dataset yang sudah di cluster
    @app.route('/api/dataset', methods=['GET'])
    def getDataset():
        with open('data/dataset_with_clusters.json', 'r') as f:
            dataset_json = json.load(f)
        response = jsonify(dataset_json)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    @app.route('/api/image/after-clustering', methods=['GET'])
    def getAfterClusteringPlot():
        return send_file('../data/images/after_clustering.png', mimetype='image/png')
    
    @app.route('/api/image/before-clustering', methods=['GET'])
    def getBeforeClusteringPlot():
        return send_file('../data/images/before_clustering.png', mimetype='image/png')

    return app