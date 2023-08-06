import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class deteccion_correlaciones:
    def __init__(self, archivo):
        self.df = pd.read_csv(archivo)
        self.numericas = self.df.select_dtypes(['int64', 'float'])
        self.variables_corr_para_modelar = self.numericas.drop(columns = [(i) for i in self.numericas.columns if self.numericas[i].isin([-1,1]).all() | self.numericas[i].isin([0,1]).all()][0])
    
    def eliminacion_variables_correlacionadas(self):
        corr_matrix = self.variables_corr_para_modelar.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))  # cogemos el triángulo superior para que solamente nos elimine 1 variable.
        to_drop = [column for column in upper.columns if any(upper[column] > 0.8)]
        nuevo_df = self.df.drop(columns = to_drop)
        return nuevo_df
     
    def variables_mas_importantes(self):
        corr_matrix2 = self.numericas.corr().abs()
        upper2 = corr_matrix2.where(np.triu(np.ones(corr_matrix2.shape), k=1).astype(np.bool))
        variable_objetivo = [(i) for i in self.numericas.columns if self.numericas[i].isin([-1,1]).all() | self.numericas[i].isin([0,1]).all()][0]
        
        variables_mas_importantes = []
        corr_clase = upper2[variable_objetivo]
        
        for i in range(0,upper2.shape[0]): 
                if (corr_clase[i] > 0.3):     
                        variables_mas_importantes.append(corr_clase.index[i])
        return variables_mas_importantes

    # y es el valor que hay que meter dependiendo de las variables que se tenga 
    def histogramas(self,datos): #datos tiene que ser el resultado de la función variables_mas_importantes 
        df_histogramas = self.df[datos]
        df_histogramas.hist(bins = 100, color='#5485E6',figsize=(25, 10))


    def correlaciones_a_eliminar(self):
        fig, ax = plt.subplots(figsize=(32,16))
        correlation_matrix_0 = self.variables_corr_para_modelar.corr()
        sns.heatmap(correlation_matrix_0, annot=True, cmap='PiYG') 
    
    def correlaciones_variables_importantes(self):
        fig, ax = plt.subplots(figsize=(32,16))
        correlation_matrix_1 = self.numericas.corr()
        sns.heatmap(correlation_matrix_1, annot=True, cmap='PiYG')