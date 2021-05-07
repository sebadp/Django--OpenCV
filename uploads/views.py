from django.shortcuts import render

# Create your views here.



import cv2
def show_camera(request):

    # Asignamos la cámara 0 a la variable cam
    cam = cv2.VideoCapture(0)

    # Mientras la cámara esté prendida hace lo siguiente:
    while cam.isOpened():
        # Creamos dos variables para obtener la data de la cámara
        ret, frame = cam.read()
        # Creamos frame2 para tener otra captura posterior
        ret, frame2 = cam.read()
        # Comparamos las capturas y detectamos movimiento
        diff = cv2.absdiff(frame, frame2)

        # Definimos el color a un tipo de gris, hay muchos COLOR_*
        gray = cv2.cvtColor(diff, cv2.COLOR_RGBA2GRAY)

        # Aplicamos difuminado
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Tresh limpia la imágen y presenta un binario
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        # Engrosa o afina la linea
        dilated = cv2.dilate(thresh, None, iterations=3)

        # Detectamos los contornos del movimiento y los guardamos en 
        # una variable
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # dibujamos un contorno sobre cualquier movimiento
        # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # En este for vamos a declarar que se ignoren los movimientos
        # pequeños. De lo contrario tomamos datos del contorno y lo 
        # guardamos en las variables x, y, w, h, para luego dibujar
        # un rectangulo sobre el frame 
        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Indicamos que si presionamos 'q' apagamos la cam.
        if cv2.waitKey(10) == ord('q'):
            break

    # mostrámos la visión en la pc:
    cv2.imshow('Sebas Cam', frame)

    context = {
        'camera': cam,
    }

    return render(request, 'index.html', context)