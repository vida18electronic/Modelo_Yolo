import cv2
import os
from tqdm import tqdm
from datetime import datetime,timedelta


# Listamos nuestras imagenes
lista_img=[imagenes for imagenes in os.listdir('./img_nuevas/') if imagenes.endswith('.jpg')==True]


# Creacion de rutas para las  imagenes
rutas=[]

for imagenes in lista_img:
    
    rutas.append('../img_nuevas/'+imagenes)
    
file=open("train.txt","w")
# Cerramos nuestro archivo
for i in range(len(rutas)):
    
    file.write(rutas[i]+'\n')

file.close()

directorio=os.getcwd()

#print(directorio+'/darknet')

# Directorio principal
os.chdir(directorio+'/darknet')

# Copiamos archivos al directorio 'darknet/cfg'
os.system('cp ../obj.data  ./cfg')
os.system('cp ../train.txt ./data')



# Ciclo para crear archivos de texto con predicciones
#input_img=[]
#filename=[]
#for imagenes in tqdm(lista_img):
#  input_img.append('../img_nuevas/'+imagenes)
#  filename.append(imagenes.split('.jpg')[0]+'.txt')

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

# Ejecutamos el comando de procesamiento en lotes

os.system('./darknet detector test cfg/obj.data cfg/yolov3_custom_new.cfg ../yolov3_custom_new_final.weights -dont_show < data/train.txt > results_RD.txt')


print('\n')
print('===================================================|')
print('                                                   |')
print('===  Finalizado conteo de objetos detectados  =====|')
print('                                                   |')
print('===== Revisar archivo darknet/results_RD.txt ======|')
print('                                                   |')
print('===================================================|')
print('\n')
print('\n')

despues=datetime.now()
final=despues-antes

print('\n')
print('\n')
print('EL TIEMPO DE PROCESAMIENTO TOTAL DE ' + str(len(lista_img)) + ' IMAGENES FUE : ' + str(final) + ' HH:MM:SS')
print('\n')
print('\n')
print('EL TIEMPO DE PROCESAMIENTO POR IMAGEN FUE : ' + str(round(final.total_seconds()/len(lista_img),2)) + ' SEGUNDOS')
print('\n')
print('\n')
# FINAL .....












