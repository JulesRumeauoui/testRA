import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import cv2

# Variables de position et angle de la caméra
xpos = 0
ypos = 0
zpos = 5
xrot = 0
yrot = 0

epsilon_x = 1
epsilon_y = 1
epsilon_z = 20

cap = cv2.VideoCapture(0)

# Charger le classificateur en cascade pour la détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# Drapeaux pour les touches enfoncées
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
space_pressed = False
shift_pressed = False

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)

def draw_point(x,y,z):
    glColor3f(1.0, 0.0, 0.0)  # Rouge
    glPointSize(5)  # Taille du point
    glBegin(GL_POINTS)
    glVertex3f(x,y,z)  # Coordonnées du point en 3D
    glEnd()

def draw_cube():
    glBegin(GL_QUADS)
    
    # Top face
    glColor3f(1.0, 0.0, 0.0)  # Red color
    glVertex3f(1.0, 1.0, -6.0) # Top right of quad (top)
    glVertex3f(-1.0, 1.0, -6.0) # Top left of quad (top)
    glVertex3f(-1.0, 1.0, -4.0) # Bottom left of quad (top)
    glVertex3f(1.0, 1.0, -4.0) # Bottom right of quad (top)

    # Bottom face
    glColor3f(0.0, 1.0, 0.0)  # Green color
    glVertex3f(1.0, -1.0, -4.0) # Top right of quad (bottom)
    glVertex3f(-1.0, -1.0, -4.0) # Top left of quad (bottom)
    glVertex3f(-1.0, -1.0, -6.0) # Bottom left of quad (bottom)
    glVertex3f(1.0, -1.0, -6.0) # Bottom right of quad (bottom)

    # Front face
    glColor3f(0.0, 0.0, 1.0)  # Blue color
    glVertex3f(1.0, 1.0, -4.0) # Top right of quad (front)
    glVertex3f(-1.0, 1.0, -4.0) # Top left of quad (front)
    glVertex3f(-1.0, -1.0, -4.0) # Bottom left of quad (front)
    glVertex3f(1.0, -1.0, -4.0) # Bottom right of quad (front)

    # Back face
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    glVertex3f(1.0, -1.0, -6.0) # Top right of quad (back)
    glVertex3f(-1.0, -1.0, -6.0) # Top left of quad (back)
    glVertex3f(-1.0, 1.0, -6.0) # Bottom left of quad (back)
    glVertex3f(1.0, 1.0, -6.0) # Bottom right of quad (back)

    # Left face
    glColor3f(1.0, 0.0, 1.0)  # Purple color
    glVertex3f(-1.0, 1.0, -4.0) # Top right of quad (left)
    glVertex3f(-1.0, 1.0, -6.0) # Top left of quad (left)
    glVertex3f(-1.0, -1.0, -6.0) # Bottom left of quad (left)
    glVertex3f(-1.0, -1.0, -4.0) # Bottom right of quad (left)

    # Right face
    glColor3f(0.0, 1.0, 1.0)  # Cyan color
    glVertex3f(1.0, 1.0, -6.0) # Top right of quad (right)
    glVertex3f(1.0, 1.0, -4.0) # Top left of quad (right)
    glVertex3f(1.0, -1.0, -4.0) # Bottom left of quad (right)
    glVertex3f(1.0, -1.0, -6.0) # Bottom right of quad (right)

    glEnd()


def get_face_position():

    # Lire une image depuis la webcam
    ret, frame = cap.read()

    height, width, _ = frame.shape
    # print(height, width)
    # Convertir l'image en niveaux de gris pour la détection de visage
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

   

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        # Calculer les coordonnées normalisées x et y du centre du visage
        pos_x = (x / (width - w) * 2) - 1
        pos_y = (y / (height - h) * 2) - 1
        pos_z = (height - h) / height
        
        cv2.imshow('Face Detection', frame)
        return (pos_x,pos_y,pos_z)

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
        #     pos_z = distance

            # return (pos_x,pos_y,pos_z)

    # Afficher l'image
    return 0


def main():
    global xpos, ypos, zpos, xrot, yrot, left_pressed, right_pressed, up_pressed, down_pressed, space_pressed, shift_pressed
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)    
    init()

    n = 7  # Nombre de dernières valeurs à considérer pour la moyenne glissante
    xpos_values = []  # Liste pour stocker les valeurs de xpos
    ypos_values = []  # Liste pour stocker les valeurs de ypos
    zpos_values = []  # Liste pour stocker les valeurs de zpos


    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_pressed = True
                elif event.key == pygame.K_RIGHT:
                    right_pressed = True
                elif event.key == pygame.K_UP:
                    up_pressed = True
                elif event.key == pygame.K_DOWN:
                    down_pressed = True
                elif event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_LSHIFT:
                    shift_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_pressed = False
                elif event.key == pygame.K_RIGHT:
                    right_pressed = False
                elif event.key == pygame.K_UP:
                    up_pressed = False
                elif event.key == pygame.K_DOWN:
                    down_pressed = False
                elif event.key == pygame.K_SPACE:
                    space_pressed = False
                elif event.key == pygame.K_LSHIFT:
                    shift_pressed = False

        if left_pressed:
            xpos += 0.1
        elif right_pressed:
            xpos -= 0.1
        if up_pressed:
            ypos -= 0.1
        elif down_pressed:
            ypos += 0.1
        if space_pressed:
            zpos += 0.1
        elif shift_pressed:
            zpos -= 0.1

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()


        near = 1.0
        far = 100.0


        left = ((xpos + 5) / 5 * -1) / (zpos / 5)
        right = ((xpos - 5) / 5  * -1) / (zpos / 5)
        bottom = ((ypos + 5) / 5 * -1) / (zpos / 5)
        top = ((ypos - 5) / 5  * -1) / (zpos / 5)

        
        if zpos <=  2 :
            zpos = 2
        


        res_position_face = get_face_position()
        if res_position_face == 0:
            print("pas de visage")
            continue
        xpos, ypos, zpos = res_position_face

        zpos = zpos * epsilon_z
        xpos = xpos * zpos * epsilon_x
        ypos = ypos * zpos * epsilon_y

        xpos *= -1 
        ypos *= -1 
        


        xpos_values.append(xpos)
        ypos_values.append(ypos)
        zpos_values.append(zpos)

        if len(xpos_values) > n:
            xpos_values = xpos_values[-n:]
            ypos_values = ypos_values[-n:]
            zpos_values = zpos_values[-n:]

        # Calculer la moyenne glissante
        avg_xpos = sum(xpos_values) / len(xpos_values)
        avg_ypos = sum(ypos_values) / len(ypos_values)
        avg_zpos = sum(zpos_values) / len(zpos_values)

        # left = -1.0 
        # right = 1
        # bottom = -1.0 
        # top = 1.0 
        # near = 1.0
        # far = 100.0

        glFrustum(left, right, bottom, top, near, far)
        # gluLookAt(xpos, ypos, zpos, xpos, ypos, 0, 0, 1, 0)
        gluLookAt(avg_xpos, avg_ypos, avg_zpos, avg_xpos, avg_ypos, 0, 0, 1, 0)
        # print(xpos, ypos, zpos)
        print(avg_xpos, avg_ypos, avg_zpos)
        draw_cube()

        #coin
        draw_point(5,-5,0)
        draw_point(-5,5,0)
        draw_point(-5,-5,0)
        draw_point(5,0,0)

        #milieu
        draw_point(-5,0,0)
        draw_point(0,5,0)
        draw_point(0,-5,0)
        draw_point(5,5,0)

        #cube
        draw_point(-5,0,-5)
        draw_point(5,0,-5)
        draw_point(0,-5,-5)
        draw_point(0,5,-5)
        draw_point(0,0,-10)

        pygame.display.flip()

      
main()
