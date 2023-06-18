from fastapi_cache.decorator import cache
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from celery import Celery
from celery.schedules import crontab
import pandas as pd

celery = Celery("delay_c", broker=f"redis://redis:6379/0")


def get_clean_data(df1_q = None, df_q = None) -> pd.DataFrame:
        if df1_q is not None  or df_q is not None:
            df1 = pd.read_csv("models/230 old december.csv")
            df = pd.read_csv("models/230 old march.csv")
        else:
            df1 = pd.read_csv("clean/normalized_data/231_december_upcoming_lanes.csv")
            df = pd.read_csv("clean/normalized_data/237_march_upcoming_lanes.csv")
        df1_just_numb = df1.loc[df1.index % 5 == 0]
        df1_just_numb = df1_just_numb.iloc[:5311]
        df_just_numb = df.loc[df.index % 5 == 0]
        return df_just_numb, df1_just_numb

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
    df1 = 1
    df2 = 2
    df_a = get_clean_data(df1, df2)[0]
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
