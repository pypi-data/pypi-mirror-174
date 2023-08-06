import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
from yellowbrick.classifier import discrimination_threshold
from sklearn.metrics import PrecisionRecallDisplay

def fis_metric_compute(real, scoring, umbral=0.5,graf_recall=False,graf_umbral=False,model=None,x=None,y=None):
    """
    umbral --> threshold de % de probabilidad a partir de la cual es True (1)  
    
    graf_recall(True)
    -----------------
    model --> el objeto sklearn model() instanciado
    x --> variables predictoras (todas)
    y --> target (todas)

    graf_umbral (True)
    ------------------
    model --> el objeto sklearn model() instanciado
    x --> variables predictoras (todas)
    y --> target (todas)
    """
    #CALCULAR LA DECISION SEGUN EL UMBRAL
    predicho = np.where(scoring > umbral,1,0)
    umbral_100 = umbral * 100
    
    #CALCULAR TODAS LAS MÉTRICAS
    conf = confusion_matrix(real,predicho)

    tn, fp, fn, tp = conf.ravel()

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    F1 = 2 * (precision * recall) / (precision + recall)

    #IMPRIMIR RESULTADOS
    print('====================  Metric Report  ==== Threshold {:.2f} % ========='.format(umbral_100))
    sns.heatmap(conf,annot=True, cmap="YlGnBu" ,fmt='g') 
    plt.tight_layout() 
    plt.title('Confusion matrix') 
    plt.ylabel('Current') 
    plt.xlabel('Predicted')
    plt.show()
    
    print('Precision:',round(precision,3))
    print('Recall   :',round(recall,3))
    print('F1       :',round(F1,3))
    if graf_recall:
        PrecisionRecallDisplay.from_estimator(model,x,y)
        plt.show()    
    if graf_umbral:
        discrimination_threshold(model,x,y, exclude = 'queue_rate')
        plt.show()
    print('\n====================================================================')
    
def fis_metric_max_roi(real,scoring, salida = 'grafico',itn=0,ifp=-15,ifn=-85,itp=85):
    """
    salida <> "grafico" devuelve valor numérico max ROI, para automatizaciones
    #DEFINIMOS LA MATRIZ DE IMPACTO
    itn   #true negatvie
    ifp   #false positive
    ifn   #false negative
    itp   #true positive
    """
    #DEFINIMOS LA MATRIZ DE IMPACTO
    ITN = itn   #true negatvief1s
    IFP = ifp   #false positive
    IFN = ifn   #false negative
    ITP = itp   #true positive
    
    #DEFINIMOS LA FUNCION DEL VALOR ESPERADO
    def valor_esperado(matriz_conf):
        TN, FP, FN, TP = conf.ravel()
        VE = (TN * ITN) + (FP * IFP) + (FN * IFN) + (TP * ITP)
        return(VE)
    
    #CREAMOS UNA LISTA PARA EL VALOR ESPERADO
    ve_list = []
    
    #ITERAMOS CADA PUNTO DE CORTE Y RECOGEMOS SU VE
    for umbral in np.arange(0,1,0.01):
        predicho = np.where(scoring > umbral,1,0) 
        conf = confusion_matrix(real,predicho)
        ve_temp = valor_esperado(conf)
        ve_list.append(tuple([umbral,ve_temp]))
        
    #DEVUELVE EL RESULTADO COMO TGRAFICO O COMO EL UMBRAL ÓPTIMO
    df_temp = pd.DataFrame(ve_list, columns = ['threshold', 'expected_value'])
    if salida == 'grafico':
        solo_ve_positivo = df_temp[df_temp.expected_value > 0]
        plt.figure(figsize = (12,6))
        sns.lineplot(data = solo_ve_positivo, x = 'threshold', y = 'expected_value')
        plt.xticks(solo_ve_positivo.threshold, fontsize = 14)
        plt.yticks(solo_ve_positivo.expected_value, fontsize = 12);        
    else:    
        return(df_temp.iloc[df_temp.expected_value.idxmax(),0])