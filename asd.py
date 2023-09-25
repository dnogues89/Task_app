import pandas as pd

df = pd.read_excel('/Users/dnogues/Downloads/TiposDocOperacion.xlsx')

for columna, datos in df.iterrows():
    print(datos[1])
    print()