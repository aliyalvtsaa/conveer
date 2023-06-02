import streamlit as st

import streamlit.components.v1 as components
components.html(
    """
    <!-- Yandex.Metrika counter --> <script type="text/javascript" > (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)}; m[i].l=1*new Date(); for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }} k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}) (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym"); ym(93814389, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true }); </script> <noscript><div><img src="https://mc.yandex.ru/watch/93814389" style="position:absolute; left:-9999px;" alt="" /></div></noscript> <!-- /Yandex.Metrika counter -->
    """,
    height=600,
)

import datetime
from datetime import date
import time
from datetime import datetime
import streamlit as st
from PIL import Image

        
#напишем приветствие
st.header('Здравствуйте!')
st.subheader('На этой страничке вы можете воспользоваться нашей учебной версией кредитного конвейера.')
st.write('Введите доступные вам данные, чтобы оценить свои шансы на получение кредита')

#создадим интерфейс для ввода данных

LOAN=0
CLNO=0
VALUE=0
REASON=0
JOB=0
YOJ=0
CLAGE=0
DEROG=None
DELINQ=None
DEBTIN=None
NINQ=None
MORTDUE=None



LOAN = st.slider('На какую сумму в вы хотите взять кредит? (LOAN)', 0, 100000, 0, 1000)
CLNO = st.slider('Сколько у вас кредитов на данный момент? (CLNO)', 0, 100,0, 1)
VALUE = st.slider('На сколько вы оцениваете свою собственность? (VALUE)',0, 1000000,0, 50000)
REASON = st.selectbox(
'Зачем вы берете кредит? (REASON)',
('На обустройство дома', 'Для консолидации долга'))
JOB = genre = st.radio(
"Кем вы работаете?",
('Менеджер', 'Офисный работник', 'В продажах', 'Профессор', 'Работаю на себя','Другое'))
given_date1 = st.date_input("Когда вы начали работать на текущей должности? (YOJ)", min_value= date(1923, 1, 1) )
#по дате посчитаем, сколько месяцев прошло с вступления заёмщика в должность
YOJ = (current_date.year - given_date.year) * 12 + (current_date.month - given_date.month)
current_date = datetime.now()
given_date = st.date_input("Когда вы взяли ваш самый давний кредит? (CLAGE)", min_value= date(1923, 1, 1) )
#по дате посчитаем, сколько месяцев прошло с получения самого давнего кредита
CLAGE = (current_date.year - given_date.year) * 12 + (current_date.month - given_date.month)
INC = st.text_input('Сколько вы зарабатываете в месяц? (INC)')
DEBT = st.text_input('Сколько в месяц вы тратите на погашение других кредитов? (DEBT)')
try:
    DEBTINC=float(DEBT)/float(INC)
except:
    DEBTINC=0


import joblib
#загрузим сохраненную модель классификации
pipeline = joblib.load('pipeline_file.pkl')

import pandas as pd
# создадим пустой датасет и добавим в него строку с нашими данными
df2 = pd.DataFrame(columns=['LOAN', 'MORTDUE', 'VALUE', 'REASON', 'JOB', 'YOJ', 'DEROG',
                            'DELINQ', 'CLAGE', 'NINQ', 'CLNO', 'DEBTINC'])

new_row = {'LOAN': LOAN,'VALUE': VALUE, 'MORTDUE': MORTDUE, 'REASON': REASON,
           'JOB': JOB, 'YOJ': YOJ, 'DEROG': DEROG,
           'DELINQ': DELINQ, 'CLAGE': CLAGE, 'NINQ': NINQ,
           'CLNO': CLNO, 'DEBTINC': DEBTINC}
new_row = pd.DataFrame(new_row, index=[0])
df2 = pd.concat([df2, new_row], ignore_index=True)
df2['REASON'] = df2['REASON'].replace(['На обустройство дома', 'Для консолидации долга'], [0, 1])
df2['JOB'] = df2['JOB'].replace(['Другое', 'В продажах', 'Офисный работник', 'Менеджер', 'Профессор', 'Работаю на себя'], 
                                [0, 1, 2, 3, 4, 5])
y_pred_proba = pipeline.predict_proba(df2)
image = Image.open('money.png').resize((300, 200))

#импортируем функцию для связи с внешними данными
from my_functions import otvet
if st.button('Рассчитать'):
    with st.spinner('Пожалуйста, подождите...'):
        time.sleep(7)
        st.write(df2)
        if otvet(y_pred_proba)=='Вам предварительно одобрен кредит!':
            st.write('Вам предварительно одобрен кредит!')
            st.image(image)
            st.balloons()
            st.write(y_pred_proba)
        else:
            st.write('Благодарим за обращение, но пока мы не можем оформить вам кредит(')
            st.write(y_pred_proba)
