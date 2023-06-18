from fastapi_cache.decorator import cache
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from celery import Celery
from celery.schedules import crontab
from forecast.forcast import ForcastRepoitory
import pandas as pd

celery = Celery("train_model", broker=f"redis://redis:6379/0")

# @cache(3600)
def culculate_sarima(train, must = None):
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit()
    return model_fit


# @cache(3600)
def culculate_arima(train, must = None):
    model = ARIMA(train, order=(1, 1, 1))
    model_fit = model.fit()
    return model_fit

@celery.task
def model_culc():
    df_a = ForcastRepoitory.get_clean_data(df1, df2)[0]
         # Преобразование колонки 'Время' в формат времени
    df_a['Время'] = pd.to_datetime(df_a['Время'])
    df_a.fillna(method='ffill', inplace=True)
    df_a['Автомобилей'] = pd.to_numeric(df_a['Автомобилей'], errors='coerce')
    df_a['Автомобилей'].dropna(inplace=True)
    train = df_a['Автомобилей'][:int(0.8*(len(df_a)))]
    culculate_arima(train, must= 1)
    culculate_sarima(train, must= 1)

celery.conf.beat_schedule = {
    'execute-pereodic-task': {
        'task': 'utils.email.spend_money_for_tarif',
        'schedule': crontab(hour=22, minute=00),
    },
}
