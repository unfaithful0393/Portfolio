import sys

import pygame

class Mandelbrot:
    def __init__(self, width, height, max_iter):
        self.iterup = False
        self.iterdown = False
        self.width = width
        self.height = height
        self.max_iter = max_iter
        #make screen size half of the width and height of the screen
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen.fill((0, 0, 0))
        self.zoom = 1
        self.x_offset = 0
        self.y_offset = 0
        self.zoom_speed = 0.1
        self.offset_speed = 0.1
        self.zoom_in = False
        self.zoom_out = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.running = True
        self.paused = False
        self.color = (255, 255, 255)
        self.color_speed = 1
        self.color_increasing = True
        self.color_index = 0

    def run(self):
        #limit to 60 fps
        clock = pygame.time.Clock()
        clock.tick(30)
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    self.running = False
                if key == pygame.K_w:
                    self.iterup = True
                if key == pygame.K_s:
                    self.iterdown = True
                if key == pygame.K_SPACE:
                    self.paused = not self.paused
                if key == pygame.K_UP:
                    self.move_up = True
                if key == pygame.K_DOWN:
                    self.move_down = True
                if key == pygame.K_LEFT:
                    self.move_left = True
                if key == pygame.K_RIGHT:
                    self.move_right = True
                if key == pygame.K_EQUALS:
                    self.zoom_in = True
                if key == pygame.K_MINUS:
                    self.zoom_out = True
                if key == pygame.K_c:
                    self.color_increasing = not self.color_increasing
            if event.type == pygame.KEYUP:
                key = event.key
                if key == pygame.K_UP:
                    self.move_up = False
                if key == pygame.K_DOWN:
                    self.move_down = False
                if key == pygame.K_LEFT:
                    self.move_left = False
                if key == pygame.K_RIGHT:
                    self.move_right = False
                if key == pygame.K_EQUALS:
                    self.zoom_in = False
                if key == pygame.K_MINUS:
                    self.zoom_out = False
                if key == pygame.K_w:
                    self.iterup = False
                if key == pygame.K_s:
                    self.iterdown = False

    def update(self):
        if self.iterup:
            self.max_iter += int(self.max_iter * 0.1)+1
        if self.iterdown:
            self.max_iter -= int(self.max_iter * 0.1)

        if self.zoom_in:
            self.zoom += self.zoom_speed*self.zoom
        if self.zoom_out:
            self.zoom -= self.zoom_speed*self.zoom
        if self.move_up:
            self.y_offset -= self.offset_speed/self.zoom
        if self.move_down:
            self.y_offset += self.offset_speed/self.zoom
        if self.move_left:
            self.x_offset -= self.offset_speed/self.zoom
        if self.move_right:
            self.x_offset += self.offset_speed/self.zoom
        if self.color_increasing:
            self.color_index += self.color_speed % 255
        else:
            self.color_index -= self.color_speed
        self.color = pygame.Color(0)
        self.color.hsva = (self.color_index % 360, 100, 100, 100)

    def draw(self):
        # Stretch the image to the size of the screen
        self.screen.fill((0, 0, 0))
        for x in range(self.width):
            for y in range(self.height):
                c = complex((x - self.width / 2) / (self.zoom * self.width / 4) + self.x_offset,
                            (y - self.height / 2) / (self.zoom * self.height / 4) + self.y_offset)
                z = 0
                for i in range(self.max_iter):
                    z = z * z + c
                    if abs(z) > 2:
                        break
                else:
                    continue
                # Scale the x and y coordinates to the size of the screen

                self.screen.set_at((int(x * self.screen.get_width() / self.width), int(y * self.screen.get_height()
                                                                                        / self.height)), self.color)
                # self.screen.set_at((x, y), self.color)

if __name__ == '__main__':
    pygame.init()
    mandelbrot = Mandelbrot(150, 100, 1)
    mandelbrot.run()
