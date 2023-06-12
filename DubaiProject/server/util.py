import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_district_names():
    return __locations

def get_estimated_price(location,bedroom,bath,sqft):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    
    x = np.zeros(len(__data_columns))
    x[0] = bedroom
    x[1] = bath
    x[2] = sqft
    if loc_index >= 0:
        x[loc_index] = 1
    
    x = x.reshape(1,-1)
    return round(__model.predict(x)[0],2)

def load_saved_artifacts():
    
    print('Loading artifact...')
    global __data_columns
    global __locations
    
    ##with open('.artifacts\columns.json', 'rb')  # uncoment this line
    with open(r"C:\Users\Polina\Desktop\Python\DubaiProject\server\artifacts\columns.json",'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
        
    global __model
    #with open('.artifacts\Dubai_properties_prices_model.pickle', 'rb') #uncoment this line of code    
    with open(r'C:\Users\Polina\Desktop\Python\DubaiProject\server\artifacts\Dubai_properties_prices_model.pickle','rb') as f:
        __model = pickle.load(f)
    print('Loading saved artifacts...done')
    
if __name__ == '__main__':
    load_saved_artifacts()
    print(get_district_names())
    print(get_estimated_price('dubai sports city',3,3,1500))
            