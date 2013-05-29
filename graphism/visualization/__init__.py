import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

SPHERE_RADIUS = 5.0
SPHERE_LONG_SLICES = 12
SPHERE_LAT_SLICES = 24
EYE = (0.0,0.0,-20.0)
CENTRE = (0.0,0.0,0.0)
UP = (0.0,1.0,0.0)

# Scene methods
def reset_view(w,h):
    width = float(w)
    height = float(h)
    aspect_ratio = width/height
    
    glViewport(0,0,int(width),int(height))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(50.0, aspect_ratio, 1.0, 50.0)
    gluLookAt(EYE[0], EYE[1], EYE[2], 
              CENTRE[0], CENTRE[1], CENTRE[2], 
              UP[0], UP[1], UP[2])
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    

def draw_scene():
    # Draw Sphere
    glColor3f(1,0,0)
    glutWireSphere(SPHERE_RADIUS, SPHERE_LONG_SLICES, SPHERE_LAT_SLICES)

def shutdown_scene():
    pass

def click_scene(x,y):
    pass

def drag_scene(x,y):
    pass

# Callbacks
def __resize(w,h):
    reset_view(w,h)

def __display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    draw_scene()
    
    glutSwapBuffers()
    
def __keyboard(key, x, y):
    if key == 27:
        pass
    if key == 'q':
        shutdown_scene()
        
    glutPostRedisplay()

def __mouse_button(button, state, x, y):
    if state == GLUT_DOWN:
        click_scene(x,y)

def __mouse_motion(x,y):
    drag_scene(x,y)

def __idle():
    glutPostRedisplay()

def render():
    """
    Renders the graph. Draws each node with diameter correlated to it's degree and position according to it's position attribute. 
    """
    glutInit()
    glutInitWindowSize(400,400)
    glutInitWindowPosition(10,10)
    glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE|GLUT_DEPTH)
    
    glutCreateWindow("Graph")
    
    glutReshapeFunc(__resize)
    glutDisplayFunc(__display)
    glutKeyboardFunc(__keyboard)
    glutMouseFunc(__mouse_button)
    glutMotionFunc(__mouse_motion)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    glutMainLoop()

    """    
    points = []
    
    for node in graph:
        position = node.position
        points += [p for p in get_circle_points(position[0], position[1], node.degree())]

    pyglet.graphics.draw(len(points), pyglet.gl.GL_POINTS, ('v2i', points))
        
    pyglet.app.run()
    """
    
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step
    
def get_circle_points(x,y,diameter):
    points = []
    r = diameter / 2.0
    for i in drange(0,r,0.1):
        for j in drange(0,2.0*math.pi,0.01):
            x, y = r*math.cos(j), r*math.sin(j)
            points.append((x, y))
            
    unique = set([(int(x),int(y)) for x, y in points])
    
    print "non, unique: %s, %s" % len(points), len(unique)
    
    return unique