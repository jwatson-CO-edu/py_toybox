#! /usr/bin/env python
#
#    <one line to give the program's name and a brief idea of what it does.>
#    Copyright (C) 2001  Michael Urman
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


"""Loads a simple model format and draws it with opengl.
allows rotations and whatnot based on simple cursor input"""

__version__ = '0.05'
__date__ = '2002/05/23'
__author__ = 'Michael Urman (mu on irc.openprojects.net)'

import sys, math
try:
    import pygame
    from pygame.locals import *
    from OpenGL.GL import *
except:
    print 'model requires pygame and pyopengl'
    raise SystemExit

try:
    from OpenGL.GLU import *
    GLU = 1
except:
    print "Warning: OpenGL.GLU did not import correctly."
    GLU = None

if len(sys.argv) < 2:
    print 'Usage: model.py model.mf'
    raise SystemExit

import Numeric as N
import types
def _cross(a, b):
    return N.array((\
        a[1]*b[2]-a[2]*b[1], \
        a[2]*b[0]-a[0]*b[2], \
        a[0]*b[1]-a[1]*b[0]))
class Quaternion:
    def __init__(q, quat=None):
        """Quaternion(q, quat=None) -> Quaternion

        Creates a new "pure" quaternion (of no rotation).  If a quaternion
        is passed in, it is copied.  If a tuple of the format (degrees, (x,
        y, z)) or (x, y, z, w) is passed in, it is turned into a
        quaternion."""

        if quat:
            if isinstance(quat, Quaternion):
                q.r = quat.r
                q.v = quat.v[:]
            elif isinstance(quat, types.TupleType):
                if len(quat) == 4:
                    q.v = N.array(quat[0:3])
                    q.r = quat[3]
                elif len(quat) == 2 and isinstance(quat[1], types.TupleType)\
                    and len(quat[1]) == 3:
                        angle = quat[0] * math.pi/360
                        q.r = math.cos(angle)
                        sin_a = math.sin(angle)
                        q.v = sin_a * N.array(quat[1])
                else:
                    raise TypeError("Invalid tuple for argument 2")
            else:
                raise TypeError("Argument 2 must be a tuple")
        else:
            q.v = N.array((1,0,0))
            q.r = 0

    def rotate(self, angle, axis):
        """rotate(self, angle, axis) -> self

        Rotate Quaternion self by angle (degrees) around axis (x, y, z) and
        return self for each chaining"""

        q = Quaternion((angle,axis)) * self
        self.r = q.r
        self.v = q.v

    def __mul__(q, o):
        """Quaternion *= Quaternion -> Quaternion
        Quaternion *= float -> Quaternion

        Multiplies a Quaternion by a constant or by another Quaternion.
        Remember to do (b * a) for a Quaternion representation of a rotation
        by a then by b.  Not Commutative!"""

        if isinstance(o, Quaternion):
            r = q.r; v = q.v
            s = o.r; w = o.v
            angle = r*s - N.dot(v,w)
            vec = r*w + s*v + _cross(v,w)

            n = math.sqrt(angle*angle + N.dot(vec,vec))
            return Quaternion((vec[0]/n, vec[1]/n, vec[2]/n, angle/n))
        else:
            return Quaternion((q.v[0]*o, q.v[1]*o, q.v[2]*o, q.r*o))

    def __imul__(q, o):
        """Quaternion *= Quaternion -> None
        Quaternion *= float -> None

        Multiplies a Quaternion in place by a constant or by another
        Quaternion.  Remember to do (b * a) for a Quaternion representation
        of a rotation by a then by b.  Not Commutative!"""

        if isinstance(o, Quaternion):
            r = q.r; v = q.v
            s = o.r; w = o.v
            q.r = r*s - N.dot(v,w)
            q.v = r*w + s*v + _cross(v,w)
            q.normalize()
        else:
            q.r *= o
            q.v *= o
        return q

    def __abs__(q):
        """abs(Quaternion) -> float

        Returns the magnitue of the Quaternion = sqrt(x*x+y*y+z*z+w*w)"""

        return math.sqrt(q.r*q.r + N.dot(q.v,q.v))

    def normalize(q):
        """normalize(q) -> q

        Normalizes the Quaternion such that the magnitued is 1.0"""

        n = abs(q)
        if n: q *= (1.0/n)
        return q

    def angle(q):
        """angle(q) -> float

        Return the angle of rotation (in degrees) represented by q"""

        return math.acos(q.r)*360/math.pi

    def axis(q):
        """axis(q) -> [x,y,z]

        Returns a (Numeric) array of the axis of rotation represented by q.
        Normalizes the vector to have magnitude of 1.0"""

        n = math.sqrt(N.dot(q.v,q.v))
        if not n: n = 1.0
        return q.v / n

    def __repr__(q):
        """repr(Quaternion) -> string
        
        Return a string of the format '<w [x y z]>' (direct Quaternion
        values)"""

        return '<%f %s>'%(q.r, q.v)

    def __str__(q):
        """str(Quaternion) -> string

        Return a string of the format '<angle (x y z)>' (angle in degrees
        and normalized axis of rotation)"""

        ax = q.axis()
        return '<%0.2f (%0.2f %0.2f %0.2f)>'%(q.angle(), ax[0], ax[1], ax[2])

class ModelNode:
    """Node base class for modeling system"""
    def __init__(self, *children):
        if children: self._children = children
        else: self._children = []

    def __repr__(self):
        return '<ModelNode id %s>'%id(self)

    def draw(self, *args, **kvargs):
        for c in self._children: c.draw(*args, **kvargs)

    def add(self, *children):
        """add(self, children) -> None

        Add all children under the current Node"""

        self._children.extend(children)

class Transform(ModelNode):
    """Transformation nodes for hierarchical models"""
    def __init__(self, translate=None, rotate=None, scale=None):
        ModelNode.__init__(self)
        self._x_translate = translate or [0,0,0]
        self._x_rotate = rotate or Quaternion((0, (1,0,0)))
        self._x_scale = scale or [1,1,1]

    def draw(self, *args, **kvargs):
        """draw(self, *args, **kvargs) -> None

        Applies transformations and calls children's draw() routine"""

        glPushMatrix()
        glTranslate(*self._x_translate)
        glRotatef(self._x_rotate.angle(), *self._x_rotate.axis())

        glScale(*self._x_scale)
        ModelNode.draw(self, *args, **kvargs)
        glPopMatrix()

    def rotate(self, angle, axis):
        """rotate(self, angle, axis) -> None

        Rotate model by angle around the axis (x,y,z)"""

        # normalize axis
        al = 1/math.sqrt(axis[0]*axis[0]+axis[1]*axis[1]+axis[2]*axis[2])
        axis = axis[0] * al, axis[1]*al, axis[2]*al

        self._x_rotate.rotate(angle, axis)

        return self._x_rotate

    def translate(self, delta):
        """translate(self, delta) -> None

        Translate model by delta (x,y,z)"""

        self._x_translate[0] += delta[0]
        self._x_translate[1] += delta[1]
        self._x_translate[2] += delta[2]
        return self._x_translate[:]

    def scale(self, factor):
        """scale(self, factor) -> None

        Scale model by factor (x,y,z)"""

        if factor: self._x_scale = [self._x_scale[i]*factor[i] for i in range(3)]
        return self._x_scale[:]


class SMF(ModelNode):
    """Handles loading and drawing of a simple model format"""

    def __init__(self, filename=None, calcnormals=None):
        """SMF([filename]) optionally loads model stored in passed filename"""

        ModelNode.__init__(self)

        self.vertices = []          # list of vertices
        self.colors = []            # corresponding colors
        self.faces = []             # list of references to vertices
        self.normals = []           # normals correspond to each face
        self.texture = None
        self.texturecoords = []     # S,T corresponds to each vertex

        self.usedrawlist = None
        self.drawlist = None

        if filename:
            f = open(filename)
            linecount = 0
            for line in f.xreadlines():
                linecount += 1
                items = line.split()
                # v X Y Z defines a vertex at (x, y, z)
                if len(items) == 4 and items[0] == 'v':
                    self.vertices.append(map(lambda x:float(x), items[1:4]))
                # f A B C defines a face using vertices A, B, C
                elif len(items) == 4 and items[0] == 'f':
                    self.faces.append(map(lambda x:int(x)-1, items[1:4]))
                # c R G B defines a color for corresponding vertex
                elif len(items) == 4 and items[0] == 'c':
                    self.colors.append(map(lambda x:float(x), items[1:4]))
                # t S T defines a texture coordinate for corresponding vertex
                elif len(items) == 3 and items[0] == 't':
                    self.texturecoords.append(map(lambda x:float(x), items[1:3]))
                # t filename defines a texture for the model
                #            should be 2**k x 2**k pixels
                elif len(items) == 2 and items[0] == 't':
                    if self.texture:
                        raise RuntimeError("Can't handle multiple textures")
                    self.texture = items[1]
                elif line[0] == '#' or len(items) == 0:
                    pass
                else:
                    raise RuntimeError("Invalid syntax on line %d '%s'"%(linecount, line))
            if self.texture:
                if not GLU:
                    raise NotImplementedError("textures require mipmaps require OpenGL.GLU")

                # load and prepare texture image for opengl
                img = pygame.image.load(self.texture)
                w, h = img.get_width(), img.get_height()
                rgb = pygame.image.tostring(img, "RGB", 0)

                #assign a texture
                self.textureid = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.textureid)
                #glPixelStorei(GL_UNPACK_ALIGNMENT,1)


                #build MIPMAP levels
                gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, w, h, GL_RGB, GL_UNSIGNED_BYTE, rgb)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)


    def draw(self, *args, **kvargs):
        """Draw the model to the waiting screen"""

        if kvargs.has_key('wireframe') and kvargs['wireframe']:
            for face in self.faces:
                glBegin(GL_LINE_LOOP)
                for vert in face:
                    glColor3fv(self.colors[vert])
                    glVertex3fv(self.vertices[vert])
                glEnd()
        elif self.usedrawlist:
            glCallList(self.drawlist)
        else:
            if self.texture:
                glPushAttrib(GL_ENABLE_BIT)     # save old enables
                glColor4f(1,1,1,1)
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.textureid)
                glBegin(GL_TRIANGLES)
                for face in self.faces:
                    for vert in face:
                        glTexCoord2fv(self.texturecoords[vert])
                        glVertex3fv(self.vertices[vert])
                glEnd()
                glPopAttrib()
            else:
                glBegin(GL_TRIANGLES)
                for face in self.faces:
                    for vert in face:
                        glColor3fv(self.colors[vert])
                        glVertex3fv(self.vertices[vert])
                glEnd()

    def build_display_list(self):
        """Try to optimize the draw routine by using a display list"""
        self.drawlist = glGenLists(1)
        glNewList(self.drawlist, GL_COMPILE)
        self.draw()
        glEndList()
        self.usedrawlist = 1

class OGLSprite:
    """Implement the ugly details of "blitting" to OpenGL"""

    def __init__(self, surf, rect=None, mipmap=None):
        """OGLSprite(self, surf, rect=None) -> OGLSprite
        
        Create a drawable texture out of a given surface."""

        if not rect: rect = surf.get_rect()

        w, h = surf.get_width(), surf.get_height()
        w2, h2 = 1, 1
        while w2 < w: w2 <<= 1
        while h2 < h: h2 <<= 1

        #surfr = pygame.surfarray.pixels3d(surf)
        #surfa = pygame.surfarray.alpha(surf)
        img = pygame.Surface((w2, h2), SRCALPHA, surf)
        #imgr = pygame.surfarray.pixels3d(img)
        #imga = pygame.surfarray.pixels_alpha(img)

        #putmask(imgr, 
        #putmask(imga, 

        img.blit(surf, (0,h2-h), rect)
        rgba = pygame.image.tostring(img, "RGBA", 0)

        # prove that blitting sucks?
        #print "0:",surf.get_at((0,0))
        #print "1:",img.get_at((0,0))

        #assign a texture
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        #glPixelStorei(GL_UNPACK_ALIGNMENT,1)

        if mipmap:
            if not GLU:
                raise NotImplementedError("OGLSprite mipmaps require OpenGL.GLU")
            #build MIPMAP levels. Ths is another slow bit            
            gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, w2, h2, GL_RGBA, GL_UNSIGNED_BYTE, rgba)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w2, h2, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 

        self.mipmap = mipmap
        self.srcsize = w, h
        self.texsize = w2, h2
        self.coords = float(w)/w2, float(h)/h2
        self.texid = texid
        #print "TEX", self.srcsize, self.texsize, self.coords

    def update(self, surf, rect=None):
        """update(self, surf, rect=None) -> None
        
        """
        if self.mipmap:
            raise TypeError("Cannot update a mipmap enabled OGLSprite")

        if not rect: rect = surf.get_rect()

        w, h = surf.get_width(), surf.get_height()
        w2, h2 = 1, 1
        while w2 < w: w2 <<= 1
        while h2 < h: h2 <<= 1

        img = pygame.Surface((w2, h2), SRCALPHA, surf)
        img.blit(surf, (0,h2-h), rect)
        rgba = pygame.image.tostring(img, "RGBA", 0)

        glBindTexture(GL_TEXTURE_2D, self.texid)
        if 'glTexSubImage2D' in dir() \
            and w2 <= self.texsize[0] and h2 <= self.texsize[1]:

            # untested; i suspect it doesn't work
            w2, h2 = self.texsize
            glTexSubImage2D(GL_TEXTURE_RECTANGLE_EXT, 0,
                0, 0, w2, h2, GL_RGBA, GL_UNSIGNED_BYTE, rgba);
            if (w, h) != self.srcsize:
                self.coords = float(w)/w2, float(h)/h2
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                w2, h2, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba)
            self.coords = float(w)/w2, float(h)/h2
            self.texsize = w2, h2

        self.srcsize = w, h

        #print "TEX", self.srcsize, self.texsize, self.coords


    def blit_at(self, *rects):
        """blit_at(self, *rects) -> self

        Draw the texture at the supplied position(s).  If a tuple and width and
        height are not specified, the original size is used (just like you'd
        expect).  Returns self so ogs.enter().blit().exit() works"""

        for rect in rects:
            x0, y0 = rect[0:2]
            try:
                x1, y1 = x0 + rect[2], y0 + rect[3]
            except IndexError:
                x1, y1 = x0 + self.srcsize[0] - 1, y0 + self.srcsize[1] - 1

            glBindTexture(GL_TEXTURE_2D, self.texid)
            glBegin(GL_TRIANGLE_STRIP)
            glTexCoord2f(0, 0); glVertex2f(x0, y0)
            glTexCoord2f(self.coords[0], 0); glVertex2f(x1, y0)
            glTexCoord2f(0, self.coords[1]); glVertex2f(x0, y1)
            glTexCoord2f(self.coords[0], self.coords[1]); glVertex2f(x1, y1)
            glEnd()

        return self

    def enter(self):
        """enter(self) -> self
        
        Set up OpenGL for drawing textures; do this once per batch of
        textures.  Returns self so ogs.enter().blit().exit() works"""

        glPushAttrib(GL_ENABLE_BIT)     # save old enables
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glColor4f(1,1,1,1)
        glEnable(GL_TEXTURE_2D)

        # XXX: in pre pygame1.5, there is no proper alpha, so this makes
        # the entire texture transparent.  in 1.5 and forward, it works.
        if pygame.version.ver >= '1.4.9':
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #glEnable(GL_ALPHA_TEST)
        #glAlphaFunc(GL_GREATER, 0.5)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, 640.0, 480.0, 0.0, 0.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        return self

    def exit(self):
        """exit(self) -> None

        Return OpenGL to previous settings; do this once per batch."""

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glPopAttrib()

    def get_width(self):
        """get_width(self) -> int"""

        return self.srcsize[0]

    def get_height(self):
        """get_height(self) -> int"""

        return self.srcsize[1]


def main():
    """loads and runs the model display"""

    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)     # use zbuffer

    # boring camera setup
    glMatrixMode(GL_PROJECTION)
    if GLU:
        gluPerspective(45.0, 640/480.0, 0.1, 100.0)
    else:
        f = 1.3 / (math.tan(45.0/2))
        glMultMatrix((f*480/640, 0, 0, 0,
                    0, f, 0, 0,
                    0, 0, 100.1/-99.9, -1,
                    0, 0, 2*100*0.1/-99.9, 0))
    
    glTranslatef(0.0, 0.0, -3.0)
    glRotatef(25, 1,0,0)

    cube = SMF(sys.argv[1])
    model = Transform()
    model.add(cube)

    font = pygame.font.Font(None, 48)
    text = OGLSprite(font.render('Pygame', 1, (255, 0, 0)))

    update = 1
    do_wireframe = 0
    quit = 0
    hide = 0
    while 1:
        events = [pygame.event.wait()]
        if pygame.event.peek():
            events.extend(pygame.event.get())

        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quit = 1
            elif event.type == KEYDOWN and event.key == K_RETURN:
                pygame.display.toggle_fullscreen()

            elif event.type == KEYDOWN and event.key == K_t:
                text.update(font.render('Pygame', 1, (255, 0, 0)))
                update = 1
            elif event.type == KEYDOWN and event.key == K_w:
                do_wireframe = not do_wireframe
                update = 1
            elif event.type == VIDEOEXPOSE:
                update = 1
            elif event.type == MOUSEBUTTONDOWN:
                if event.button in (1,3):
                    hide += 1
                    pygame.mouse.set_visible(0)
                    pygame.event.set_grab(1)
                elif event.button == 2:
                    print 'building display list'
                    cube.build_display_list()
            elif event.type == MOUSEBUTTONUP:
                if event.button in (1,3):
                    hide -= 1
                    if not hide:
                        pygame.mouse.set_visible(1)
                        pygame.event.set_grab(0)

            if event.type == MOUSEMOTION and not update:
                if event.buttons[0]:
                    dx, dy = event.rel
                    dist = math.sqrt(dx*dx+dy*dy)
                    q = model.rotate(dist, (event.rel[1], event.rel[0], 0))
                    text.update(font.render(str(q), 1, (255, 127, 127)))
                    update = 1
                if event.buttons[2]:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        s = 100 + event.rel[0]+event.rel[1]
                        s *= 0.01
                        x, y, z = model.scale((s,s,s))
                        text.update(font.render('<%0.2f %0.2f %0.2f>'%(x,y,z), 1, (126, 127, 255)))
                    else:
                        x, y, z = model.translate((event.rel[0]*0.02, -event.rel[1]*0.02, 0))
                        text.update(font.render('<%0.2f %0.2f %0.2f>'%(x,y,z), 1, (255, 127, 127)))
                    update = 1

        if quit:
            break

        if update:
            update = 0
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            model.draw(wireframe=do_wireframe)

            text.enter()
            text.blit_at(
                (screen.get_width()-text.get_width()+1,
                screen.get_height()-text.get_height()+1))
            text.exit()

            pygame.display.flip()


if __name__ == '__main__': main()
