from PIL import Image, ImageColor
from PIL import ImageDraw
from Point import Point



Cw = 1200 # Ширина холста
Ch = 1200 # Высота холста

Vw = 10
Vh = 10
d = 1

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
PURPLE = (160,32,240)
CYAN = (0,255,255)
BACKGROUND_COLOR = (255,255,255)

P0 = Point(-200,100, 0.8)
P1 = Point(-200,120, 0.7)
P3 = Point(60,240, 0.2)
P4 = Point(-50,240,0.4)

# Четыре "передних" вершины.
vAf = [-1, 1, 1]
vBf = [1, 1, 1]
vCf = [1, -1, 1]
vDf = [-1, -1, 1]

  # Четыре "задних" вершины.
vAb = [-1, 1, 2]
vBb = [1, 1, 2]
vCb = [1, -1, 2]
vDb = [-1, -1, 2]

vertexes = [
    ( 1,  1,  1),
    (-1,  1,  1),
    (-1, -1,  1),
    ( 1, -1,  1),
    ( 1,  1, -1),
    (-1,  1, -1),
    (-1, -1, -1),
    ( 1, -1, -1)
]

Triangles = [
    (0, 1, 2, RED),
    (0, 2, 3, RED),
    (4, 0, 3, GREEN),
    (4, 3, 7, GREEN),
    (5, 4, 7, BLUE),
    (5, 7, 6, BLUE),
    (1, 5, 6, YELLOW),
    (1, 6, 2, YELLOW),
    (4, 5, 1, PURPLE),
    (4, 1, 0, PURPLE),
    (2, 6, 7, CYAN),
    (2, 7, 3, CYAN)
]

def RenderObject(vertexes, triangles):
    projected = []
    for V in vertexes:
        print(V)
        projected.append(ProjectVertex(V))
    print(projected)
    for T in triangles:
        RenderTriangle(T, projected)
    

def RenderTriangle(triangle, projected):
    print(triangle)
    print(projected[triangle[0]].x)
    DrawWireframeTriangle(projected[triangle[0]],
                          projected[triangle[1]],
                          projected[triangle[2]],
                          triangle[3])



def ViewportToCanvas(x,y):
    return Point(x*Cw/Vw, y*Ch/Vh)

def ProjectVertex(v):
    return ViewportToCanvas(v[0]*d/v[2], v[1]*d/v[2])

def PutPixel(x, y, color):
    draw.point((Cw/2+x,Ch/2-y), fill=color)

def vector_multiply(A, c):
    return tuple(map(lambda x: int(x*c), A))

def swap_point(A, B):
    P_t = A
    A = B
    B = P_t
    return A, B

def DrawLine(P0, P1, color):
    dx = P1.x - P0.x
    dy = P1.y - P0.y

    if abs(dx) > abs(dy):
        if P0.x > P1.x:
            P0, P1 = swap_point(P0, P1)
        ys = Interpolate(P0.x, P0.y, P1.x, P1.y)
        for x in range(int(P0.x), int(P1.x)):
            PutPixel(x, ys[int(x-P0.x)], color)
    else:
        if P0.y > P1.y:
            P0, P1 = swap_point(P0, P1)
        xs = Interpolate(P0.y, P0.x, P1.y, P1.x)
        for y in range(int(P0.y), int(P1.y)):
            PutPixel(xs[int(y-P0.y)], y, color)

def Interpolate(i0, d0, i1, d1):
    if i0==i1:
        return [d0]
    values = []
    a = int(d1 - d0)/(i1-i0)
    d = d0
    for i in range(int(i0), int(i1)):
        values.append(d)
        d = d + a
    return values

def DrawWireframeTriangle (P0, P1, P2, color):
    DrawLine(P0, P1, color)
    DrawLine(P1, P2, color)
    DrawLine(P2, P0, color)
def DrawFilledTriangle (P0, P1, P2, color):
    # Сортировка точек так, что y0 <= y1 <= y2
    if P1.y < P0.y:
         swap_point(P1, P0)
    if P2.y < P0.y:
         swap_point(P2, P0)
    if P2.y < P1.y:
        swap_point(P2, P1)

    # Вычисление координат x рёбер треугольника
    x01 = Interpolate(P0.y, P0.x, P1.y, P1.x)
    x12 = Interpolate(P1.y, P1.x, P2.y, P2.x)
    x02 = Interpolate(P0.y, P0.x, P2.y, P2.x)
    # Конкатенация коротких сторон
    x01= x01[:-1]
    x012 = x01 + x12

    # Определяем, какая из сторон левая и правая
    m = int(len(x012) / 2)
    if x02[m] < x012[m]: 
        x_left = x02
        x_right = x012
    else:
        x_left = x012
        x_right = x02

    # Отрисовка горизонтальных отрезков
    for y in range(P0.y, P2.y):
        for x in range(int(x_left[y - P0.y]), int(x_right[y - P0.y])):
            PutPixel(x, y, color)

def DrawShadedTriangle (P0, P1, P2, color):
    # Сортировка точек так, что y0 <= y1 <= y2
    if P1.y < P0.y:
         swap_point(P1, P0)
    if P2.y < P0.y:
         swap_point(P2, P0)
    if P2.y < P1.y:
        swap_point(P2, P1)

    # Вычисление координат x рёбер треугольника
    x01 = Interpolate(P0.y, P0.x, P1.y, P1.x)
    h01 = Interpolate(P0.y, P0.h, P1.y, P1.h)

    x12 = Interpolate(P1.y, P1.x, P2.y, P2.x)
    h12 = Interpolate(P1.y, P1.h, P2.y, P2.h)

    x02 = Interpolate(P0.y, P0.x, P2.y, P2.x)
    h02 = Interpolate(P0.y, P0.h, P2.y, P2.h)
    # Конкатенация коротких сторон
    x01= x01[:-1]
    x012 = x01 + x12

    h01 = h01[:-1]
    h012 = h01 + h12

    # Определяем, какая из сторон левая и правая
    m = int(len(x012) / 2)
    if x02[m] < x012[m]: 
        x_left = x02
        x_right = x012

        h_left = h02
        h_right = h012
    else:
        x_left = x012
        x_right = x02

        h_left = h012
        h_right = h02

    # Отрисовка горизонтальных отрезков
    for y in range(P0.y, P2.y):
        x_l = int(x_left[y - P0.y])
        x_r = int(x_right[y - P0.y])

        h_segment = Interpolate(x_l, h_left[y - P0.y], x_r, h_right[y - P0.y])
        for x in range(x_l, x_r):
            shaded_color = vector_multiply(color, h_segment[x - x_l])
            PutPixel(x, y, shaded_color)


image = Image.new("RGB", (Cw, Ch))
draw = ImageDraw.Draw(image)


#DrawWireframeTriangle(P1,P3, P4, red)
#DrawShadedTriangle(P1,P3, P4, red)
#DrawWireframeTriangle(P0,P1, P4, blue)

# Передняя грань.
def DrawCube():
    # Передняя грань.
    DrawLine(ProjectVertex(vAf), ProjectVertex(vBf), BLUE)
    DrawLine(ProjectVertex(vBf), ProjectVertex(vCf), BLUE)
    DrawLine(ProjectVertex(vCf), ProjectVertex(vDf), BLUE)
    DrawLine(ProjectVertex(vDf), ProjectVertex(vAf), BLUE)

     # Задняя грань.
    DrawLine(ProjectVertex(vAb), ProjectVertex(vBb), RED)
    DrawLine(ProjectVertex(vBb), ProjectVertex(vCb), RED)
    DrawLine(ProjectVertex(vCb), ProjectVertex(vDb), RED)
    DrawLine(ProjectVertex(vDb), ProjectVertex(vAb), RED)

  # Рёбра, соединяющие переднюю и заднюю грани.
    DrawLine(ProjectVertex(vAf), ProjectVertex(vAb), GREEN)
    DrawLine(ProjectVertex(vBf), ProjectVertex(vBb), GREEN)
    DrawLine(ProjectVertex(vCf), ProjectVertex(vCb), GREEN)
    DrawLine(ProjectVertex(vDf), ProjectVertex(vDb), GREEN)
RenderObject(vertexes, Triangles)

image.show()