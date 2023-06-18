import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from train.delay_c import culculate_arima, culculate_sarima
import json

class ForcastRepoitory():

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
    
    def get_forcats_cars(lat = None,lon = None):
        df1 = 1
        df2 = 2
        df_a = ForcastRepoitory.get_clean_data(df1, df2)[0]
         # Преобразование колонки 'Время' в формат времени
        df_a['Время'] = pd.to_datetime(df_a['Время'])

        df_a.fillna(method='ffill', inplace=True)
        decomp = seasonal_decompose(df_a['Автомобилей'], model='additive', period=288)

        result = adfuller(df_a['Автомобилей'])

        df_a['Автомобилей'] = pd.to_numeric(df_a['Автомобилей'], errors='coerce')
        df_a['Автомобилей'].dropna(inplace=True)
        rolling_mean = df_a['Автомобилей'].rolling(window=10).mean()
        

        # Вычитание скользящего среднего из исходного временного ряда
        df_minus_rolling_mean = df_a['Автомобилей'] - rolling_mean
        df_minus_rolling_mean.dropna(inplace=True)

        result = adfuller(df_minus_rolling_mean)

        train = df_a['Автомобилей'][:int(0.8*(len(df_a)))]
        test = df_a['Автомобилей'][int(0.8*(len(df_a))):]

        # Arima model
        model_fit = culculate_arima(train)
        forecast_values = model_fit.forecast(len(test), alpha=0.0, return_conf_int=True)
        fc_series_arima = pd.Series(forecast_values, index=test.index)



        model_fit = culculate_sarima(train)

        forecast_values = model_fit.forecast(len(test), alpha=0.05, return_conf_int=True)
        fc_series_sarima = pd.Series(forecast_values, index=test.index)

        # Установка 'Время' как индекс
        df_a.set_index('Время', inplace=True)
        df_a = df_a.resample('5T').mean()
        df_a['Автомобилей'] = df_a['Автомобилей'].dropna()
        data = {
                'observed': df_a['Автомобилей'].tolist(),
                'trend': decomp.trend.tolist(),
                'seasonality': decomp.seasonal.tolist(),
                'residuals': decomp.resid.tolist(),
                'adf_statistic': result[0],
                'p_value': result[1],
                'rolling_mean': rolling_mean.tolist(),
                'adf_statistic_minus_mean': result[0],
                'p_value_minus_mean': result[1],
                'train': train.tolist(),
                'test': test.tolist(),
                'forecast_arima': fc_series_arima.tolist(),
                'forecast_sarima': fc_series_sarima.tolist()
            }

        # Convert the data to JSON
        json_data = json.dumps(data)

        # Print or return the JSON data
        return json_data
