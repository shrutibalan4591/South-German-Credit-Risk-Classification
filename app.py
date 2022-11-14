import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Function for encoding status value
def status_encode(status):
  if status==1:
    return([1,0,0])
  elif status==3:
    return([0,1,0])
  elif status==4:
    return([0,0,1])
  else:
    return([0,0,0])

# Function for encoding employment_duration value
def ed_encode(ed):
  if ed==1:
    return([1,0,0,0])
  elif ed==2:
    return([0,1,0,0])
  elif ed==4:
    return([0,0,1,0])
  elif ed==5:
    return([0,0,0,1])
  else:
    return([0,0,0,0])

# Function for encoding savings value
def savings_encode(savings):
  if savings==1:
    return([1,0,0])
  elif savings==4:
    return([0,1,0])
  elif savings==5:
    return([0,0,1])
  else:
    return([0,0,0])

# Function for encoding other_debtors value
def other_debtors_encode(od):
  if od==1:
    return([1,0,0])
  elif od==2:
    return([0,1,0])
  elif od==3:
    return([0,0,1])
  else:
    return([0,0,0])

# Function for encoding other_debtors value
def credit_history_encode(ch):
  if ch==0:
    return([1,0,0,0])
  elif ch==1:
    return([0,1,0,0])
  elif ch==3:
    return([0,0,1,0])
  elif ch==4:
    return([0,0,0,1])
  else:
    return([0,0,0,0])

# Function for encoding purpose value
def purpose_encode(purpose):
  if purpose==0:
    return([1,0,0])
  elif purpose==1:
    return([0,1,0])
  elif purpose==6:
    return([0,0,1])
  else:
    return([0,0,0])

# Function for encoding property value
def property_encode(property):
  if property==1:
    return([1,0,0])
  elif property==2:
    return([0,1,0])
  elif property==4:
    return([0,0,1])
  else:
    return([0,0,0])

# Function for encoding housing value
def housing_encode(housing):
  if housing==1:
    return([1,0])
  elif housing==2:
    return([0,1])
  else:
    return([0,0])

# Function for encoding other_installment_plans value
def oip_encode(oip):
  if oip==3:
    return([1])
  else:
    return([0])

# Function for encoding other_installment_plans value
def pss_encode(pss):
  if pss==3:
    return([1])
  else:
    return([0])

app = Flask(__name__)

model = pickle.load(open('crc.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        duration = [int(request.form['duration'])]
        amount = [int(request.form['amount'])]
        age = [int(request.form['age'])]

        status = status_encode(int(request.form['status']))
        employment_duration  = ed_encode(int(request.form['emp_dur']))
        savings = savings_encode(int(request.form['savings']))
        other_debtors = other_debtors_encode(int(request.form['other_debtors']))
        credit_history = credit_history_encode(int(request.form['credit_history']))
        purpose = purpose_encode(int(request.form['purpose']))
        property = property_encode(int(request.form['property']))
        other_installment_plans = oip_encode(int(request.form['other_installments']))
        housing = housing_encode(int(request.form['housing']))
        personal_status_sex = pss_encode(int(request.form['personal_status']))

    features = duration + amount + age + status + employment_duration + savings + other_debtors
    features = features + credit_history + purpose + property + other_installment_plans + housing + personal_status_sex

    features_arr = [np.array(features)]

    prediction = model.predict(features_arr)
  
    result = ""
    if prediction == 1:
      result = "GOOD RISK"
    else:
      result = "BAD RISK"

    return render_template('index.html', prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
