import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
# Variables de position et angle de la caméra
xpos = 0
ypos = 0
zpos = 5
xrot = 0
yrot = 0

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
    gluPerspective(45, (800/600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)

def draw_cube():
    glBegin(GL_QUADS)
    
    glColor3f(1.0, 0.0, 0.0)  # Red color
    glVertex3f(1.0, 1.0, -1.0) # Top right of quad (top)
    glVertex3f(-1.0, 1.0, -1.0) # Top left of quad (top)
    glVertex3f(-1.0, 1.0, 1.0) # Bottom left of quad (top)
    glVertex3f(1.0, 1.0, 1.0) # Bottom right of quad (top)

    # Bottom face
    glColor3f(0.0, 1.0, 0.0)  # Green color
    glVertex3f(1.0, -1.0, 1.0) # Top right of quad (bottom)
    glVertex3f(-1.0, -1.0, 1.0) # Top left of quad (bottom)
    glVertex3f(-1.0, -1.0, -1.0) # Bottom left of quad (bottom)
    glVertex3f(1.0, -1.0, -1.0) # Bottom right of quad (bottom)

    # Front face
    glColor3f(0.0, 0.0, 1.0)  # Blue color
    glVertex3f(1.0, 1.0, 1.0) # Top right of quad (front)
    glVertex3f(-1.0, 1.0, 1.0) # Top left of quad (front)
    glVertex3f(-1.0, -1.0, 1.0) # Bottom left of quad (front)
    glVertex3f(1.0, -1.0, 1.0) # Bottom right of quad (front)

    # Back face
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    glVertex3f(1.0, -1.0, -1.0) # Top right of quad (back)
    glVertex3f(-1.0, -1.0, -1.0) # Top left of quad (back)
    glVertex3f(-1.0, 1.0, -1.0) # Bottom left of quad (back)
    glVertex3f(1.0, 1.0, -1.0) # Bottom right of quad (back)

    # Left face
    glColor3f(1.0, 0.0, 1.0)  # Purple color
    glVertex3f(-1.0, 1.0, 1.0) # Top right of quad (left)
    glVertex3f(-1.0, 1.0, -1.0) # Top left of quad (left)
    glVertex3f(-1.0, -1.0, -1.0) # Bottom left of quad (left)
    glVertex3f(-1.0, -1.0, 1.0) # Bottom right of quad (left)

    # Right face
    glColor3f(0.0, 1.0, 1.0)  # Cyan color
    glVertex3f(1.0, 1.0, -1.0) # Top right of quad (right)
    glVertex3f(1.0, 1.0, 1.0) # Top left of quad (right)
    glVertex3f(1.0, -1.0, 1.0) # Bottom left of quad (right)
    glVertex3f(1.0, -1.0, -1.0) # Bottom right of quad (right)

    glEnd()



def calculate_oblique_matrix_ortho(projection_matrix, clip_plane):
    q = np.dot(np.linalg.inv(projection_matrix), [np.sign(clip_plane[0]), np.sign(clip_plane[1]), 1.0, 1.0])
    c = clip_plane * (2.0 / np.dot(clip_plane, q))
    oblique_matrix = np.array(projection_matrix)
    oblique_matrix[0][2] = c[0]
    oblique_matrix[1][2] = c[1]
    oblique_matrix[2][2] = c[2]
    oblique_matrix[3][2] = c[3] - 1.0
    return oblique_matrix

def main():
    global xpos, ypos, zpos, xrot, yrot, left_pressed, right_pressed, up_pressed, down_pressed, space_pressed, shift_pressed
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    init()
    # gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0)

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

        projection_matrix = glGetFloatv(GL_PROJECTION_MATRIX)

        clip_plane = np.array([0.0, 1.0, 0.0, -1.0])

        oblique_matrix = calculate_oblique_matrix_ortho(projection_matrix, clip_plane)
        glLoadIdentity()

        glMultMatrixf(oblique_matrix)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(xpos, ypos, zpos, 0, 0, 0, 0, 1, 0)
        draw_cube()
        pygame.display.flip()

      
main()
