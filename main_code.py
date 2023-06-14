import streamlit as st
import datetime
from datetime import date
import time
from datetime import datetime
import streamlit as st
from PIL import Image
import pandas as pd
#установим градиентный фон для нашего интерфейса
page_bg_img = '''
<style>
.stApp {
background-image: url("https://sun9-45.userapi.com/impg/VNJn_pn39ZxAKRVxLTlIG6OfLqj_V66jorJFPg/8bx4oihFGW0.jpg?size=1920x1080&quality=95&sign=5584774fc19d4bc9a604e7c90bd2a69d&type=album");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
        
#поприветствуем пользователя
st.header('Здравствуйте!')
st.write('Здесь Вы можете воспользоваться нашей учебной версией кредитного конвейера.')
st.write('Заполните форму, чтобы оценить свои шансы на получение кредита')

#создадим переменные: тем, по которым пользователь будет вводить данные присвоим 0, 
#а тем, которые мы возьмем "из внутренней базы данных", присвоим NA

LOAN=0
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
CLNO=None


#попросим пользователя ввести данные (** - для жирного шрифта)
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
#по дате посчитаем, сколько месяцев прошло с вступления заёмщика в должность и внесем данные в переменную YOJ
YOJ = (current_date.year - given_date1.year) * 12 + (current_date.month - given_date1.month)
INC = st.text_input('**Сколько Вы зарабатываете в месяц?**')
DEBT = st.text_input('**Сколько в месяц Вы тратите на погашение других кредитов?**')
#по доходу и тратам на кредиты посчитаем DEBTINC - отношение долга к доходу
try:
    DEBTINC=float(DEBT)/float(INC)
except:
    DEBTINC=0

import joblib
#загрузим сохраненную модель классификации
pipeline = joblib.load('pipeline_file.pkl')
df = pd.read_csv('data.csv')
image = Image.open('star.png').resize((270, 300))
#импортируем функцию для связи с внешними данными
from external_data_api import otvet
if st.button('Рассчитать'):
    with st.spinner('Пожалуйста, подождите...'):
        #в новый ряд поставим значения, которые ввел пользоеватель
        new_row = {'LOAN': LOAN,'MORTDUE': MORTDUE,'VALUE': VALUE, 'REASON': REASON,
           'JOB': JOB, 'YOJ': YOJ, 'DEROG': DEROG,
           'DELINQ': DELINQ, 'CLAGE': CLAGE, 'NINQ': NINQ,
           'CLNO': CLNO, 'DEBTINC': DEBTINC}
        new_row = pd.DataFrame(new_row, index=[0])
        new_row['REASON'] = new_row['REASON'].replace(['На обустройство дома', 'Для консолидации долга'], [0, 1])
        new_row['JOB'] = new_row['JOB'].replace(['Другое', 'В продажах', 'Офисный работник', 'Менеджер', 'Профессор', 'Работаю на себя'], 
                                [0, 1, 2, 3, 4, 5])
        #с помощью пайплайна, который содержит модель и imputer для заполнения пропущенных данных средними, выведем предсказание
        y_pred_proba = pipeline.predict_proba(new_row)
        time.sleep(7)
        #опционально можно вывести новый ряд, чтобы посмотреть, с какими значениями работает модель
        #st.write(new_row)
        #функция ответ выдает с учетом вероятности дефолта и курса доллара итоговый ответ кредитного конвейера
        if otvet(y_pred_proba)=='Вам предварительно одобрен кредит!':
            st.write('Вам предварительно одобрен кредит!')
            st.image(image)
            st.balloons()
            st.write(y_pred_proba)
        else:
            st.write('Благодарим за обращение, но пока мы не можем оформить вам кредит(')
            st.write(y_pred_proba)
