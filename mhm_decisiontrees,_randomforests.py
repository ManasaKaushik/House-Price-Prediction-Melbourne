# -*- coding: utf-8 -*-
"""MHM - DecisionTrees, RandomForests.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oMhiIt2c1jNAUL0gtYxgeGArexjqvJQZ
"""

#load datasets from device
from google.colab import files
uploaded = files.upload()

import pandas as pd
#store datasets in relevant dataframes
mel_pless = pd.read_csv('MELBOURNE_HOUSE_PRICES_LESS.csv')
mel_full = pd.read_csv('Melbourne_housing_FULL.csv')
#examine available columns in the dataset
mel_full.columns

#drop rows with any null values
mel_full = mel_full.dropna(axis=0)

#set the feature you want to predict as y
y = mel_full.Price

#pick a set of features you think are most relevant and call it X (the feature set)
house_features = ['Rooms', 'Bedroom2', 'Bathroom', 'YearBuilt', 'Landsize', 'Lattitude', 'Longtitude']
X = mel_full[house_features]
X.describe()
X.head()

from sklearn.tree import DecisionTreeRegressor
#first prediction trial using decision trees
model = DecisionTreeRegressor(random_state=7)
model.fit(X,y)

print('The price predictions are:')
v = model.predict(X)
print(v)

from sklearn.metrics import mean_absolute_error
#observe the error between the predicted value and the actual value
mean_absolute_error(y,v)

#Since the model is trained on the dataset entirely and is then tested on the
#dataset again, the validation of the model does not hold good because it already has
#access to the values it is going to predict. So we will use train_test_split here and
#have a different part of the dataset to exclusively test the model on.
from sklearn.model_selection import train_test_split
train_X,val_X,train_y,val_y = train_test_split(X,y,random_state=7)
model_tts = DecisionTreeRegressor(random_state=7)
model_tts.fit(train_X,train_y)
pred = model_tts.predict(val_X)
mean_absolute_error(val_y, pred)

#from such a high value difference of the predicted price vs the actual price, we understand
#that the model is overshooting the values. This is a topic of underfitting/overfitting.
#This can be controlled by changing the number of leaf nodes in the decision tree. Too many
#leaf nodes will cause overfitting while too little will lead to underfitting.
def find_best(max_leaf_nodes, train_X, val_X, train_y, val_y):
  model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=7)
  model.fit(train_X,train_y)
  prediction = model.predict(val_X)
  mae = mean_absolute_error(val_y, prediction)
  return mae

#for different values of the leaf nodes, check which one fits the best
for max_leaf_nodes in [50,100,200,400,800,1500,3000,5000]:
  eval = find_best(max_leaf_nodes, train_X, val_X, train_y, val_y)
  print("Max leaf nodes: %d \t\t Mean Absolute Error: %d" %(max_leaf_nodes, eval))

#We see that 400 seems to be a better number
#To dig down further, we can narrow down the loop from 300 to 800
candidate_max_leaf_nodes = [300,350,400,450,500,550,600,650,750,800,10000]
scores = {leaf_size: find_best(leaf_size, train_X, val_X, train_y, val_y) for leaf_size in candidate_max_leaf_nodes}
best_tree_size = min(scores, key=scores.get)
print(best_tree_size)
#We can confirm that the ideal number of leaf nodes is 400. Since we have the stats down, 
#we can now train the model on the entire dataset, instead of a part of it. 
final_model = DecisionTreeRegressor(max_leaf_nodes=best_tree_size,random_state=7)
final_model.fit(X,y)
r = final_model.predict(X)
mean_absolute_error(r,y)
#thus, we have brought down the mean aboslute error by atleast 50%, indicating that
#the validation accuracy has increased by 50%

#let us try the same prediction, but this time with random forests, as they work as predictors
#when compared to decision trees. This is because the RF uses many such component DT in order to
#compute an average of their outputs and use that instead.
from sklearn.ensemble import RandomForestRegressor
model_rf = RandomForestRegressor(random_state=7)
model_rf.fit(X, y)
v = model_rf.predict(X)
mean_absolute_error(v,y)

#we see that the regressor has reduced the error margin significantly.
#let us test some parameters and observe their effects. First test max_leaf_nodes
leaf_nodes = [50,100,200,400,800,1500,3000,5000]
for x in leaf_nodes:
  model_rf = RandomForestRegressor(random_state=7, max_leaf_nodes=x)
  model_rf.fit(train_X, train_y)
  v = model_rf.predict(val_X)
  calc = mean_absolute_error(v,val_y)
  print("Number of leaf nodes: %d \t\t Mean Absolute Error: %d " %(x, calc))

#let us continue to try higher numbers
leaf_nodes = [8000,10000,20000,40000,50000,70000,90000,100000]
for x in leaf_nodes:
  model_rf = RandomForestRegressor(random_state=7, max_leaf_nodes=x)
  model_rf.fit(train_X, train_y)
  v = model_rf.predict(val_X)
  calc = mean_absolute_error(v,val_y)
  print("Number of leaf nodes: %d \t\t Mean Absolute Error: %d " %(x, calc))

#we notice that at max_leaf_nodes of 5000, the error margin is the lowest and it stays the same.
#Let us check its effect on the complete dataset.
model_rf = RandomForestRegressor(random_state=7,max_leaf_nodes=5000)
model_rf.fit(X, y)
v = model_rf.predict(X)
mean_absolute_error(v,y)

