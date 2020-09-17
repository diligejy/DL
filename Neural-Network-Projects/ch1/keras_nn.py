from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import numpy as np

model = Sequential()
# 레이어 1 
model.add(Dense(units = 4, activation = 'sigmoid', input_dim = 3))
# 출력 레이어
model.add(Dense(units = 1, activation = 'sigmoid'))
# print(model.summary())
# optimizers
sgd = optimizers.SGD(lr=1)
model.compile(loss='mean_squared_error', optimizer=sgd)

X = np.array([[0,0,1],
              [0,1,1],
              [1,0,1],
              [1,1,1]])
y = np.array([[0],[1],[1],[0]])

model.fit(X, y, epochs=1500, verbose=False)

print(model.predict(X))