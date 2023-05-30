def otvet(y_pred_proba):
    from datetime import datetime, timedelta
    import requests
    import xml.etree.ElementTree as ET
    # сегодняшняя дата
    today = datetime.today()
    # дата 35 дней назад
    start_date = today - timedelta(days=35)
    # создаем список дат в date_list
    date_list = []
    current_date = start_date
    while current_date <= today:
        date_string = current_date.strftime("%d/%m/%Y")
        date_list.append(date_string)
        current_date += timedelta(days=1)
    #теперь получим цены
    prices=[]
    for day_today in date_list:
        r=requests.get("http://www.cbr.ru/scripts/XML_daily.asp?", params={"date_req":day_today})
        root = ET.fromstring(r.content)
        for valute in root.iter('Valute'):
            name = valute.find('Name').text
            if name == "Доллар США":
                desired_valute = valute.find('Value').text
                desired_valute = desired_valute.replace(",", ".")
        prices.append(float(desired_valute))

    # наш бенчмарк
    benchmark = max(prices)
    # средее
    average = sum(prices) / len(prices)
    # десять процентов
    threshold = 0.1
    if abs(average/benchmark - 1)<0.1:
        itog='рубль укрепляется'
    else:
        itog='рубль не укрепляется'

    if itog=='рубль укрепляется' and y_pred_proba[0][1]<0.45:
        result='Вам предварительно одобрен кредит!'
    elif itog=='рубль не укрепляется' and y_pred_proba[0][1]<0.55:
        result='Вам предварительно одобрен кредит!'
    else:
        result='Благодарим за обращение, но пока мы не можем оформить вам кредит('
    return result
    

