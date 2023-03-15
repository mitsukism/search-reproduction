import json
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
from sklearn.linear_model import LinearRegression


def predict(request):
    # POSTされたJSONオブジェクトを取得する
    data = request.get_json()

    # 回答のみを取得する
    answer1 = data['question1']
    answer2 = data['question2']
    answer3 = data['question3']
    answer4 = data['question4']
    answer5 = data['question5']
    answer6 = data['question6']
    answer7 = data['question7']
    answer8 = data['question8']
    answer9 = data['question9']
    answer10 = data['question10']

    answer=[answer1,answer2,answer3,answer4,answer5,answer6,answer7,answer8,answer9,answer10]
    sequences =[[1, 3, 5, 2, 3, 4, 3],
        [1, 3, 5, 3, 5, 3, 5, 2, 3, 7, 6, 6],
        [1, 3, 7, 5, 3, 5 ,3 ,5, 2 ,3 ,5 ,2 ,2 ,4, 3],
        [1, 3, 6, 6, 5, 3, 7, 7, 6, 5, 3, 6, 6, 6, 6, 5, 3, 5, 5, 3, 5, 3 ,7 ,6 ,6 ,6 ,6 ,5 ,3, 7, 7, 7 ,7 ,7 ,7 ,7 ,7, 7, 7 ,7 ,7 ,5 ,4, 2, 3],
        [1, 3, 3, 7, 7, 5, 2, 3, 6, 5, 3, 5, 4, 2, 3, 7, 7, 5, 4, 3, 5, 4, 2, 3, 6, 6, 6, 6, 6, 6, 7, 7, 7, 5, 3, 6, 6, 6, 5, 2, 2, 2, 2, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 3, 5, 2, 3, 5, 3, 5, 2, 3, 5, 2, 2 ,2 ,2 ,3, 6, 6,7, 7, 6, 7, 6, 6, 7],
        [1, 2, 2, 3, 5, 3 ,7 ,5 ,3 ,6 ,6, 5, 2, 2, 2, 2, 3, 6, 6, 5, 2, 2, 3, 7, 7, 7, 5, 3],
        [1, 2, 2, 2, 2, 3, 5, 2, 3],
        [1, 2, 3, 6, 5, 2, 3, 7, 5, 2, 3, 7],
        [1, 3, 6, 6, 7, 7, 7, 7, 5, 3, 6],
        [1, 3, 7, 7, 6, 7, 6, 6, 6],
        [1, 3, 6, 6, 5, 2, 2, 3],
        [1, 2, 3, 5, 3, 6, 6, 6, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 6, 6, 5, 3]]
    n=1

    predict_num=predict_search(sequences,n,answer)
    return predict_num


def predict_search(sequences,n,next_sequence):
  next_sequence_num=len(next_sequence)
  #パターンを見つけるために数列を平坦化
  flattened_sequences=[num for seq in sequences for num in seq]

  #特徴量と目標変数を作成
  X=[]
  x=[]
  y=[]
  for i in range(len(flattened_sequences)-next_sequence_num):
    for j in range(next_sequence_num):
      x.append(flattened_sequences[i+j])
      if(len(x)==next_sequence_num):
        X.append(x)
        x=[]
    y.append(flattened_sequences[i+next_sequence_num])
  X=np.array(X)
  y=np.array(y)
  model=LinearRegression()
  model.fit(X,y)
  for i in range(n):
    next_num = model.predict([next_sequence])
  return int(next_num)

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # 予測モデルからの出力値を取得する
    predict_num = predict(request)

    # HTTPレスポンスを生成する
    response_data = {
        'prediction': predict_num
    }
    response = jsonify(response_data) # dictをJSON形式に変換
    response.status_code = 200 # HTTPレスポンスのステータスコードを設定
    return response