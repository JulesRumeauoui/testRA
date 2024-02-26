import cv2

# Définir la largeur et la hauteur de la fenêtre

# Initialiser la capture vidéo depuis la webcam avec la taille spécifiée
cap = cv2.VideoCapture(0)

# Charger le classificateur en cascade pour la détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # Lire une image depuis la webcam
    ret, frame = cap.read()
    height, width, _ = frame.shape
    # print(height, width)

    # Convertir l'image en niveaux de gris pour la détection de visage
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Dessiner un rectangle autour des visages détectés et afficher la vidéo
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        # Calculer les coordonnées normalisées x et y du centre du visage
        pos_x = (x / (width - w) * 2) - 1
        pos_y = (y / (height - h) * 2) - 1
        pos_z = (height - h) / height
        print(pos_z)

    # Afficher l'image
    cv2.imshow('Face Detection', frame)

    # Sortir de la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture vidéo et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
