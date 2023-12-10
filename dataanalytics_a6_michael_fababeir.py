# -*- coding: utf-8 -*-
"""DataAnalytics_A6_Michael_Fababeir.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NAm2XHZzv_HFo8urdtcFuGeKZYXG2ipM
"""

import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

data1 = pd.read_csv("synthea-pt30k4-lc-data-sel.csv") # Get synthetic patient data
nrows, ncolumns = data1.shape
print(nrows, ncolumns)

data2 = pd.read_csv("cancer patient data sets.csv") # Get patient data
nrows, ncolumns = data2.shape
print(nrows, ncolumns)

# count null values from both datasets
print(data1.isnull().sum())
print(data2.isnull().sum())

df1 = pd.DataFrame()

df1["age"] = data1["C-424144002"]
df1["gender"] = data1["C-263495000"].apply(lambda x: 1 if x == 'm' else 0)
df1["alcohol"] = data1["C-10939881000119104"].apply(lambda x: 1 if x is True else 0) # 1 is frequent drinker and 0 is non-frequent drinker
df1["smoking"] = data1["C-449868002"].apply(lambda x: 1 if x is True else 0) # 1 is frequent smoker and 0 is non-frequent smoker
df1["obesity"] = data1["C-162864005"].apply(lambda x: 1 if x is True else 0) # 1 is not obese, 2 is obese and 3, is severly obese
df1["coughing"] = data1["C-84229001"].apply(lambda x: 1 if x is True else 0) # 1 is frequent cougher and 0 is non-frequent cougher
df1["wheezing"] = data1["C-56018004"].apply(lambda x: 1 if x is True else 0) # 1 is frequent wheezing and 0 is non-frequent wheezing
df1["lung_cancer"] = data1["label"]

df2 = pd.DataFrame()

df2["age"] = data2["Age"]
df2["gender"] = data2["Gender"].apply(lambda x: 1 if x == 1 else 0)
df2["alcohol"] = data2["Alcohol use"].apply(lambda x: 1 if x > 4 else 0) # 1 is frequent drinker and 0 is non-frequent drinker
df2["smoking"] = data2["Smoking"].apply(lambda x: 1 if x > 5 else 0) # 1 is frequent smoker and 0 is non-frequent smoker
df2["obesity"] = data2["Obesity"].apply(lambda x: 1 if x > 4 else 0) # 1 is obese and 0 is not obese
df2["coughing"] = data2["Dry Cough"].apply(lambda x: 1 if x > 4 else 0) # 1 is frequent cougher and 0 is non-frequent cougher
df2["wheezing"] = data2["Wheezing"].apply(lambda x: 1 if x > 4 else 0) # 1 is frequent wheezing and 0 is non-frequent wheezing
df2["lung_cancer"] = data2["Level"].apply(lambda x: 0 if x == "Low" else 1)

combined_df = df1.append(df2)
combined_df['id'] = range(1, len(combined_df) + 1)
nrows, ncolumns = combined_df.shape
print(nrows, ncolumns)

# Data 1 analysis
# Strip plot for age distribution
plt.figure(figsize=(12, 6))
sns.stripplot(x='gender', y='age', data=df1, jitter=True, hue='smoking', palette='Set2')
plt.title('Strip Plot for Categorical Age Distribution')
plt.xlabel('Gender')
plt.ylabel('Age')
plt.show()

# Bar gaphs counting the occurences of each variables
categorical_columns = ['alcohol', 'smoking', 'obesity', 'coughing', 'wheezing', 'lung_cancer']
plt.figure(figsize=(15, 10))

for i, column in enumerate(categorical_columns, 1):
    plt.subplot(2, 3, i)
    sns.countplot(x=column, data=df1, palette='viridis')
    plt.title(f'Bar Graph for {column.capitalize()}')
    plt.xlabel(column)
    plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Histograms for Age and Other Attributes
numerical_columns = ['age']
plt.figure(figsize=(12, 6))

for i, column in enumerate(numerical_columns, 1):
    plt.subplot(1, 1, i)
    sns.histplot(df1[column], kde=True, color='skyblue', bins=20)
    plt.title(f'Histogram for {column.capitalize()}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

print(set(df1["alcohol"]))

# Correlation matrix
correlation_matrix = df1.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix')
plt.show()

# Search for outliers in age


# Box plot
plt.figure(figsize=(8, 6))
sns.boxplot(x=df1['age'])
plt.title('Box Plot for Age')
plt.show()

Q1 = df1['age'].quantile(0.25)
Q3 = df1['age'].quantile(0.75)
IQR = Q3 - Q1

threshold = 1.5

# Interquartile range
outliers = df1[(df1['age'] < Q1 - threshold * IQR) | (df1['age'] > Q3 + threshold * IQR)]

print(f"Potential Outliers in Age: {outliers[['age']]}")

# Data 2 analysis
# Strip plot for age distribution
plt.figure(figsize=(12, 6))
sns.stripplot(x="gender", y="age", data=df2, jitter=True, hue="smoking", palette="Set2")
plt.title('Strip Plot for Categorical Age Distribution')
plt.xlabel("Gender")
plt.ylabel("Age")
plt.show()

# Bar gaphs counting the occurences of each variables
categorical_columns = ['alcohol', 'smoking', 'obesity', 'coughing', 'wheezing', 'lung_cancer']
plt.figure(figsize=(15, 10))

for i, column in enumerate(categorical_columns, 1):
    plt.subplot(2, 3, i)
    sns.countplot(x=column, data=df2, palette='viridis')
    plt.title(f'Bar Graph for {column.capitalize()}')
    plt.xlabel(column)
    plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Histograms for Age and Other Attributes
numerical_columns = ["age"]
plt.figure(figsize=(12, 6))

for i, column in enumerate(numerical_columns, 1):
    plt.subplot(1, 1, i)
    sns.histplot(df2[column], kde=True, color='skyblue', bins=20)
    plt.title(f'Histogram for {column.capitalize()}')
    plt.xlabel(column)
    plt.ylabel("Frequency")
plt.tight_layout()
plt.show()


# Correlation matrix
correlation_matrix = df2.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix')
plt.show()

# Search for outliers in age


# Box plot
plt.figure(figsize=(8, 6))
sns.boxplot(x=df2['age'])
plt.title('Box Plot for Age')
plt.show()

Q1 = df2['age'].quantile(0.25)
Q3 = df2['age'].quantile(0.75)
IQR = Q3 - Q1

threshold = 1.5

# Interquartile range
outliers = df2[(df2['age'] < Q1 - threshold * IQR) | (df2['age'] > Q3 + threshold * IQR)]

print(f"Potential Outliers in Age: {outliers[['age']]}")

summary_statistics = combined_df.describe()
print(summary_statistics)

combined_df[["age"]] = MinMaxScaler().fit_transform(combined_df[["age"]])
print(combined_df)

X = combined_df.drop(columns=["lung_cancer"]) # split into X and y sets
y = combined_df["lung_cancer"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=147932)

# Support Vector Classifier

svc_model = SVC(kernel='linear', random_state = 147932)
svc_model.fit(X_train, y_train)

y_pred_svc = svc_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred_svc)

print(accuracy_score(y_test, y_pred_svc))
print(precision_score(y_test, y_pred_svc, average='macro'))
print(recall_score(y_test, y_pred_svc, average = 'macro'))
print(f1_score(y_test, y_pred_svc, average = 'macro'))
print(f'Mean Squared Error (SVC): {mse}')
svc_conf_matrix = confusion_matrix(y_test, y_pred_svc)

# KNeighbors Regression

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)

y_pred_knn = knn_model.predict(X_test)


mse_knn = mean_squared_error(y_test, y_pred_knn)
print(accuracy_score(y_test, y_pred_knn))
print(precision_score(y_test, y_pred_knn, average='macro'))
print(recall_score(y_test, y_pred_knn, average = 'macro'))
print(f1_score(y_test, y_pred_knn, average = 'macro'))
print(f'Mean Squared Error (KNN): {mse_knn}')
knn_conf_matrix = confusion_matrix(y_test, y_pred_knn)

# Random Forest Regression

rf_model = RandomForestClassifier(n_estimators=100, random_state=147932)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)


mse_rf = mean_squared_error(y_test, y_pred_rf)
print(accuracy_score(y_test, y_pred_rf))
print(precision_score(y_test, y_pred_rf, average='macro'))
print(recall_score(y_test, y_pred_rf, average = 'macro'))
print(f1_score(y_test, y_pred_rf, average = 'macro'))
print(f'Mean Squared Error (Random Forest): {mse_rf}')
rf_conf_matrix = confusion_matrix(y_test, y_pred_rf)

# Logistic Regression

logreg_model = LogisticRegression()
logreg_model.fit(X_train, y_train)


y_pred_lr = logreg_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred_lr)

mse_lr = mean_squared_error(y_test, y_pred_lr)

print(accuracy_score(y_test, y_pred_lr))
print(precision_score(y_test, y_pred_lr, average='macro'))
print(recall_score(y_test, y_pred_lr, average = 'macro'))
print(f1_score(y_test, y_pred_lr, average = 'macro'))
print(f'Mean Squared Error (Logistic Regression): {mse_lr}')
lr_conf_matrix = confusion_matrix(y_test, y_pred_lr)

# Visualize Confusion Matrices
plt.figure(figsize=(15, 5))

plt.subplot(1, 4, 1)
sns.heatmap(rf_conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.title('Random Forest')

plt.subplot(1, 4, 2)
sns.heatmap(svc_conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.title('Support Vector Machines')

plt.subplot(1, 4, 3)
sns.heatmap(knn_conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.title('K-Nearest Neighbors')

plt.subplot(1, 4, 4)
sns.heatmap(lr_conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.title('Logistic Regression')

plt.tight_layout()
plt.show()