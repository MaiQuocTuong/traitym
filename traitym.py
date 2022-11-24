 
import random
from math import sin, cos, pi, log
from tkinter import *
CANVAS_WIDTH =  1000
CANVAS_HEIGHT =  850
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2 
IMAGE_ENLARGE = 11.5
HEART_COLOR = "#00BFFF"   #màu xanh dương , #FF1493:màu hồng ,   #8B0000: màu đỏ 

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):

    x = 13.14*(sin(t)**3)
    y = -(13.14 * cos(t) -4* cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    x *= shrink_ratio
    y *= shrink_ratio

 
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)
 

def scatter_inside(x, y, beta=0.520):

    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy


def shrink(x, y, ratio):
 
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):
  
    return 1.314*(4 * sin(3 * p)) / (3 * pi)

class Heart:
  

    def __init__(self, generate_frame=10):
        self._points = set()  
        self._edge_diffusion_points = set()  
        self._center_diffusion_points = set()  
        self.all_points = {}  
        self.build(5200)

        self.random_halo = 5200

        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
    
        for _ in range(number):
            t = random.uniform(0, 25 * pi)  
            x, y = heart_function(t)
            self._points.add((x, y))

       
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.1)
                self._edge_diffusion_points.add((x, y))

    
        point_list = list(self._points)
        for _ in range(5200):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.3)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        
        force = Heart.new_method(x, y)

        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-2, 3)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-2, 3)

        return x - dx, y - dy

    @staticmethod
    def new_method(x, y):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)  #tocdonhay
        return force

    def calc(self, generate_frame):
        ratio = 30 * curve(generate_frame / 10 * pi)  

        halo_radius = int(3 + 4 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(5200 + 1314 * abs(curve(generate_frame / 10 * pi) ** 3))

        all_points = []

      
        heart_halo_point = set()  
        for _ in range(halo_number):
            t = random.uniform(0, 35 * pi)  
            x, y = heart_function(t, shrink_ratio= 11.4)  
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
           
                heart_halo_point.add((x, y))
                x += random.randint(-13,13)
                y += random.randint(-13, 13)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

  
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

      
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(200, draw, main, render_canvas, render_heart, render_frame + 1)


if __name__ == '__main__':
    root = Tk()
    root.title("M nhất")  
    canvas = Canvas(root, bg='#000', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()  
    draw(root, canvas, heart)  
    root.mainloop()

