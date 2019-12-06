from __future__ import absolute_import, division, print_function, unicode_literals
from sklearn import preprocessing, neighbors, svm
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from sklearn.model_selection import train_test_split

def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('label')
  train_ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    train_ds =train_ds.shuffle(buffer_size=len(dataframe))
    train_ds =train_ds.batch(batch_size)
  return train_ds

df = pd.read_csv('combined_data.csv', index_col=[0])
X = np.array(df.drop(['label'], 1))
y = np.array(df['label'])
print(X)
print(y)
# X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

# train, test = train_test_split(df, test_size=0.2)
# train, val = train_test_split(train, test_size=0.2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

clf = svm.SVC(decision_function_shape='ovo')
model = clf.fit(X_train, y_train)
print(model.score(X_test, y_test))
# print(model.score(X_test, y_test))
# print(X_test)
result = model.predict(X_test)
print(result == y_test)
#print(result)
