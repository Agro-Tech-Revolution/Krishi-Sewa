import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import pickle

# import raw dataset
data_set_raw = pd.read_csv('Crop_rec.csv')

# preprocessing dataset
c = data_set_raw.label.astype('category')
targets = dict(enumerate(c.cat.categories))
data_set_raw['target'] = c.cat.codes

y = data_set_raw.target
X = data_set_raw[['N', 'P', 'K', 'temperature', 'humidity', 'ph', ]]

X_train, X_test, Y_train, Y_test = train_test_split(X, y, random_state=1)

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

Gbs_model = GradientBoostingClassifier()
Gbs_model.fit(X_train_scaled, Y_train)
#print(accuracy_score(Y_test, Gbs.predict(X_test_scaled)))

pickle.dump(Gbs_model, open("npk_model.sav", "wb"))
pickle.dump(scaler, open("scaler.sav", "wb"))
