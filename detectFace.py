import cv2

# Définir la largeur et la hauteur de la fenêtre

# Initialiser la capture vidéo depuis la webcam avec la taille spécifiée
cap = cv2.VideoCapture(0)

# Charger le classificateur en cascade pour la détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    # Lire une image depuis la webcam
    ret, frame = cap.read()
    height, width, _ = frame.shape
    # print(height, width)

    # Convertir l'image en niveaux de gris pour la détection de visage
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.015, 7)
    # Initialiser les variables pour le visage avec la plus grande largeur
    max_width = 0
    max_face = None
    
    # Trouver le visage avec la plus grande largeur
    for (x, y, w, h) in faces:
        if w > max_width:
            max_width = w
            max_face = (x, y, w, h)
    
    # Dessiner un rectangle autour du visage avec la plus grande largeur
    if max_face is not None:
        x, y, w, h = max_face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Calculer les coordonnées normalisées x et y du centre du visage
        pos_x = (x / (width - w) * 2) - 1
        pos_y = (y / (height - h) * 2) - 1
        pos_z = (height - h) / height

        # roi_gray = gray[y:y+h, x:x+w]
        # roi_color = frame[y:y+h, x:x+w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)

        # # Ne conserver que les deux premières détections
        # eyes = eyes[:2]
        # centers = []
        # for (ex, ey, ew, eh) in eyes:
        #     center = (x + ex + ew//2, y + ey + eh//2)
        #     centers.append(center)
        #     # Dessiner un cercle autour du centre de l'oeil
        #     cv2.circle(frame, center, 2, (0, 255, 0), -1)
        # if len(centers) == 2:
        #     eye1_center, eye2_center = centers
        #     distance = ((eye1_center[0] - eye2_center[0]) ** 2 + (eye1_center[1] - eye2_center[1]) ** 2) ** 0.5

        #     distance = (width - distance) / width
        #     print(distance)


    # Afficher l'image
    cv2.imshow('Face Detection', frame)

    # Sortir de la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture vidéo et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
