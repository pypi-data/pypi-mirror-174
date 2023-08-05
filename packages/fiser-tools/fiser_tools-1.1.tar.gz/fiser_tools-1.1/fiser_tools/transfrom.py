import numpy as np
import pandas as pd
    
def fis_time_elements(df):
    """
    Extracción de los elementos para un DataFrame con la fecha indexada y convertidos
    en nuevas columnas
    """
    month = df.index.month
    year = df.index.year
    day = df.index.day
    minute = df.index.minute
    hour = df.index.hour
    
    return(pd.DataFrame({'month':month,'year':year,'day':day,'minute':minute,'hour':hour}))
    
def fis_time_lags(df, num_lags = 7):
    """
    Crea nuevas columnas en un DataFrame con los lags num_lags definidos (7 default)
    """
    #Crea el objeto data frame
    lags = pd.Dataframe()
    #Crear todos los lags
    for cada in range(1, num_lags):
        lags['lag_'+str(cada)] = df.shift(cada).iloc[:0]
    return(lags)

def fis_time_rolling_mean(df, num_periodos = 7):
    """
    Crea num_periodos nuevas columnas en un DataFrame con la media movil de 1 a num_periodos
    """
    mm = pd.DataFrame()
    for cada in range (1, num_periodos):
        mm['rm_'+str(cada)] = df.shift(1).rolling(cada).mean().iloc[:,0]
    return(mm)
    
#Función para agrupar categorías raras en 'OTROS'
def fis_group_cat_unknown(variable, criterio = 0.05,nombre='OTHERS'):
    """
    A partir del porcentaje de recurrencia (criterio) se agrupan N categorias en 1 sola nombre = 'OTHERS'
    """
    #Calcula las frecuencias
    frecuencias = variable.value_counts(normalize=True)
    #Identifica las que están por debajo del criterio
    temp = [cada for cada in frecuencias.loc[frecuencias < criterio].index.values]
    #Las recodifica en 'OTROS'
    temp2 = np.where(variable.isin(temp),nombre,variable)
    #Devuelve el resultado
    return(pd.Series(temp2))