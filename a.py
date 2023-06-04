import streamlit as st


page_bg_img = '''
<style>
.stApp {
background-image: url("https://i.ibb.co/Nt9NzzK/e-4.png");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
import datetime
from datetime import date
import time
from datetime import datetime
import streamlit as st
from PIL import Image

        
#напишем приветствие
st.header('Здравствуйте!')
st.write('Здесь Вы можете воспользоваться нашей учебной версией кредитного конвейера.')
st.write('Заполните форму, чтобы оценить свои шансы на получение кредита')

#создадим интерфейс для ввода данных

LOAN=0
CLNO=None
VALUE=0
REASON=0
JOB=0
YOJ=0
CLAGE=None
DEROG=None
DELINQ=None
DEBTIN=None
NINQ=None
MORTDUE=None



LOAN = st.slider('**На какую сумму Вы хотели бы взять кредит?**', 0, 100000, 0, 1000)
VALUE = st.slider('**На сколько вы оцениваете свою собственность?**',0, 1000000,0, 50000)
REASON = st.selectbox(
'**Зачем Вы берете кредит?**',
('На обустройство дома', 'Для консолидации долга'))
JOB = genre = st.radio(
"**Кем Вы работаете?**",
('Менеджер', 'Офисный работник', 'В продажах', 'Профессор', 'Работаю на себя','Другое'))
given_date1 = st.date_input("**Когда Вы начали работать на текущей должности?**", min_value= date(1923, 1, 1) )
current_date = datetime.now()
#по дате посчитаем, сколько месяцев прошло с вступления заёмщика в должность
YOJ = (current_date.year - given_date1.year) * 12 + (current_date.month - given_date1.month)
INC = st.text_input('**Сколько Вы зарабатываете в месяц?**')
DEBT = st.text_input('**Сколько в месяц Вы тратите на погашение других кредитов?**')
try:
    DEBTINC=float(DEBT)/float(INC)
except:
    DEBTINC=0

import joblib
#загрузим сохраненную модель классификации
pipeline = joblib.load('pipeline_file.pkl')

data_file = 'data.csv'
if st.session_state.get('loaded_data'):
    df = pd.read_csv(data_file)
else:
    column_names = ['LOAN', 'MORTDUE', 'VALUE', 'REASON', 'JOB', 'YOJ', 'DEROG',
                    'DELINQ', 'CLAGE', 'NINQ', 'CLNO', 'DEBTINC']
    df = pd.DataFrame(columns=column_names)
    st.session_state['loaded_data'] = True

image = Image.open('star.png').resize((270, 300))

#импортируем функцию для связи с внешними данными
from my_functions import otvet
if st.button('Рассчитать'):
    with st.spinner('Пожалуйста, подождите...'):
        new_row = {'LOAN': LOAN,'VALUE': VALUE, 'MORTDUE': MORTDUE, 'REASON': REASON,
           'JOB': JOB, 'YOJ': YOJ, 'DEROG': DEROG,
           'DELINQ': DELINQ, 'CLAGE': CLAGE, 'NINQ': NINQ,
           'CLNO': CLNO, 'DEBTINC': DEBTINC}
        new_row = pd.DataFrame(new_row, index=[0])
        df = pd.concat([df, new_row], ignore_index=True)
        y_pred_proba = pipeline.predict_proba(df[-1])
        df.to_csv(data_file, index=False)  
        time.sleep(7)
        st.write(df)
        if otvet(y_pred_proba)=='Вам предварительно одобрен кредит!':
            st.write('Вам предварительно одобрен кредит!')
            st.image(image)
            st.balloons()
            st.write(y_pred_proba)
        else:
            st.write('Благодарим за обращение, но пока мы не можем оформить вам кредит(')
            st.write(y_pred_proba)
