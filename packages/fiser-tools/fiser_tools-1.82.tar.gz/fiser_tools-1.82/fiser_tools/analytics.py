import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import statsmodels.tsa.stattools as sts

def fis_variable_frecuency(df_cat):
    """
    Salida en formato DataFrame de la frecuencia de las variables categoricas en %
    """
    resultado = df_cat.apply(lambda x: x.value_counts(normalize = True)).T.stack()\
                .to_frame().reset_index()\
                .rename(columns={'level_0':'Variable','level_1':'Valor',0: "Frecuencia"})\
                .sort_values(by = ['Variable','Frecuencia'])
    return(resultado)
    
def fis_all_continous_statistics(df_cont):
    """
    Salida en formato DataFrame de todos los estadísticos de variable contínua + mediana
    """
    #Calculamos describe
    estadisticos = df_cont.describe().T
    #Añadimos la mediana
    estadisticos['median'] = df_cont.median()
    #Reordenamos para que la mediana esté al lado de la media
    estadisticos = estadisticos.iloc[:,[0,1,8,2,3,4,5,6,7]]
    #Lo devolvemos
    return(estadisticos)
    
def fis_eda_categoric_graph(df_cat):
    """
    Salida gráfica de todas las variables categoricas para exploration data analysis
    """
    #Calculamos el número de filas que necesitamos
    from math import ceil
    filas = ceil(df_cat.shape[1] / 2)

    #Definimos el gráfico
    f, ax = plt.subplots(nrows = filas, ncols = 2, figsize = (16, filas * 6))

    #Aplanamos para iterar por el gráfico como si fuera de 1 dimensión en lugar de 2
    ax = ax.flat 

    #Creamos el bucle que va añadiendo gráficos
    for cada, variable in enumerate(df_cat):
        df_cat[variable].value_counts().plot.barh(ax = ax[cada])
        ax[cada].set_title(variable, fontsize = 12, fontweight = "bold")
        ax[cada].tick_params(labelsize = 12)
    plt.tight_layout()
    plt.show()
        
def fis_eda_continous_graph(df_cont,mode='density'):
    """
    Salida gráfica de todas las variables continuas para exploration data analysis
    """
    #Calculamos el número de fila que necesitamos
    from math import ceil
    filas = ceil(df_cont.shape[1] / 2)

    #Definimos el gráfico
    f, ax = plt.subplots(nrows = filas, ncols = 2, figsize = (16, filas * 6))

    #Aplanamos para iterar por el gráfico como si fuera de 1 dimensión en lugar de 2
    ax = ax.flat 

    #Creamos el bucle que va añadiendo gráficos
    for cada, variable in enumerate(df_cont):
        if mode=='density':
            df_cont[variable].plot.density(ax = ax[cada])
        else:
            df_cont[variable].plot(ax = ax[cada])
        ax[cada].set_title(variable, fontsize = 12, fontweight = "bold")
        ax[cada].tick_params(labelsize = 12)
    plt.tight_layout()
    plt.show()
        

def fis_preprocessing_strong_corr(df,lim_inf = 0.3, lim_sup = 1,drop_dupli=True):
    """
    Extracción de variables correlacionadas a partir de un umbral lim_inf y tope lim_sup
    """
    #Calcula la matriz de correlación
    c = df.corr().abs()
    #Lo pasa todo a filas
    c= c.unstack()
    #Pasa el índice a columnas y le pone nombres
    c = pd.DataFrame(c).reset_index()
    c.columns = ['var1','var2','corr']
    #A dataframe, filtra limites y ordena en descendiente
    c = c.loc[(c['corr'] > lim_inf) &  (c['corr'] < lim_sup),:].sort_values(by = 'corr', ascending=False)
    #Desduplica las correlaciones (o no si drop_dupli es False)
    c = c if drop_dupli == False else c.drop_duplicates(subset = ['corr'])
    #Devuelve la salida
    return(c)
    
def fis_preprocessing_ranking_mi(mutual_selector, predictors_df, modo = 'tabla'):
    """
    Salida Mejorada de la salida from sklearn.feature_selection import mutual_info_classif
    """
    #Maqueta el ranking
    ranking_mi = pd.DataFrame(mutual_selector, index = predictors_df.columns).reset_index()
    ranking_mi.columns = ['variable','importancia_mi']
    ranking_mi = ranking_mi.sort_values(by = 'importancia_mi', ascending = False)
    ranking_mi['ranking_mi'] = np.arange(0,ranking_mi.shape[0])
    #Muestra la salida
    if modo == 'tabla':
        return(ranking_mi)
    else:
        g = ranking_mi[0:15].importancia_mi.sort_values().plot.barh()
        g.set_yticklabels(ranking_mi[0:15].sort_values(by = 'importancia_mi').variable)
        return(g)

def fis_preprocessing_ranking_per(predictoras,rfe_ranking):
    """
    Salida Mejorada de la salida from sklearn.feature_selection import RFECV
    """
    rank_rfe = pd.DataFrame({'variable': predictoras.columns, 'ranking_rfe': rfe_ranking}).sort_values(by = 'ranking_rfe')
    return(rank_rfe)
 
def fis_preprocessing_ranking_per(predictoras,permutacion,modo='tabla'):
    """
    Salida Mejorada de la salida from sklearn.inspection import permutation_importance
    """
    ranking_per = pd.DataFrame({'variable': predictoras.columns, 'importancia_per': permutacion.importances_mean}).sort_values(by = 'importancia_per', ascending = False)
    ranking_per['ranking_per'] = np.arange(0,ranking_per.shape[0])
    if modo == 'tabla':
        return(ranking_per)
    else:
        ranking_per.set_index('variable').importancia_per.sort_values().plot.barh(figsize = (8,10));
    
def fis_preprocessing_ranking_tot(rank_mi, rank_rfe,rank_per,modo='tabla'):
    """
    Comparativa de todos los rankings (mi, rfe, permutation) grafica y por tabla
    """
    ranking_tot = pd.merge(pd.merge(rank_mi,rank_rfe),rank_per)
    ranking_tot['puntos'] = ranking_tot.ranking_mi + ranking_tot.ranking_rfe + ranking_tot.ranking_per
    ranking_tot.sort_values(by = 'puntos', inplace=True)
    ranking_tot['ranking_tot'] = range(0,len(ranking_tot.variable))
    if modo == 'tabla':
        return(ranking_tot)
    else:
        ranking_tot.set_index('variable').puntos.sort_values(ascending = False).plot.barh(figsize = (8,10));
        
def fis_outliers_standard_desv(variable, x = 4):
    """
    Dada una variable sacamos los índices de un Dataframe para aquellos registors que su valor 
    esté en un umbral de la media mas/menos x veces la desviación estándard de la muestra
    por defecto es 4 veces.
    """
    #sacamos los nulos por ahora
    variable = variable.dropna()
    #calculamos los límites
    media = np.mean(variable)
    sd = np.std(variable)
    umbral = sd * x
    lim_inf = media - umbral
    lim_sup = media + umbral
    #encontramos los índices de los que están fuera de los límites
    indices = [indice for indice,valor in variable.items() if valor < lim_inf or valor > lim_sup]
    return(indices)
    
# Invirtiendo la transformación
def fis_TS_invert_transformation(X_train, pred):
    """
    Los pronósticos se generan en la escala de los datos de entrenamiento utilizados por el modelo, es decir, son datos transformados. 
    Entonces, para volver a ponerlos en su escala original, necesitamos des-diferenciarlos.
    La forma de invertir la diferenciación es sumar estas diferencias consecutivamente al número base. 
    Una forma sencilla de hacerlo es determinar primero la suma acumulada y luego sumarla al número base.
    Este proceso se puede revertir agregando la observación en el paso de tiempo anterior al difference value. 
    inverted(ts) = differenced(ts) + observation(ts-1)
    
    Retrocede una aplicación de:
    ----------------------------
    X_train_transformed=X_train.diff().dropna()
    X_train_transformed.head()
    """
    forecast = pred.copy()
    columns = X_train.columns
    for col in columns:
        forecast[str(col)+'_pred'] = X_train[col].iloc[-1] + forecast[str(col)+'_pred'].cumsum()
    return forecast
  

def fis_TS_grangers_causality_matrix(X_train_transformed, variables, test = 'ssr_chi2test', verbose=False,maxlag=15):
    """
    Causalidad de Granger (Wiener-Granger)
    
    Ejemplo:
    --------
    grangers_causality_matrix(X_train_transformed, variables = X_train_transformed.columns)
    """
    dataset = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in dataset.columns:
        for r in dataset.index:
            test_result = grangercausalitytests(X_train_transformed[[r,c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            if verbose: 
                print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            dataset.loc[r,c] = min_p_value
    dataset.columns = [var + '_x' for var in variables]
    dataset.index = [var + '_y' for var in variables]
    return dataset
  
def fis_TS_dickey_fuller_statistics(X_train):
    """
    Dickey Fuller test, para diferentes columnas de un DataFrame que correspondan a series temporales.
    Si los p-valores son mayores que 0.05, No se rechaza la hipótesis nula de que la serie no es estacionaria. 
    Habría que transformar los datos porque no se puede confirmar estacionariedad.
    """
    print('Augmented Dickey-Fuller Test:')
    print('=============================')
    for column in X_train.columns:
        result = sts.adfuller(X_train[column].values)
        print("Temporal Serie for: ",column)
        print('p-value: %f' % result[1])
        print('--------------------------------')