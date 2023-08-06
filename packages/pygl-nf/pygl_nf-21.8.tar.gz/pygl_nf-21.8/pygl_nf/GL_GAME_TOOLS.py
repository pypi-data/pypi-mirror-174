import pygame
import random
import math
from pygl_nf import GL_MATH,GL
import pygame
import time
import functools


def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        runtime = time.perf_counter() - start
        print(f"{func.__name__} took {runtime:.4f} secs")
        return result
    return _wrapper

class Ray():
    def __init__(self,max_length,shag,angl,pos) -> None:
        self.max_lenght = max_length
        self.shag = shag
        self.angl = math.radians(angl)
        self.pos = pos
        self.colide = False

        self.sx = 0
        self.sy = 0

    def Detect_to_rect_map_enum(self,map):
     
        for i in range(self.max_lenght//self.shag):

            self.colide = False
            sx = self.pos[0]+i*self.shag*math.sin(self.angl)
            sy = self.pos[1]+i*self.shag*math.cos(self.angl)
            for bindex,block in enumerate( map ):
                if block.collidepoint(sx,sy):
                    self.colide = True
                    break
                
            if self.colide:
                break
        
        return sx,sy,self.colide,bindex

    def Detect_to_rect_map(self,map):
     
        for i in range(self.max_lenght//self.shag):

            self.colide = False
            sx = self.pos[0]+i*self.shag*math.sin(self.angl)
            sy = self.pos[1]+i*self.shag*math.cos(self.angl)
            for block in map:
                
                if block.collidepoint(sx,sy):
                    self.colide = True
                    break
                
            if self.colide:
                break
        
        return sx,sy,self.colide

    def Set_angle(self,angle):
        self.angl = math.radians(angle)

    @property
    def angle(self):
        return math.degrees(self.angl)

    @property
    def dx(self):
        return self.sx

    @property
    def dy(self):
        return self.sy

class Colliders():
    def collide_rect_circle(rect_pos,rect_size,circle_pos,circle_size):
        colide = False

        rect_x, rect_y = rect_pos
        circle_x, circle_y = circle_pos
        rect_w, rect_h = rect_size
        circle_rad = circle_size

        p1_rast = GL_MATH.Math_().RAST(circle_pos,[rect_x,rect_y])
        p2_rast = GL_MATH.Math_().RAST(circle_pos,[rect_x+rect_w,rect_y])
        p3_rast = GL_MATH.Math_().RAST(circle_pos,[rect_x,rect_y+rect_h])
        p4_rast = GL_MATH.Math_().RAST(circle_pos,[rect_x+rect_w,rect_y+rect_h])
        if p1_rast<circle_rad:                                          colide = True
        elif p2_rast<circle_rad:                                        colide = True
        elif p3_rast<circle_rad:                                        colide = True
        elif p4_rast<circle_rad:                                        colide = True
        else:colide = False

        if rect_x<=circle_x<=rect_x+rect_w:
            if circle_y>rect_y:
                if abs(circle_y-rect_y)<circle_rad+rect_h:              colide=True
                else:                                                   colide=False
            elif circle_y<rect_y:

                if abs(circle_y-(rect_y+rect_h))<circle_rad+rect_h:     colide=True
                else:                                                   colide=False

        if rect_y<=circle_y<=rect_y+rect_h:
            if circle_x>rect_x:
                if abs(circle_x-rect_x)<circle_rad+rect_w:              colide=True
                else:                                                   colide=False
            elif circle_x<rect_x:

                if abs(circle_x-(rect_x+rect_w))<circle_rad+rect_w:     colide=True
                else:                                                   colide=False


        return colide

    def collide_circle_circle(circle1_pos, circle2_pos, circle1_rad, circle2_rad):
        rast = GL_MATH.Math_().RAST(circle1_pos,circle2_pos)
        if rast<circle1_rad+circle2_rad:
            return True
        else:
            return False

    class Circle_Rigget_buddie():
        def __init__(self,radius,pos=[0,0],gravity:float=None,resistance=[0.5,0.5],air_resistance=[1,1]) -> None:
            self.radius = radius
            self.position = pos
            if gravity==None:self.gravity = 0.5
            else: self.gravity = gravity
            self.gravity_V = GL_MATH.Vec2_([0,self.gravity])
            self.speed_V = GL_MATH.Vec2_([0,-1])
            self.resistance = resistance
            self.air_resistance = air_resistance
            self.provisions = {
                'collide':False,
                'collide_rigget_buddie':False,
                'collide_point':False
            }

        def __View__(self,surf:GL.Display_init_,color,board_size=5):
            surf.GL.Circle(color,self.pos,self.radius,board_size,'s','D')

        def __str__(self) -> str:
            return f'[p:{self.position},r:{self.radius},sp:{self.speed_V.xy()},res:{self.resistance},a_res{self.air_resistance}]'

        def __Camera__(self,sx,sy):
            self.pos[0]+=sx
            self.pos[1]+=sy

        @property
        def x(self):
            return self.pos[0]

        @property
        def y(self):
            return self.pos[1]

        @property
        def pos(self):
            return self.pos

        @property
        def size(self):
            return [self.radius*2,self.radius*2]

        @property
        def sx(self):
            return self.speed_V.vector.x

        @property
        def sy(self):
            return self.speed_V.vector.y
            
        def Collide_point(self,point):
            if GL_MATH.Math_().RAST(self.position,point)<self.radius:return True
            else:return False

        def Collide_point_property(self,point):
            if GL_MATH.Math_().RAST(self.position,point)<self.radius:self.provisions['collide_point']=True
            else:self.provisions['collide_point']=False

    class Rect_Rigget_buddie():
        def __init__(self,size,pos=[0,0],gravity:float=None,resistance=[0.5,0.5],air_resistance=[1,1]) -> None:
            self.rb = pygame.Rect(pos[0],pos[1],size[0],size[1])
            if gravity==None:self.gravity = 0.5
            else: self.gravity = gravity
            self.gravity_V = GL_MATH.Vec2_([0,self.gravity])
            self.speed_V = GL_MATH.Vec2_([0,-1])
            self.resistance = resistance
            self.air_resistance = air_resistance
            self.provisions = {
                'collide':False,
                'collide_rigget_buddie':False,
                'collide_point':False
            }

        def __View__(self,screen:GL.Display_init_,color,board_size=5,border_radius=15,surf='s'):
            screen.GL.Rect(color,self.pos,self.size,surf,board_size,'F',R=border_radius)

        def __str__(self) -> str:
            return f'[p:{self.pos},s:{self.size},sp:{self.speed_V.xy()},res:{self.resistance},a_res{self.air_resistance}]'

        def __Camera__(self,sx,sy):
            self.rb.x+=sx
            self.rb.y+=sy


        @property
        def x(self):
            return self.rb.x

        @property
        def center(self):
            return self.rb.center

        @property
        def center_x(self):
            return self.rb.centerx

        @property
        def center_y(self):
            return self.rb.centery

        @property
        def y(self):
            return self.rb.y

        @property
        def pos(self):
            return [self.rb.x,self.rb.y]

        @property
        def size(self):
            return [self.rb.w,self.rb.h]

        @property
        def sx(self):
            return self.speed_V.vector.x

        @property
        def sy(self):
            return self.speed_V.vector.y

        @property
        def prov_collide_(self):
            return self.provisions['collide']

        @property
        def prov_collide_rigget_buddie_(self):
            return self.provisions['collide_rigget_buddie']

        @property
        def prov_collide_point_(self):
            return self.provisions['collide_point']

        def Set_pos(self,x,y,speed_stoping_x=True,speed_stoping_y=True,centered=False):
            if not centered:
                self.rb.x = x
                self.rb.y = y
            else:
                self.rb.centerx = x
                self.rb.centery = y
            if speed_stoping_x:self.speed_V.vector.x = 0
            if speed_stoping_y:self.speed_V.vector.y = 0

        def Set_pos_x(self,x):
            self.rb.x = x

        def Set_pos_y(self,y):
            self.rb.y = y

        def Set_speed(self,x:float,y:float):
            self.speed_V.vector.x = x
            self.speed_V.vector.y = y

        def Set_speed_x(self,x):
            self.speed_V.vector.x = x

        def Set_speed_y(self,y):
            self.speed_V.vector.y = y

        def Move(self,sx=None,sy=None):
            #self.rb.x+=sx
            #self.rb.y+=sy
            if sx!=None:self.speed_V.vector.x = sx
            if sy!=None:self.speed_V.vector.y = sy

        def Collide_rigget_buddie_property(self,rigget_buddie):
            self.provisions['collide_rigget_buddie'] = self.rb.colliderect(rigget_buddie.rb)

        def Collide_point_property(self,point):
            self.provisions['collide_point'] = self.rb.collidepoint(point)

        def Collide_rigget_buddie(self,rigget_buddie):
            return self.rb.colliderect(rigget_buddie.rb)

        def Collide_point(self,point):
            return self.rb.collidepoint(point)
        
        def Simulate_rigget_buddies(self,map_rigget_buddies):
            self.rb.x+=self.speed_V.vector.x
            self.speed_V.vector.x*=self.air_resistance[0]
            self.speed_V.vector.y*=self.air_resistance[1]
            for block in map_rigget_buddies:
                if block.rb.colliderect(self.rb.x,self.rb.y,self.rb.w,self.rb.h):
                    if self.speed_V.vector.x>0:
                        self.speed_V.vector.x=0
                        self.rb.right = block.rb.left           
                if block.rb.colliderect(self.rb.x,self.rb.y,self.rb.w,self.rb.h):
                    if self.speed_V.vector.x<0:
                        self.speed_V.vector.x=0
                        self.rb.left = block.rb.right  


            if abs(self.speed_V.vector.y)<1 and self.provisions.get('collide'):self.speed_V.vector.y=0
            self.rb.y+=self.speed_V.vector.y

            self.provisions['collide']=False

            for block in map_rigget_buddies:
                if block.rb.colliderect(self.rb.x,self.rb.y,self.rb.w,self.rb.h):
                    if self.speed_V.vector.y>0:
                        self.rb.bottom = block.rb.top
                        self.speed_V.vector.y =- int(self.speed_V.vector.y*self.resistance[1])
                        self.speed_V.vector.x *=self.resistance[0]
                        self.provisions['collide']=True 
                    elif self.speed_V.vector.y<0:
                        self.rb.top = block.rb.bottom
                        self.speed_V.vector.y = 0
                        
            self.speed_V.vector+=self.gravity_V.vector

        def Simulate_pygame_rect_list(self,map_pygame_rect):
            self.rb.x+=self.speed_V.vector.x
            self.speed_V.vector.x*=self.air_resistance[0]
            self.speed_V.vector.y*=self.air_resistance[1]
            
            if self.rb.collidelist(map_pygame_rect):
                    if self.speed_V.vector.x>0:
                        self.speed_V.vector.x=0
                        self.rb.right = block.left           
            if self.rb.collidelist(map_pygame_rect):
                    if self.speed_V.vector.x<0:
                        self.speed_V.vector.x=0
                        self.rb.left = block.right  


            if abs(self.speed_V.vector.y)<2 and self.provisions.get('collide'):self.speed_V.vector.y=0
            self.rb.y+=self.speed_V.vector.y

            self.provisions['collide']=False

            for block in map_pygame_rect:
                if self.rb.collidelist(map_pygame_rect):
                    if self.speed_V.vector.y>0:
                        self.rb.bottom = block.top
                        self.speed_V.vector.y =- int(self.speed_V.vector.y*self.resistance[1])
                        self.speed_V.vector.x *=self.resistance[0]
                        self.provisions['collide']=True 
                    elif self.speed_V.vector.y<0:
                        self.rb.top = block.bottom
                        self.speed_V.vector.y = 0
                        
            self.speed_V.vector+=self.gravity_V.vector 

        def Simulate_pygame_rect(self,map_pygame_rect,simulate_rad=200):
            self.rb.x+=self.speed_V.vector.x
            self.speed_V.vector.x*=self.air_resistance[0]
            self.speed_V.vector.y*=self.air_resistance[1]
            
            for block in map_pygame_rect:

                    if block.colliderect(self.rb.x,self.rb.y,self.rb.w,self.rb.h):
                        if self.speed_V.vector.x>0:
                            self.speed_V.vector.x=0
                            self.rb.right = block.left           
                    if block.colliderect(self.rb.x,self.rb.y,self.rb.w,self.rb.h):
                        if self.speed_V.vector.x<0:
                            self.speed_V.vector.x=0
                            self.rb.left = block.right  


            if abs(self.speed_V.vector.y)<2 and self.provisions.get('collide'):self.speed_V.vector.y=0
            self.rb.y+=self.speed_V.vector.y

            self.provisions['collide']=False

            for block in map_pygame_rect:

                    if block.colliderect(self.rb.x,self.rb.y,self.rb.w,self.rb.h):
                        if self.speed_V.vector.y>0:
                            self.rb.bottom = block.top
                            self.speed_V.vector.y =- int(self.speed_V.vector.y*self.resistance[1])
                            self.speed_V.vector.x *=self.resistance[0]
                            self.provisions['collide']=True 
                        elif self.speed_V.vector.y<0:
                            self.rb.top = block.bottom
                            self.speed_V.vector.y = 0
                        
            self.speed_V.vector+=self.gravity_V.vector 

class Camera():
    def __init__(self,muvement_speed=[0.5,0.5],cam_size = [2500,2500], otr_x=False, otr_y=False,angl = 0) -> None:
        self.sx = 0
        self.sy = 0
        self.cam_pulse = muvement_speed
        self.shake_timer = 0
        self.shake_time = 0

        self.otr_x = otr_x
        self.otr_y = otr_y
        self.angl = angl
        
        self.cam_size = cam_size
        self.cam_surf = pygame.Surface(self.cam_size)
        self.save_cam_surf = pygame.Surface([self.cam_size[0],self.cam_size[1]],pygame.SRCALPHA, 32).convert_alpha()
        self.coef = 1
        

    def Stabilization(self,obj_pos,stabilisation_pos,cam_pulse=None):
        if cam_pulse==None:
            self.sx = int((stabilisation_pos[0]-obj_pos[0])*self.cam_pulse[0])
            self.sy = int((stabilisation_pos[1]-obj_pos[1])*self.cam_pulse[1])
        else:
            self.sx = int((stabilisation_pos[0]-obj_pos[0])*cam_pulse[0])
            self.sy = int((stabilisation_pos[1]-obj_pos[1])*cam_pulse[1])

    @property
    def sxs(self):
        return self.sx

    @property
    def sys(self):
        return self.sy

    def sahke(self,time = 10,mosh=10):
        self.shake_time = time
        if self.shake_timer>self.shake_time:
            self.shake_timer = 0
        self.shake_timer +=1
        if self.shake_timer<self.shake_time:
            self.sx+=random.randint(-mosh,mosh)
            self.sy+=random.randint(-mosh,mosh)

    def Move(self,speed_x,speed_y):
        self.sx+=int(speed_x)
        self.sy+=int(speed_y)

    def Render(self,win1,pos,bg,tranformings=False):
        
        if tranformings:
            self.cam_surf = pygame.transform.flip(self.cam_surf,self.otr_x,self.otr_y)
            self.cam_surf = pygame.transform.rotate(self.cam_surf,self.angl)
        self.pos = self.cam_surf.get_rect(center=pos)
        win1.screen.blit(self.cam_surf,[self.pos.x,self.pos.y])
        self.save_cam_surf.fill(bg)

    def zoom(self,scale=1):
        self.coef = scale
        if self.coef<0:self.coef=0.001
        self.cam_surf = pygame.transform.scale(self.save_cam_surf,[self.cam_size[0]*self.coef,self.cam_size[1]*self.coef])