def otvet(y_pred_proba):
    from datetime import datetime, timedelta
    import requests
    import currencyapicom
    client = currencyapicom.Client('qVc9LBFXf4ScZGLMR6YY3vxaQq03htsgFW4VFk5I')
    day_before_yesterday = datetime.now() - timedelta(days=2)
    day_before_yesterday_str = yesterday.strftime('%Y-%m-%d')
    result1 = client.historical(day_before_yesterday_str)
    data1=result1['data']['EUR']['value']
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    result2 = client.historical(yesterday_str)
    data2=result1['data']['EUR']['value']
    if data2-data1>0:
        itog='доллар укрепляется'
    else:
        itog='доллар не укрепляется'

    if itog=='доллар укрепляется' and y_pred_proba[0][1]<0.55:
        result='Вам предварительно одобрен кредит!'
    elif itog=='доллар не укрепляется' and y_pred_proba[0][1]<0.45:
        result='Вам предварительно одобрен кредит!'
    else:
        result='Благодарим за обращение, но пока мы не можем оформить вам кредит('
    return result
    

