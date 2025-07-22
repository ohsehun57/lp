from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# Ángulos de rotación
rotX, rotY, rotZ = 0, 0, 0

def init():
    glEnable(GL_DEPTH_TEST)         # Habilitar prueba de profundidad
    glEnable(GL_LIGHTING)           # Habilitar iluminación
    glEnable(GL_LIGHT0)             # Habilitar luz 0
    glEnable(GL_COLOR_MATERIAL)     # Permitir que el color afecte el material
    glClearColor(0.1, 0.1, 0.1, 1)  # Fondo oscuro

    # Configurar luz
    light_position = [1.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

def display():
    global rotX, rotY, rotZ
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Mover la cámara
    glTranslatef(0.0, 0.0, -5.0)

    # Aplicar rotaciones
    glRotatef(rotX, 1.0, 0.0, 0.0)
    glRotatef(rotY, 0.0, 1.0, 0.0)
    glRotatef(rotZ, 0.0, 0.0, 1.0)

    # Dibujar tetera
    glColor3f(0.7, 0.4, 0.8)  # Color violeta
    glutSolidTeapot(1.0)

    glutSwapBuffers()

def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global rotX, rotY, rotZ
    if key == b'a':
        rotZ -= 5
    elif key == b'd':
        rotZ += 5
    glutPostRedisplay()

def special_keys(key, x, y):
    global rotX, rotY
    if key == GLUT_KEY_RIGHT:
        rotY += 5
    elif key == GLUT_KEY_LEFT:
        rotY -= 5
    elif key == GLUT_KEY_UP:
        rotX -= 5
    elif key == GLUT_KEY_DOWN:
        rotX += 5
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)

    glutCreateWindow(b"Tetera 3D con rotación e iluminación")
    
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()
