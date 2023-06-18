import pickle
import numpy as np
import pandas as pd
import math
from geopy.distance import geodesic
from estates.schemas import real_EstateBase


city_center_coordinates = [55.7522, 37.6156]

# rf_model_path = 'models/rf_model.pkl'
xgb_model_path = 'models/xgb_model.pkl'


def get_azimuth(latitude, longitude):
    rad = 6372795
    
    llat1 = city_center_coordinates[0]
    llong1 = city_center_coordinates[1]
    llat2 = float(latitude)
    llong2 = float(longitude)
    
    lat1 = llat1*math.pi/180.
    lat2 = llat2*math.pi/180.
    long1 = llong1*math.pi/180.
    long2 = llong2*math.pi/180.

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
    x = sl1*sl2+cl1*cl2*cdelta
    ad = math.atan2(y,x)

    x = (cl1*sl2) - (sl1*cl2*cdelta)
    y = sdelta*cl2
    z = math.degrees(math.atan(-y/x))

    if (x < 0):
        z = z+180.

    z2 = (z+180.) % 360. - 180.
    z2 = - math.radians(z2)
    anglerad2 = z2 - ((2*math.pi)*math.floor((z2/(2*math.pi))) )
    angledeg = (anglerad2*180.)/math.pi

    return round(angledeg, 2)


# Вычисляет среднюю абсолютную процентную ошибку
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# Вычисляет медианную абсолютную процентную ошибку
def median_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.median(np.abs((y_true - y_pred) / y_true)) * 100


def predict_cost(flat: pd.DataFrame):
    xgb_model = pickle.load(open(xgb_model_path, 'rb'))
    # rf_model = pickle.load(open(rf_model_path, 'rb'))

    flat['distance'] = list(
        map(lambda x, y: geodesic(city_center_coordinates, [x, y]).meters, flat['latitude'], flat['longitude']))
    flat['azimuth'] = list(map(lambda x, y: get_azimuth(x, y), flat['latitude'], flat['longitude']))
    flat['distance'] = flat['distance'].round(0)
    flat['azimuth'] = flat['azimuth'].round(0)

    # Удаляем ненужные столбцы с широтой и долготой
    flat = flat.drop('latitude', axis=1)
    flat = flat.drop('longitude', axis=1)

    # rf_prediction_flat = rf_model.predict(flat).round(0)
    xgb_prediction_flat = xgb_model.predict(flat).round(0)

    return xgb_prediction_flat *flat['totalArea'][0]

def predict(estate: real_EstateBase) -> int:
    flat = pd.DataFrame({
                     'wallsMaterial': [estate.wallsMaterial],
                     'floorNumber': [estate.floorNumber],
                     'floorsTotal': [estate.floorsTotal],
                     'totalArea':[estate.totalArea],
                     'kitchenArea':[estate.kitchenArea],
                     'latitude':[float(estate.latitude)],
                     'longitude':[float(estate.longitude)]
                     })
    return predict_cost(flat)
