import pygame

class Shape():
    def __init__(self, pos, size, color, bevel, surface, run_function):
        self.surface = surface
        self.pos = pos
        self.size = size
        self.color = color
        self.bevel = bevel
        self.run_function = run_function

    def draw(self):
            pygame.draw.rect(self.surface, self.color, 
                             (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0,
                             self.bevel,self.bevel,self.bevel,self.bevel)


class Text():
    def __init__(self,text,pos,size,color,font,surface):
        self.surface = surface
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.font = font

    def draw(self):
        font = pygame.font.Font(self.font, self.size)
        text = font.render(self.text, True, self.color)
        self.surface.blit(text, self.pos)


class Shapes():
    def __init__(self,surface):
        self.surface = surface
        self.shapes = []
        self.text = []

    def update(self,pos):
        for shape in self.shapes:
            if shape.pos[0] < pos[0] and (shape.pos[0] + shape.size[0]) > pos[0]:
                if shape.pos[1] < pos[1] and (shape.pos[1] + shape.size[1]) > pos[1]:
                    exec(f"{shape.run_function}")
                    return

    def defineShape(self,pos=(0,0), size=(100,100), color="White", bevel=10, run_function=None):
        shape = Shape(pos=pos,size=size, color=color,bevel=bevel,surface=self.surface, run_function=run_function)
        self.shapes.append(shape)
        
    def defineText(self,text="placeholder",pos=(0,0), size=32, color="White",font="freesansbold.ttf"):
        text = Text(pos=pos, text=text, size=size, color=color, surface=self.surface,font=font)
        self.text.append(text)

    def draw(self):
        for shape in self.shapes:
            shape.draw()
        for text in self.text:
            text.draw()


def art_init(art,resolution):
        green = pygame.Color(0,102,102,255)
        art.defineShape(pos=(20,20), size=(resolution[0]-40,resolution[1]-40), color=pygame.Color(25,25,25,255), bevel=30)
        art.defineShape(pos=(25,88), size=(resolution[0]-50,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.defineShape(pos=(25,138), size=(resolution[0]-50,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.defineShape(pos=(25,188), size=(resolution[0]-50,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.defineShape(pos=(25,238), size=(resolution[0]-50,40), color=pygame.Color(40,40,40,255), bevel=20)

        art.defineShape(pos=(160,143), size=(70,30), color=green, bevel=25)
        art.defineShape(pos=(280,143), size=(70,30), color=green, bevel=25)
        art.defineShape(pos=(40,423), size=(80,40), color=green, bevel=15)
        art.defineShape(pos=(280,423), size=(80,40), color=green, bevel=15)

        art.defineText(text="MediaMaster:",pos=(15,15),size=24)
        art.defineText(text="Name:",pos=(40,101),size=16)
        art.defineText(text="Resolution:",pos=(40,151),size=16)
        art.defineText(text="X",pos=(250,151),size=14)
        art.defineText(text="Color Space:",pos=(40,201),size=16)
        art.defineText(text="Format:",pos=(40,251),size=16)
        art.defineText(text="Load",pos=(59,436),size=16)
        art.defineText(text="Export",pos=(293,436),size=16)


def main():
    pygame.init()
    pygame.display.set_caption("MediaMaster")
    resolution = (400,500)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    is_running = True
    art = Shapes(screen)
    art_init(art,resolution)
    #event loop
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                art.update(pos)

    #Game loop
        screen.fill(pygame.Color(30,30,30,255))
        art.draw()
        pygame.display.flip()
        clock.tick(12)
    pygame.quit()


if __name__ == "__main__":
    main()