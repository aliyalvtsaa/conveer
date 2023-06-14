#функция для обращения к внешним данным
def otvet(y_pred_proba):
    from datetime import datetime, timedelta
    import requests
    import currencyapicom
    #по currencyapi и ключу доступа ополучим курс доллара (аккуратно: у нас ограниченное количество токеновв)
    client = currencyapicom.Client('qVc9LBFXf4ScZGLMR6YY3vxaQq03htsgFW4VFk5I')
    #получим курс за позавчера
    day_before_yesterday = datetime.now() - timedelta(days=2)
    day_before_yesterday_str = day_before_yesterday.strftime('%Y-%m-%d')
    result1 = client.historical(day_before_yesterday_str)
    data1=result1['data']['EUR']['value']
    #и за вчера
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    result2 = client.historical(yesterday_str)
    data2=result1['data']['EUR']['value']
    #сравним: если вчерашний курс больше позавчерашнего, то курс доллара стал выше, отметим "доллар укрепляется"
    if data2-data1>0:
        itog='доллар укрепляется'
    else:
        itog='доллар не укрепляется'
    #если доллар укрепляется, повысим порог до вероятности дефолта 0.55
    if itog=='доллар укрепляется' and y_pred_proba[0][1]<0.55:
        result='Вам предварительно одобрен кредит!'
        #если доллар не укрепляется, понизим порог до верроятности 0.45
    elif itog=='доллар не укрепляется' and y_pred_proba[0][1]<0.45:
        result='Вам предварительно одобрен кредит!'
    else:
        #если сочетание вероятности и данных по укреплению доллара не подходит ни под один из вариантов выше, не будем выдавать кредит
        result='Благодарим за обращение, но пока мы не можем оформить вам кредит('
    return result
    

