from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL.Image import *

textures = {}


class Planet:
    def __init__(self, fName, distance, r):
        self.fName = fName
        self.distance = distance
        self.r = r

    @staticmethod
    def LoadTextures(fName):
        if textures.get(fName) is not None:
            return textures.get(fName)
        texture = textures[fName] = glGenTextures(1)
        image = open(fName)

        ix = image.size[0]
        iy = image.size[1]
        image = image.tobytes("raw", "RGBX", 0, -1)
        # Create Texture
        glBindTexture(GL_TEXTURE_2D, texture)  # 2d texture (x and y size)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        return texture

    def drawPlanet(self, flag=False):
        glBindTexture(GL_TEXTURE_2D, self.LoadTextures(self.fName))

        Q = gluNewQuadric()
        gluQuadricNormals(Q, GL_SMOOTH)
        gluQuadricTexture(Q, GL_TRUE)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

        glPushMatrix()
        glTranslatef(0.0, 0.0, self.distance)  # Center The Cylinder
        if flag:
            glPushMatrix()
            glScalef(1.1, 1, 1)  # Center The Cylinder
            glutWireTorus(0.10, 0.67, 100, 50)
            glPopMatrix()
        gluSphere(Q, self.r, 32, 16)
        glPopMatrix()

        gluDeleteQuadric(Q)
