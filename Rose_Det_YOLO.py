#
#Autor : Alexander BolaÃ±o
#Modelo : Deteccion etapas de rosas con YOLO
#Fecha : Mayo 15 del 2019
#

import pandas as pd
from sklearn.model_selection import train_test_split
import cv2
import os
from tqdm import tqdm
from datetime import datetime,timedelta



directorio=os.getcwd()

print(directorio+'/darknet')

# Directorio principal
os.chdir(directorio+'/darknet')

# Descomprimimos en la carpeta darknet/data
os.system('unzip ../obj.zip -d ./data/')

# Copiamos archivos al directorio 'darknet/'
os.system('cp ../object.names ./data')
os.system('cp ../obj.data  ./data')
os.system('cp ../generate_train.py ./')
os.system('cp ../yolov3_custom_new.cfg ./cfg')

# Ejecutamos generate.py 
os.system('python generate_train.py') 

# Leemos archivo 
df=pd.read_csv('./data/train.txt',header=None)
data_train, data_test, labels_train, labels_test = train_test_split(df[0], df.index, test_size=0.20, random_state=42)

# Creamos el archivo train.txt
data_train=data_train.reset_index()
data_train=data_train.drop(columns='index')

with open("train.txt", "w") as outfile:
    for ruta in data_train[0]:
        outfile.write(ruta)
        outfile.write("\n")
    outfile.close()

# Creamos archivo test.txt
data_test=data_test.reset_index()
data_test=data_test.drop(columns='index')

with open("test.txt", "w") as outfile:
    for ruta in data_test[0]:
        outfile.write(ruta)
        outfile.write("\n")
    outfile.close()

#Eliminamos train.txt parcial
os.system('rm ./data/train.txt')

#Funcion guardar imagen
def save_img(input_img,imagen):
  import cv2

  image = cv2.imread(imagen)
  cv2.imwrite('pred_img/'+input_img,image)
  
  return  

lista_img=[imagenes for imagenes in os.listdir('../img_nuevas/') if imagenes.endswith('.jpg')==True]

# Ciclo para crear archivos de texto con predicciones
input_img=[]
filename=[]
for imagenes in tqdm(lista_img):
  input_img.append('../img_nuevas/'+imagenes)
  filename.append(imagenes.split('.jpg')[0]+'.txt')

# Enviamos archivos train.txt y test.txt a /data
os.system('cp train.txt ./data')
os.system('cp test.txt  ./data')

#Creamos carpeta de predicciones
os.mkdir('pred_img')
os.mkdir('results')

# Eliminamos archivos train.txt y test.txt a /data
os.system('rm train.txt ')
os.system('rm test.txt  ')

print('\n')
print('\n')
print('========================================|')
print('                                        |')
print('=== Proceso de prediccion de objetos ===|')
print('                                        |')
print('========================================|')
print('\n')
print('\n')

antes=datetime.now()

#Ciclo de ejecucion del modelo
for i in tqdm(range(len(input_img))):
  
  
  os.system('./darknet detector test data/obj.data cfg/yolov3_custom_new.cfg ../yolov3_custom_new_final.weights '+input_img[i]+' -thresh 0.47 > results/'+filename[i])
  name_img=input_img[i]
  name_img=name_img.split('img_nuevas/')[1]
  save_img(name_img,'predictions.jpg') 

print('\n')
print('\n')
print('===================================================|')
print('                                                   |')
print('===  Finalizado conteo de objetos detectados  =====|')
print('                                                   |')
print('== Revisar archivo Detecciones_modelo_YOLO.xlsx  ==|')
print('                                                   |')
print('===================================================|')
print('\n')
print('\n')

# Listamos archivos 

lista_file=[resultados for resultados in os.listdir('results/') if resultados.endswith('.txt')==True]

tipo=[]
puntaje=[]
name=[]

for files in range(len(lista_file)):
    
    # Lectura de nuestro archivo
    f=open('results/'+lista_file[files],'r')
    prediccion = f.readlines()
    
    for objetos in range(5,len(prediccion)):
        
        name.append(prediccion[4].split('img_nuevas/')[1].split(':')[0]) # Nombre de imagen
        tipo.append(prediccion[objetos].split(':')[0]) # Categoria 
        puntaje.append(int(prediccion[objetos].split(':')[1].split('%')[0])) # Puntaje

data ={
    'Nombre_imagen':name,
    'Fase':tipo,
    'Confianza (%)' :puntaje 
    }

# Creamos dataframe
df=pd.DataFrame(data)

# Resultados

df_final ={
    'Rosas':df[df['Fase']=='rose'].count()[0],
    'Botones':df[df['Fase']=='button'].count()[0],
    'Total':df[df['Fase']=='rose'].count()[0]+df[df['Fase']=='button'].count()[0]
    
    }

df_final=pd.DataFrame(df_final,index=['Detecciones YOLO'])

# Impresion archivo Excel
with pd.ExcelWriter('Detecciones_modelo_YOLO.xlsx') as writer:
    df.to_excel(writer,sheet_name='Detecciones')
    df_final.to_excel(writer,sheet_name='Totales')
    
despues=datetime.now()
final=despues-antes
print('El Procesamiento de todas las imagenes tuvo una duracion de  : ' + str(final) + ' h : Min : Seg' )

# FINAL .....

    