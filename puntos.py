import cv2
import numpy as np
  
#Iniciamos la camara
captura = cv2.VideoCapture(0)
 
# Parametros para la funcion de Lucas Kanade
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
 
#Capturamos una imagen y la convertimos de RGB -> HSV
_, imagen = captura.read()
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
  
#Establecemos el rango de colores que vamos a detectar
#En este caso de verde oscuro a verde-azulado claro
verde_bajos = np.array([57,61,64], dtype=np.uint8)
verde_altos = np.array([116, 255, 255], dtype=np.uint8)
  
#Crear una mascara con solo los pixeles dentro del rango de verdes
mask = cv2.inRange(hsv, verde_bajos, verde_altos)
 
#Eliminamos ruido
kernel = np.ones((10,10),np.uint8)
mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
 
#Detectamos contornos, nos quedamos con el mayor y calculamos su centro
_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mayor_contorno = max(contours, key = cv2.contourArea)
momentos = cv2.moments(mayor_contorno)
cx = float(momentos['m10']/momentos['m00'])
cy = float(momentos['m01']/momentos['m00'])
 
 
#Convertimos la imagen a gris para poder introducirla en el bucle principal
frame_anterior = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
 
 
 
#Convertimos el punto elegido a un array de numpy que se pueda pasar como parametro
#a la funcion cv2.calcOpticalFlowPyrLK()
punto_elegido, st, err = cv2.calcOpticalFlowPyrLK(frame_anterior, frame_gray, punto_elegido, None, **lk_params)
 
  
while(1):
      
    #Capturamos una imagen y la convertimos de RGB -> GRIS
    _, imagen = captura.read()
    frame_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
 
    #Se aplica el metodo de Lucas Kanade
    punto_elegido, st, err = cv2.calcOpticalFlowPyrLK(frame_anterior, frame_gray, punto_elegido, **lk_params)
 
    #Pintamos el centro (lo hacemos con un bucle por si, por alguna razon, decidimos pintar mas puntos)
    for i in punto_elegido:
          cv2.circle(imagen,tuple(i[0]), 3, (0,0,255), -1)
 
    #Se guarda el frame de la iteracion anterior del bucle
    frame_anterior = frame_gray.copy()
      
    #Mostramos la imagen original con la marca del centro
    cv2.imshow('Camara', imagen)
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
  
cv2.destroyAllWindows()