import pygame
import math

import port
class Shape():
    def __init__(self, pos, size, color, bevel, surface, run_function,id):
        self.surface = surface
        self.pos = pos
        self.size = size
        self.color = color
        self.bevel = bevel
        self.run_function = run_function
        self.id = id
        self.normal_color = color
        self.toggle_color = pygame.Color(0,60,60,255)

    def reset_color(self):
        self.color = self.normal_color 

    def clicked(self):

        self.color = self.toggle_color

    def draw(self):
            pygame.draw.rect(self.surface, self.color, 
                             (self.pos[0], self.pos[1], self.size[0], self.size[1]), 0,
                             self.bevel,self.bevel,self.bevel,self.bevel)


class Text():
    def __init__(self,text,pos,size,surface,id):
        self.surface = surface
        self.text = text
        self.pos = pos
        self.size = size
        self.id = id
        self.width = None
        self.height = None
        self.age = 0

    def blink(self,dt):
        self.age += dt
        if math.sin(math.radians(self.age/3)) > 0:
            self.text = self.text + "|"
        else:
            pass
    
    def draw(self):
        font = pygame.font.Font("freesansbold.ttf", self.size)
        text = font.render(self.text, True, "White")
        self.width = text.get_width()
        self.height = text.get_height()
        self.surface.blit(text, self.pos)


class GUI():
    def __init__(self,surface):
        self.surface = surface
        self.shapes = []
        self.text = []
        self.info = {}

    def check_shape_clicked(self,pos):
        for shape in self.shapes:
            if shape.id != None:
                if (shape.pos[0] < pos[0] and (shape.pos[0] + shape.size[0]) > pos[0] and 
                    shape.pos[1] < pos[1] and (shape.pos[1] + shape.size[1]) > pos[1]):
                        self._clear_shape_toggle(shape.id)
                        shape.clicked()
                        if shape.id == "OS,export":
                            self.loading_icon(pos=(180,430),id="Load,None")
                        return shape.run_function

    def check_text_clicked(self,pos):
        for text in self.text:
            if text.id != None:
                if (text.pos[0] < pos[0] and (text.pos[0] + text.width) > pos[0] and 
                    text.pos[1] < pos[1] and (text.pos[1] + text.height) > pos[1]):
                        return True,text
        return False, None
    
    def update_import_data(self,name,res,color,format):
        self._clear_shape_toggle("OS")
        self._clear_shape_toggle("Color_Space")
        self._clear_shape_toggle("Format")
        for text in self.text:
            if text.id != None:
                if text.id == "Name":
                    text.text = str(name)
                elif text.id == "X":
                    text.text = str(res[0])
                elif text.id == "Y":
                    text.text = str(res[1])
        for shape in self.shapes:
            if shape.id != None:
                split_id = shape.id.split(",")[1]
                if split_id == color or split_id == format:
                    shape.color = shape.toggle_color

    def edit_text(self, new_text, text,dt):
        text.text = new_text
        if dt != None:
            text.blink(dt)

    def _clear_shape_toggle(self,id):
        for shape in self.shapes:
            if str(shape.id).split(",")[0] == str(id).split(",")[0]:
                shape.reset_color()
         
    def read_gui_data(self):
        self._clear_shape_toggle("OS")
        for text in self.text:
            if text.id != None:
                self.info[text.id] = text.text
        for shape in self.shapes:
            if shape.id != None:
                group,id = str(shape.id).split(",")
                if group != "OS" and shape.color == shape.toggle_color:
                    self.info[group] = id
        return self.info

    def loading_icon(self,pos,id):
        self.define_shape(pos=pos,size=(30,30),color="White",bevel=30,id=id)
        self.define_shape(pos=(pos[0]+5,pos[1]+5),size=(20,20),color=pygame.Color(25,25,25,0),bevel=30,id=id)

    def load_destroy(self):
        for shape in self.shapes:
            if shape.id == "Load,None":
                self.shapes.remove(shape)

    def define_shape(self,pos, size, color=pygame.Color(0,102,102,255), bevel=25, run_function=None, id=None):
        shape = Shape(pos=pos,size=size, color=color,bevel=bevel,surface=self.surface, run_function=run_function,id=id)
        self.shapes.append(shape)
        
    def define_text(self, text, pos, size=16,id=None):
        text = Text(text=text, pos=pos, size=size, surface=self.surface, id=id)
        self.text.append(text)

    def draw(self):
        for shape in self.shapes:
            shape.draw()
        for text in self.text:
            text.draw()


def gui_init(art):
        art.define_shape(pos=(20,20), size=(360,460), color=pygame.Color(25,25,25,255), bevel=30)
        art.define_shape(pos=(25,88), size=(350,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.define_text(text="MediaMaster:",pos=(15,15),size=24)
        art.define_text(text="Name:",pos=(40,101))
        art.define_text(text="____",pos=(100,101),id="Name")

        art.define_shape(pos=(25,138), size=(350,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.define_shape(pos=(160,143), size=(70,30))
        art.define_shape(pos=(280,143), size=(70,30))
        art.define_text(text="X",pos=(250,151),size=14)
        art.define_text(text="____",pos=(175,151),id="X")
        art.define_text(text="____",pos=(295,151),id="Y")
        art.define_text(text="Resolution:",pos=(40,151))
        
        art.define_shape(pos=(25,188), size=(350,40), color=pygame.Color(40,40,40,255), bevel=20)
        art.define_shape(pos=(155,193), size=(60,30),id="Color_Space,RGB")
        art.define_shape(pos=(225,193), size=(60,30),id="Color_Space,RGBA")
        art.define_shape(pos=(295,193), size=(60,30),id="Color_Space,L")
        art.define_text(text="Color Space:",pos=(40,201))
        art.define_text(text=f"RGB{" "*13}RGBA{" "*12}Grey",pos=(172,202),size=12)

        art.define_shape(pos=(25,238), size=(350,165), color=pygame.Color(40,40,40,255), bevel=20)
        art.define_shape(pos=(110,245), size=(55,30),id="Format,png")
        art.define_shape(pos=(175,245), size=(55,30),id="Format,jpg")
        art.define_shape(pos=(240,245), size=(55,30),id="Format,jpeg")
        art.define_shape(pos=(305,245), size=(55,30),id="Format,bmp")
        art.define_shape(pos=(45,285), size=(55,30),id="Format,webp")
        art.define_shape(pos=(110,285), size=(55,30),id="Format,heic")
        art.define_shape(pos=(175,285), size=(55,30),id="Format,gif")
        art.define_shape(pos=(240,285), size=(55,30),id="Format,tif")
        art.define_shape(pos=(305,285), size=(55,30),id="Format,mp4")
        art.define_shape(pos=(45,325), size=(55,30),id="Format,avi")
        art.define_shape(pos=(110,325), size=(55,30),id="Format,mov")
        art.define_shape(pos=(175,325), size=(55,30),id="Format,mkv")
        art.define_shape(pos=(240,325), size=(55,30),id="Format,webp")
        art.define_shape(pos=(305,325), size=(55,30),id="Format,wmv")
        art.define_shape(pos=(45,365), size=(55,30),id="Format,flv")
        art.define_shape(pos=(110,365), size=(55,30),id="Format,ogv")
        art.define_shape(pos=(175,365), size=(55,30),id="Format,mpeg")
        art.define_shape(pos=(240,365), size=(55,30),id="Format,m4v")
        art.define_text(text="Format:",pos=(40,251))
        art.define_text(text=f"PNG{" "*13}JPG{" "*13}JPEG{" "*12}BMP",pos=(124,255),size=12) 
        art.define_text(text=f"WebP{" "*11}HEIC{" "*13}GIF{" "*16}TIF{" "*14}MP4",pos=(57,295),size=12)
        art.define_text(text=f"AVI{" "*14}MOV{" "*13}MKV{" "*11}WEBP{" "*11}WMV",pos=(62,335),size=12)
        art.define_text(text=f"FLV{" "*14}OGV{" "*12}MPEG{" "*11}M4V",pos=(62,375),size=12)

        art.define_shape(pos=(40,423), size=(80,40), bevel=15,run_function="file_import(art)", id="OS,import")
        art.define_shape(pos=(280,423), size=(80,40), bevel=15,run_function="file_export(art)", id="OS,export")
        art.define_text(text=f"Load{" "*49}Export",pos=(59,436))

def file_import(art):
    file_path = port.import_file()
    name,res,color,format = port.fetch_data(file_path)
    art.update_import_data(name,res,color,format)
    art.info["Path"] = file_path

def file_export(art):
    data = art.read_gui_data()
    port.save(data)
    art.load_destroy()

def main():
    #initialization
    pygame.init()
    pygame.display.set_caption("MediaMaster")
    resolution = (400,500)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    new_text = ""
    dt = 0
    is_running = True
    is_typing = False
    run_function = None
    art = GUI(screen)
    gui_init(art)

    #event loop
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                run_function = art.check_shape_clicked(pos)
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

                if is_typing == False:
                    art.edit_text(new_text=new_text, text=text,dt=None)
                    if len(new_text) == 0:
                        art.edit_text(new_text="____", text=text,dt=None)
                    new_text = ""
                    

    #Game loop
        if is_typing:
            art.edit_text(new_text=new_text, text=text,dt=dt)
        screen.fill(pygame.Color(30,30,30,255))
        art.draw()
        pygame.display.flip()
        exec(f"{run_function}")
        run_function = None
        dt = clock.tick(12)
    pygame.quit()


if __name__ == "__main__":
    main()