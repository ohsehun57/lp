# Mostrar un triángulo de un solo color usando PyOpenGL y clases
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class TrianguloApp:
    def __init__(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
        glutInitWindowSize(500, 500)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b"Triangulo de un solo color - PyOpenGL")
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fondo blanco
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Configuramos un sistema de coordenadas ortogonal simple
        glOrtho(-15, 15, -15, 15, -1, 1)

        glutDisplayFunc(self.dibujar)
        glutMainLoop()

    def dibujar(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glPointSize(2)
#usi para u
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-0.5, -0.5)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(0.5, -0.5)
        glColor3f(0.0, 0.0, 1.0); glVertex2f(0.0, 0.5)
        glColor3f(0.0, 0.0, 1.0); glVertex2f(0.0, 0.5)
        glEnd()
#usi para n
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-0.5, -0.5)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(0.5, -0.5)
        glColor3f(0.0, 0.0, 1.0); glVertex2f(0.0, 0.5)
        glColor3f(0.0, 0.0, 1.0); glVertex2f(0.0, 0.5)
        glEnd()
#usi para a
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.0, 0.0); glVertex2f(-0.5, -0.5)
        glColor3f(0.0, 1.0, 0.0); glVertex2f(0.5, -0.5)
        glColor3f(0.0, 0.0, 1.0); glVertex2f(0.0, 0.5)
        glColor3f(0.0, 0.0, 1.0); glVertex2f(0.0, 0.5)
        glEnd()

        glFlush()

if __name__ == "__main__":
    TrianguloApp()