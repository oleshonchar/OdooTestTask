from PIL import Image, ImageDraw
from math import cos, sin, pi


def get_coords(r, t):
    return int(r*cos(t)), int(r*sin(t))


def translate(point, screen_size):
    return point[0] + screen_size / 2, point[1] + screen_size


def draw_wave(a, b, img, step=0.1, loops=500):
    draw = ImageDraw.Draw(img)
    t = 0.0
    r = a
    prev_pos = get_coords(r, t)
    while t < 2 * loops * pi:

        t += step
        r = a + b * t

        pos = get_coords(r, t)
        draw.line(translate(prev_pos, img.size[0]) + translate(pos, img.size[0]), fill=10)
        prev_pos = pos


if __name__ == "__main__":

    image = Image.open('image.jpg')
    draw_wave(0, 1, image)
    image.save('transformed.jpg')
