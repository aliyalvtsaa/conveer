import streamlit as st
import datetime
import time
import streamlit as st
from PIL import Image

st. set_page_config(layout="wide")
st.header('Здравствуйте!')

st.subheader('На этой страничке вы можете воспользоваться нашей учебной версией кредитного конвейера.')
st.write('Введите доступные вам данные, чтобы оценить свои шансы на получение кредита')
# Create two columns
col1, col2, col3 = st.columns(3)

LOAN=None
CLNO=None
MORTDUE=None
VALUE=None
REASON=None
JOB=None
YOJ=None
DEROG=None
DELINQ=None
DEBTINC=None
NINQ=None
CLAGE=None
# Add inputs to the first column

with col1:
    LOAN = st.slider('На какую сумму вы хотите взять кредит? (LOAN)', 0, 100000, 1000)
    MORTDUE = st.slider('Какой у вас долг по ипотеке? (MORTDUE)',0, 500000, 10000)
    CLNO = st.slider('Сколько у вас кредитов на данный момент? (CLNO)', 0, 100, 1)
    VALUE = st.slider('На сколько вы оцениваете свою собственность? (VALUE)',0, 1000000, 50000)

# Add inputs to the second column
with col2:
    REASON = st.selectbox(
    'Зачем вы берете кредит? (REASON)',
    ('На обустройство дома', 'Для консолидации долга'))
    JOB = genre = st.radio(
    "Кем вы работаете?",
    ('Менеджер', 'Офисный работник', 'В продажах', 'Профессор', 'Работаю на себя','Другое'))
    YOJ = st.slider('Сколько вы проработали на этой работе? (YOJ)',0, 100, 5)
    given_date = st.date_input("When\'s your birthday")
from datetime import datetime
current_date = datetime.now()
# Calculate the difference in months
CLAGE = (current_date.year - given_date.year) * 12 + (current_date.month - given_date.month)


try:
    DEBTINC=INC/DEBT
except:
    DEBTINC=0

with col3:
    DEROG = st.slider('Сколько у вас было серьезных уничижительных отчетов? (DEROG)',0, 10, 1)
    DELINQ = st.slider('Сколько у вас просроченных кредитов? (DELINQ)',0, 15, 1)
    INC = st.text_input('Сколько вы зарабатываете в месяц? (INC)')
    DEBT = st.text_input('Сколько вы тратите на погашение кредитов в месяц? (DEBT)')
try:
    DEBTINC=INC/DEBT
except:
    DEBTINC=0

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

import joblib

# Load the saved pipeline from the file
pipeline = joblib.load('pipeline_file.pkl')


import pandas as pd
# Create an empty DataFrame
df2 = pd.DataFrame(columns=['LOAN', 'MORTDUE', 'VALUE', 'REASON', 'JOB', 'YOJ', 'DEROG',
                            'DELINQ', 'CLAGE', 'NINQ', 'CLNO', 'DEBTINC'])

# Create a dictionary with the values for the new row
new_row = {'LOAN': LOAN, 'MORTDUE': MORTDUE, 'REASON': REASON,
           'JOB': JOB, 'YOJ': YOJ, 'DEROG': DEROG,
           'DELINQ': DELINQ, 'CLAGE': CLAGE, 'NINQ': NINQ,
           'CLNO': CLNO, 'DEBTINC': DEBTINC}
new_row = pd.DataFrame(new_row, index=[0])
# Add the new row to the DataFrame
df2 = pd.concat([df2, new_row], ignore_index=True)
df2['REASON'] = df2['REASON'].replace(['На обустройство дома', 'Для консолидации долга'], [0, 1])
df2['JOB'] = df2['JOB'].replace(['Другое', 'В продажах', 'Офисный работник', 'Менеджер', 'Профессор', 'Работаю на себя'], 
                                [0, 1, 2, 3, 4, 5])
y_pred_proba = pipeline.predict_proba(df2)
image = Image.open('money.png').resize((300, 200))
from my_functions import otvet

if st.button('Рассчитать'):
    with st.spinner('Пожалуйста, подождите...'):
        time.sleep(7)
        if otvet(y_pred_proba)=='Вам предварительно одобрен кредит!':
            st.write('Вам предварительно одобрен кредит!')
            st.image(image)
            st.balloons()
        else:
            st.write('Благодарим за обращение, но пока мы не можем оформить вам кредит(')
        
