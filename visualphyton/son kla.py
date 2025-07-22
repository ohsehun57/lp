from manim import *

class SonKlarisma3D(ThreeDScene):
    def construct(self):
        # Activar la cámara 3D
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Crear el texto 3D
        texto = Text3D("son klarisma", font="Arial", weight=BOLD)
        texto.scale(1.5)
        texto.set_color_by_gradient(BLUE, PURPLE)
        texto.move_to(ORIGIN)

        # Agregar luz
        self.add_light_source()
        self.add(texto)

        # Animaciones: escalar, rotar y mover
        self.play(ScaleInPlace(texto, 1.2), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.1)

        self.play(Rotate(texto, angle=PI, axis=UP), run_time=4)
        self.play(texto.animate.shift(UP * 1.5), run_time=2)
        self.play(texto.animate.shift(DOWN * 3), run_time=2)
        self.play(texto.animate.shift(UP * 1.5), run_time=2)

        # Final
        self.wait(2)
