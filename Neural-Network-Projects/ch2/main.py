from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from keras import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('diabetes.csv')
# print(df.isnull().sum())
# print(df.describe())
print('Number of rows with 0 values for each variable')
for col in df.columns:
    missing_rows = df.loc[df[col] == 0].shape[0]
    print(col + ': ' + str(missing_rows))

df['Glucose'] = df['Glucose'].replace(0, np.nan)
df['BloodPressure'] = df['BloodPressure'].replace(0, np.nan)
df['SkinThickness'] = df['SkinThickness'].replace(0, np.nan)
df['Insulin'] = df['Insulin'].replace(0, np.nan)
df['BMI'] = df['BMI'].replace(0, np.nan)

print('Number of rows with 0 values for each variable')
for col in df.columns:
    missing_rows = df.loc[df[col] == 0].shape[0]
    print(col + ': ' + str(missing_rows))

df['Glucose'] = df['Glucose'].fillna(df['Glucose'].mean())
df['BloodPressure'] = df['BloodPressure'].fillna(df['BloodPressure'].mean())
df['SkinThickness'] = df['SkinThickness'].fillna(df['SkinThickness'].mean())
df['Insulin'] = df['Insulin'].fillna(df['Insulin'].mean())
df['BMI'] = df['BMI'].fillna(df['BMI'].mean())

# Data Regularization
df_scaled = preprocessing.scale(df)
df_scaled = pd.DataFrame(df_scaled, columns = df.columns)
# No need for Target Variable Regularization
df_scaled['Outcome'] = df['Outcome']
df = df_scaled

print(df.describe().loc[['mean', 'std', 'max'],].round(2).abs())

X = df.loc[:, df.columns != 'Outcome']
y = df.loc[:, 'Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.2)

# Model Configuration
model = Sequential()
model.add(Dense(32, activation='relu', input_dim=8))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=200, verbose=False)

# Results - Accuracy
scores = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: %.2f%%\n" % (scores[1]*100))
scores = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy: %.2f%%\n" % (scores[1]*100))

y_test_pred = model.predict_classes(X_test)
c_matrix = confusion_matrix(y_test, y_test_pred)
ax = sns.heatmap(c_matrix, annot = True, 
                xticklabels = ['No Diabetes', 'Diabetes'],
                yticklabels = ['No Diabetes', 'Diabetes'],
                cbar = False, cmap = 'Blues')
ax.set_xlabel('Prediction')
ax.set_ylabel('Actual')
plt.show()
plt.clf()

# roc curve
y_test_pred_probs = model.predict(X_test)
FPR, TPR, _ = roc_curve(y_test, y_test_pred_probs)
plt.plot(FPR, TPR)
plt.plot([0, 1], [0, 1], '--', color = 'black') # 대각선
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.show()
plt.clf()