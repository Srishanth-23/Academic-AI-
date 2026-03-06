import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor

import joblib

data = pd.DataFrame({

"attendance":[95,90,85,80,70,60,50,40,30,75],

"internal_marks":[90,85,80,75,65,55,45,35,30,70],

"coding_activity":[200,180,160,140,100,80,60,40,20,120],

"previous_cgpa":[9.2,9.0,8.7,8.5,8.0,7.5,7.0,6.5,6.0,8.2],

"final_cgpa":[9.3,9.1,8.8,8.6,8.1,7.6,7.2,6.7,6.2,8.3]

})

X = data[["attendance","internal_marks","coding_activity","previous_cgpa"]]

y = data["final_cgpa"]

X_train,X_test,y_train,y_test = train_test_split(

X,

y,

test_size=0.2,

random_state=42

)

model = RandomForestRegressor(

n_estimators=200,

max_depth=6

)

model.fit(

X_train,

y_train

)

joblib.dump(

model,

"app/ml/cgpa_model.pkl"

)

print("CGPA Prediction Model Trained Successfully")
