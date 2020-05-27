from PIL import Image, ImageColor
from PIL import ImageDraw
from Point import Point



Cw = 600 # Ширина холста
Ch = 600 # Высота холста

red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
BACKGROUND_COLOR = (255,255,255)

def PutPixel(x, y, color):
    draw.point((Cw/2+x,Ch/2-y), fill=color)

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
            print(P0.x, P0.y)
            P0, P1 = swap_point(P0, P1)
            print(P0.x, P0.y)
        ys = Interpolate(P0.x, P0.y, P1.x, P1.y)
        print(ys)
        for x in range(P0.x, P1.x):
            PutPixel(x, ys[x-P0.x], color)
    else:
        if P0.y > P1.y:
            print(P0.x, P0.y)
            P0, P1 = swap_point(P0, P1)
            print(P0.x, P0.y)
        xs = Interpolate(P0.y, P0.x, P1.y, P1.x)
        print(xs)
        for y in range(P0.y, P1.y):
            PutPixel(xs[y-P0.y], y, color)

def Interpolate(i0, d0, i1, d1):
    if i0==i1:
        return [d0]
    values = []
    a = (d1 - d0)/(i1-i0)
    d = d0
    for i in range(i0, i1):
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


image = Image.new("RGB", (Cw, Ch))
draw = ImageDraw.Draw(image)

P0 = Point(-200,100)
P1 = Point(-200,120)

P3 = Point(60,240)
P4 = Point(-50,240)
DrawWireframeTriangle(P1,P3, P4, red)
DrawFilledTriangle(P1,P3, P4, red)
#DrawWireframeTriangle(P0,P1, P4, blue)




image.show()