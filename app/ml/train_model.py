import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

import joblib

data = pd.DataFrame({

"attendance":[95,85,70,60,50,90,80,40,30,75],

"marks":[90,80,65,50,40,85,70,35,30,60],

"coding":[200,150,80,40,20,180,120,10,5,60],

"risk":[0,0,1,1,1,0,0,1,1,1]

})

X = data[["attendance","marks","coding"]]

y = data["risk"]

X_train,X_test,y_train,y_test = train_test_split(

X,

y,

test_size=0.2,

random_state=42

)

model = RandomForestClassifier(

n_estimators=200,

max_depth=6

)

model.fit(

X_train,

y_train

)

joblib.dump(

model,

"app/ml/model.pkl"

)

print("Model trained successfully")
