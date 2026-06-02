# render.py

import turtle
import keyboard

from math import *
from time import perf_counter

from obj_loader import load_obj

# ============================================
# SETUP
# ============================================

WIDTH = 1280
HEIGHT = 720

turtle.setup(WIDTH, HEIGHT)

screen = turtle.Screen()
screen.bgcolor("#22252b")

turtle.colormode(255)
turtle.tracer(0, 0)

t = turtle.Turtle()

t.hideturtle()
t.speed(0)
t.penup()
t.pencolor((0, 0, 0))

FOCAL_LENGTH = 500
NEAR_PLANE = 0.1

# ============================================
# CAMERA
# ============================================

camera_x = 0
camera_y = 0
camera_z = -5

rot_h = 0
rot_v = 0

sin_h = 0
cos_h = 1

sin_v = 0
cos_v = 1

# ============================================
# LIGHT
# ============================================

light_x = 0
light_y = 0
light_z = 1

light_len = sqrt(
    light_x * light_x +
    light_y * light_y +
    light_z * light_z
)

light_x /= light_len
light_y /= light_len
light_z /= light_len

# ============================================
# LOAD MODEL
# ============================================

verts, normals, tris = load_obj("monkey.obj")

# ============================================
# CALCULATE TRIG
# ============================================

def calculate_trig():

    global sin_h
    global cos_h

    global sin_v
    global cos_v

    sin_h = sin(rot_h)
    cos_h = cos(rot_h)

    sin_v = sin(rot_v)
    cos_v = cos(rot_v)

# ============================================
# UPDATE LIGHT
# ============================================

def update_light():

    global light_x
    global light_y
    global light_z

    light_x = sin_h * cos_v
    light_y = sin_v
    light_z = cos_h * cos_v

    length = sqrt(
        light_x * light_x +
        light_y * light_y +
        light_z * light_z
    )

    if length != 0:

        light_x /= length
        light_y /= length
        light_z /= length

# ============================================
# TRANSFORM POINT
# ============================================

def transform_point(x, y, z):

    # relative to camera

    x -= camera_x
    y -= camera_y
    z -= camera_z

    # horizontal rotation

    tx = (x * cos_h) - (z * sin_h)
    tz = (z * cos_h) + (x * sin_h)

    x = tx
    z = tz

    # vertical rotation

    ty = (y * cos_v) - (z * sin_v)
    tz = (z * cos_v) + (y * sin_v)

    y = ty
    z = tz

    return x, y, z

# ============================================
# PROJECT
# ============================================

def project(x, y, z):

    sx = (x / z) * FOCAL_LENGTH
    sy = (y / z) * FOCAL_LENGTH

    return sx, sy

# ============================================
# LIGHTING
# ============================================

def normal_brightness(nx, ny, nz):

    brightness = -(
        nx * light_x +
        ny * light_y +
        nz * light_z
    )

    brightness = (brightness + 1) * 0.5

    brightness = max(0.2, brightness)

    return brightness

# ============================================
# DRAW TRIANGLE
# ============================================

def draw_triangle(tri):

    v1_i, v2_i, v3_i, n1_i, n2_i, n3_i = tri

    # ========================================
    # VERTICES
    # ========================================

    v1 = verts[v1_i]
    v2 = verts[v2_i]
    v3 = verts[v3_i]

    # ========================================
    # NORMALS
    # ========================================

    n1 = normals[n1_i]
    n2 = normals[n2_i]
    n3 = normals[n3_i]

    # averaged normal

    nx = (n1[0] + n2[0] + n3[0]) / 3
    ny = (n1[1] + n2[1] + n3[1]) / 3
    nz = (n1[2] + n2[2] + n3[2]) / 3

    length = sqrt(
        nx * nx +
        ny * ny +
        nz * nz
    )

    if length == 0:
        return

    nx /= length
    ny /= length
    nz /= length

    # ========================================
    # TRANSFORM
    # ========================================

    x1, y1, z1 = transform_point(*v1)
    x2, y2, z2 = transform_point(*v2)
    x3, y3, z3 = transform_point(*v3)

    # ========================================
    # CLIPPING
    # ========================================

    if (
        z1 <= NEAR_PLANE or
        z2 <= NEAR_PLANE or
        z3 <= NEAR_PLANE
    ):
        return

    # ========================================
    # PROJECT
    # ========================================

    sx1, sy1 = project(x1, y1, z1)
    sx2, sy2 = project(x2, y2, z2)
    sx3, sy3 = project(x3, y3, z3)

    # ========================================
    # BACKFACE CULLING
    # ========================================

    cross = (
        (sx2 - sx1) * (sy3 - sy1)
        -
        (sy2 - sy1) * (sx3 - sx1)
    )

    if cross > 0:
        return

    # ========================================
    # LIGHTING
    # ========================================

    brightness = normal_brightness(
        nx,
        ny,
        nz
    )

    # ========================================
    # FOG
    # ========================================

    avg_z = (
        z1 +
        z2 +
        z3
    ) / 3

    fog = min(
        0.45,
        avg_z / 80
    )

    # ========================================
    # BASE COLOR
    # ========================================

    base_r = 180
    base_g = 210
    base_b = 255

    # ========================================
    # APPLY LIGHT
    # ========================================

    r = int(base_r * brightness)
    g = int(base_g * brightness)
    b = int(base_b * brightness)

    # ========================================
    # APPLY FOG
    # ========================================

    fog_r = 31
    fog_g = 36
    fog_b = 44

    r = int((r * (1 - fog)) + (fog_r * fog))
    g = int((g * (1 - fog)) + (fog_g * fog))
    b = int((b * (1 - fog)) + (fog_b * fog))

    # clamp

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    # ========================================
    # DRAW
    # ========================================

    t.fillcolor((r, g, b))

    t.goto(sx1, sy1)

    t.begin_fill()

    t.goto(sx2, sy2)
    t.goto(sx3, sy3)
    t.goto(sx1, sy1)

    t.end_fill()

# ============================================
# DRAW MODEL
# ============================================

def draw_model():

    tri_depth = []

    for tri in tris:

        v1_i, v2_i, v3_i, _, _, _ = tri

        v1 = verts[v1_i]
        v2 = verts[v2_i]
        v3 = verts[v3_i]

        z = (
            transform_point(*v1)[2] +
            transform_point(*v2)[2] +
            transform_point(*v3)[2]
        ) / 3

        tri_depth.append((z, tri))

    # painter algorithm

    tri_depth.sort(reverse=True)

    for _, tri in tri_depth:

        draw_triangle(tri)

# ============================================
# CONTROLS
# ============================================

def controls(delta):

    global camera_x
    global camera_y
    global camera_z

    global rot_h
    global rot_v

    move_speed = 0.05 * delta
    rot_speed = 0.03 * delta

    # movement

    keyboard.add_hotkey("w", lambda: camera_x + sin_h * move_speed, camera_z + cos_h * move_speed)



    if keyboard.is_pressed("s"):

        camera_x -= sin_h * move_speed
        camera_z -= cos_h * move_speed

    if keyboard.is_pressed("a"):

        camera_x -= cos_h * move_speed
        camera_z += sin_h * move_speed

    if keyboard.is_pressed("d"):

        camera_x += cos_h * move_speed
        camera_z -= sin_h * move_speed

    if keyboard.is_pressed("space"):

        camera_y += move_speed

    if keyboard.is_pressed("shift"):

        camera_y -= move_speed

    # rotation

    if keyboard.is_pressed("left"):
        rot_h -= rot_speed

    if keyboard.is_pressed("right"):
        rot_h += rot_speed

    if keyboard.is_pressed("up"):
        rot_v += rot_speed

    if keyboard.is_pressed("down"):
        rot_v -= rot_speed

    # clamp

    if rot_v > pi / 2:
        rot_v = pi / 2

    if rot_v < -pi / 2:
        rot_v = -pi / 2

# ============================================
# MAIN LOOP
# ============================================

running = True

last_time = perf_counter()

while running:

    current_time = perf_counter()

    delta = current_time - last_time

    last_time = current_time

    delta *= 75

    try:

        t.clear()

        controls(delta)

        calculate_trig()
        update_light()

        draw_model()

        turtle.update()

    except turtle.Terminator:

        running = False

    except Exception as e:

        print(e)

        running = False