import pygame

class Shape():
    def __init__(self, pos, size, color, bevel, surface, run_function,group):
        self.surface = surface
        self.pos = pos
        self.size = size
        self.color = color
        self.bevel = bevel
        self.run_function = run_function
        self.group = group

    def draw(self):
            pygame.draw.rect(self.surface, self.color, 
                             (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0,
                             self.bevel,self.bevel,self.bevel,self.bevel)


class Text():
    def __init__(self,text,pos,size,font,surface,editable):
        self.surface = surface
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.editable = editable
        self.width = None
        self.height = None

    def draw(self):
        font = pygame.font.Font(self.font, self.size)
        text = font.render(self.text, True, "White")
        self.width = text.get_width()
        self.height = text.get_height()
        self.surface.blit(text, self.pos)


class ArtObjects():
    def __init__(self,surface):
        self.surface = surface
        self.shapes = []
        self.text = []

    def check_shape_clicked(self,pos):
        for shape in self.shapes:
            if shape.group != None:
                if (shape.pos[0] < pos[0] and (shape.pos[0] + shape.size[0]) > pos[0] and 
                    shape.pos[1] < pos[1] and (shape.pos[1] + shape.size[1]) > pos[1]):
                        self._clear_group_color(shape.group)
                        shape.color = pygame.Color(0,60,60,255)
                        exec(f"{shape.run_function}")

    def check_text_clicked(self,pos):
        for text in self.text:
            if text.editable == True:
                if (text.pos[0] < pos[0] and (text.pos[0] + text.width) > pos[0] and 
                    text.pos[1] < pos[1] and (text.pos[1] + text.height) > pos[1]):
                        return True,text
        return False, None
    
    def edit_text(self, new_text, text):
        text.text = new_text

    def _clear_group_color(self,id):
        for shape in self.shapes:
            if shape.group == id:
                shape.color = pygame.Color(0,102,102,255)
         
    def defineShape(self,pos, size, color=pygame.Color(0,102,102,255), bevel=25, run_function=None,group=None):
        shape = Shape(pos=pos,size=size, color=color,bevel=bevel,surface=self.surface, run_function=run_function,group=group)
        self.shapes.append(shape)
        
    def defineText(self, text, pos, size=16,font="freesansbold.ttf",editable=False):
        text = Text(pos=pos, text=text, size=size, surface=self.surface,font=font,editable=editable)
        self.text.append(text)

    def draw(self):
        for shape in self.shapes:
            shape.draw()
        for text in self.text:
            text.draw()


def art_init(art):
        
        art.defineShape(pos=(20,20), size=(360,460), color=pygame.Color(25,25,25,255), bevel=30)
        art.defineShape(pos=(25,88), size=(350,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.defineText(text="MediaMaster:",pos=(15,15),size=24)
        art.defineText(text="Name:",pos=(40,101))
        art.defineText(text="____",pos=(100,101),editable=True)

        art.defineShape(pos=(25,138), size=(350,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.defineShape(pos=(160,143), size=(70,30))
        art.defineShape(pos=(280,143), size=(70,30))
        art.defineText(text="X",pos=(250,151),size=14)
        art.defineText(text="____",pos=(175,151),editable=True)
        art.defineText(text="____",pos=(295,151),editable=True)
        art.defineText(text="Resolution:",pos=(40,151))
        
        art.defineShape(pos=(25,188), size=(350,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.defineShape(pos=(155,193), size=(60,30), group="Color_Space")
        art.defineShape(pos=(225,193), size=(60,30), group="Color_Space")
        art.defineShape(pos=(295,193), size=(60,30), group="Color_Space")
        art.defineText(text="Color Space:",pos=(40,201))
        art.defineText(text=f"RGB{" "*13}RGBA{" "*12}Grey",pos=(172,202),size=12)

        art.defineShape(pos=(25,238), size=(350,125), color=pygame.Color(40,40,40,255), bevel=20)
        art.defineShape(pos=(110,245), size=(55,30), group="Format")
        art.defineShape(pos=(175,245), size=(55,30), group="Format")
        art.defineShape(pos=(240,245), size=(55,30), group="Format")
        art.defineShape(pos=(305,245), size=(55,30), group="Format")
        art.defineShape(pos=(45,285), size=(55,30), group="Format")
        art.defineShape(pos=(110,285), size=(55,30), group="Format")
        art.defineShape(pos=(175,285), size=(55,30), group="Format")
        art.defineShape(pos=(240,285), size=(55,30), group="Format")
        art.defineShape(pos=(305,285), size=(55,30), group="Format")
        art.defineShape(pos=(45,325), size=(55,30), group="Format")
        art.defineShape(pos=(110,325), size=(55,30), group="Format")
        art.defineShape(pos=(175,325), size=(55,30), group="Format")
        #art.defineShape(pos=(240,325), size=(55,30), group="Format")
        #art.defineShape(pos=(305,325), size=(55,30), group="Format")
        art.defineText(text="Format:",pos=(40,251))
        art.defineText(text=f"PNG{" "*13}JPG{" "*13}JPEG{" "*12}BMP",pos=(124,255),size=12)
        art.defineText(text=f"WebP{" "*11}HEIC{" "*13}GIF{" "*15}TIFF{" "*13}mp4",pos=(57,295),size=12)
        art.defineText(text=f"AVI{" "*14}MOV{" "*13}MKV",pos=(62,335),size=12)

        art.defineShape(pos=(40,423), size=(80,40), bevel=15,run_function="file_import()", group="OS")
        art.defineShape(pos=(280,423), size=(80,40), bevel=15,run_function="file_export()", group="OS")
        art.defineText(text=f"Load{" "*49}Export",pos=(59,436))

def file_import():
    print("import")

def file_export():
    print("export")

def main():
    pygame.init()
    pygame.display.set_caption("MediaMaster")
    resolution = (400,500)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    is_running = True
    new_text = ""
    is_typing = False
    art = ArtObjects(screen)
    art_init(art)
    #event loop
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                art.check_shape_clicked(pos)
                if is_typing == False:
                    is_typing,text = art.check_text_clicked(pos)

            if is_typing == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        new_text += "_"
                    elif event.key == pygame.K_BACKSPACE:
                        new_text = new_text[:-1]
                    elif (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                        is_typing = False
                    else:
                        new_text += pygame.key.name(event.key)
                art.edit_text(new_text=new_text + "|", text=text)

                if is_typing == False:
                    art.edit_text(new_text=new_text, text=text)
                    if len(new_text) == 0:
                        art.edit_text(new_text="____", text=text)
                    new_text = ""
                    

    #Game loop
        screen.fill(pygame.Color(30,30,30,255))
        art.draw()
        pygame.display.flip()
        clock.tick(12)
    pygame.quit()


if __name__ == "__main__":
    main()