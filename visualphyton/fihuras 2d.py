from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Triangulo2D:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angulo = 0.0
        self.escala = 1.0

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
        glutInitWindowSize(600, 600)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b"Triangulo 2D: rotacion, traslacion y escalado")

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10, 10, -10, 10, -1, 1)

        glutDisplayFunc(self.dibujar)
        glutIdleFunc(self.actualizar)
        glutSpecialFunc(self.teclas_especiales)

        glutMainLoop()

    def dibujar(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Aplicar transformaciones: traslación, rotación, escala
        glTranslatef(self.x, self.y, 0)
        glRotatef(self.angulo, 0, 0, 1)
        glScalef(self.escala, self.escala, 1)

        # Triángulo con vértices de diferentes colores
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)  # Rojo
        glVertex2f(-2.0, -1.5)

        glColor3f(0.0, 1.0, 0.0)  # Verde
        glVertex2f(2.0, -1.5)

        glColor3f(0.0, 0.0, 1.0)  # Azul
        glVertex2f(0.0, 2.0)
        glEnd()

        glutSwapBuffers()

    def actualizar(self):
        glutPostRedisplay()

    def teclas_especiales(self, tecla, x, y):
        if tecla == GLUT_KEY_UP:
            self.y += 0.2
        elif tecla == GLUT_KEY_DOWN:
            self.y -= 0.2
        elif tecla == GLUT_KEY_LEFT:
            self.x -= 0.2
        elif tecla == GLUT_KEY_RIGHT:
            self.x += 0.2
        elif tecla == GLUT_KEY_F1:
            self.angulo += 5
        elif tecla == GLUT_KEY_F2:
            self.angulo -= 5
        elif tecla == GLUT_KEY_F3:
            self.escala += 0.1
        elif tecla == GLUT_KEY_F4:
            self.escala = max(0.1, self.escala - 0.1)  # evita valores negativos o 0

        # Normalizar ángulo
        if self.angulo >= 360:
            self.angulo -= 360
        elif self.angulo < 0:
            self.angulo += 360

        glutPostRedisplay()

if __name__ == "__main__":
    Triangulo2D()
