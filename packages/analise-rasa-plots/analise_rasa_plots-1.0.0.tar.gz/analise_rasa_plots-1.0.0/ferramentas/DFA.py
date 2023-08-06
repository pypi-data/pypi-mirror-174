import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import seaborn as sns

class DFA: 
    
    @property
    def listing(self):
        return None
    
    @listing.setter
    def listing(self,df):
        self.listaint, self.listafloat, self.listaobj, self.listadatetime, self.listadeltadatetime, self.listacategory, self.listastring, self.outros = [], [], [], [], [], [], [], []
        for obj in df.columns:
            if df[obj].dtype == 'int64':
                self.listaint.append(obj)
            elif df[obj].dtype == 'int32':
                self.listaint.append(obj)
            elif df[obj].dtype == 'float64':
                self.listafloat.append(obj)
            elif df[obj].dtype == 'float32':
                self.listafloat.append(obj)
            elif df[obj].dtype == 'object':
                self.listaobj.append(obj)
            elif df[obj].dtype == 'datetime64':
                self.listadatetime.append(obj)
            elif df[obj].dtype == 'timedelta64':
                self.listadeltadatetime.append(obj)
            elif df[obj].dtype == 'category':
                self.listacategory.append(obj)
            elif df[obj].dtype == str:
                self.listastring.append(obj)
            else:
                self.outros.append(obj)
    def Dicting(self):
        DictingSeriesValues = [self.listaint,self.listafloat,self.listadatetime,self.listadeltadatetime,self.listacategory,self.listastring,self.listaobj,self.outros]
        DictingSeriesKeys = ['listaint','listafloat','listadatetime','listadeltadatetime','listacategory','listastring','object','outros']
        self._keysvalues = dict(zip(DictingSeriesKeys,DictingSeriesValues))
        return self._keysvalues

def Normalize(df):
    datasN = MinMaxScaler().fit_transform(df)
    datasN = pd.DataFrame(datasN)
    return datasN

def PlotBox(df):
    fig = plt.figure(figsize =(10,7))
    ax = fig.add_subplot(111)    
    bp = ax.boxplot(df, patch_artist = True, vert = 0)
    ax.set_yticklabels(df.columns)
    plt.title("Box plots")
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()  
    plt.show()
    
def PlotKde(df):
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.kdeplot(data=df, ax=ax)

def AnalisePreliminar(df,/,IncludeInt=False,IncludeFloat=False,Kind=None,NormalizeDf=False, Comments=False): 
    poss=['boxplot','kde']
    res = []
    if isinstance(df, pd.DataFrame):
        return "Parâmetros insuficientes. Forneça um ou mais dataframes numa lista no primeiro argumento. O restante dos argumentos são IncludeInt,IncludeFloat,NormalizeDf, Comments,Kind"
    res.append(Kind)
    if not (res[0] in poss):
        return f"especifique o Kind - {poss}"
    
    try:         
        if (IncludeInt or IncludeFloat):
            iterador = DFA()
            n = 0
            for obj in df:
                iterador.listing = obj      
                datas = []        
                if IncludeInt:
                    datas.extend(iterador.listaint)
                    if (len(iterador.listaint)==0) and Comments:
                        print("Não há colunas de números inteiros nas colunas do df.")
                if IncludeFloat:
                    datas.extend(iterador.listafloat)
                    if (len(iterador.listafloat)==0) and Comments:
                        print("Não há colunas de números float nas colunas do df.")
                Ndatas = obj[datas]
                if NormalizeDf:
                    Cols = Ndatas.columns
                    Ndatas = Normalize(Ndatas)
                    Ndatas.columns=Cols
                n += 1
                
                if 'boxplot' in res[0]:
                    PlotBox(Ndatas)
                if 'kde' in res[0]:
                    PlotKde(Ndatas)
        else:
            print("Passe um ou mais argumentos bool: IncludeInt e IncludeFloat. \nTambém há a função de normalização para ajudar na visualização dos dados.")
    except:
        print("Um erro ocorreu.")    
