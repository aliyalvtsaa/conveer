df2 = pd.DataFrame(columns=['LOAN', 'MORTDUE', 'VALUE', 'REASON', 'JOB', 'YOJ', 'DEROG',
                            'DELINQ', 'CLAGE', 'NINQ', 'CLNO', 'DEBTINC'])
df2['REASON'] = df2['REASON'].replace(['На обустройство дома', 'Для консолидации долга'], [0, 1])
df2['JOB'] = df2['JOB'].replace(['Другое', 'В продажах', 'Офисный работник', 'Менеджер', 'Профессор', 'Работаю на себя'], 
                                [0, 1, 2, 3, 4, 5])
