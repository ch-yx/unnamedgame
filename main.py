
from Box2D import *
import pygame
from math import floor
from collections import defaultdict
from contextlib import contextmanager,ExitStack
from functools import lru_cache
def debugprint(x):
    print(x)
    return x
CACHE_SIZE=7
image_loader = lru_cache(maxsize=None)(pygame.image.load)
class Gloop:
    
    # pygame setup
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720),pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.world=Level(self)
        self.centerX=0
        self.centerY=0
        self.pixpu=50
        self.mouseISdown=False
        self.backroundColor="skyblue"
        
        self.mapscreencache=defaultdict(lambda:pygame.Surface((CACHE_SIZE*self.pixpu,CACHE_SIZE*self.pixpu),flags=pygame.SRCALPHA ))
        self.rezoom()
    def rezoom(self):
        self.mapscreencache.clear()
        self.Images=(pygame.transform.scale(image_loader('0.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('0_.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('1.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('2.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('3.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('playerbody.png'),(self.pixpu,self.pixpu*2))
        ,pygame.transform.scale(image_loader('playerfoot1.png'),(self.pixpu,self.pixpu*2))
        ,pygame.transform.scale(image_loader('playerfoot2.png'),(self.pixpu,self.pixpu*2))
        ,pygame.transform.scale(image_loader('playerhand1.png'),(self.pixpu,self.pixpu*2))
        ,pygame.transform.scale(image_loader('slime_air_b_1.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('slime_air_d_1.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('slime_b_1.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('slime_d_1.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('slime_air_b_2.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('slime_b_2.png'),(self.pixpu,self.pixpu))
        )
        self.flipImages=lru_cache(8)(lambda N:pygame.transform.flip(self.Images[N],1,0))
    def world2screen(self,x,y):
        return (
        ((x-self.centerX)*self.pixpu+self.screen.get_width()/2),
        ((self.centerY-y)*self.pixpu+self.screen.get_height()/2)
        )
    def screen2world(self,x,y):
        return (
        (x-self.screen.get_width()/2)/self.pixpu+self.centerX,
        self.centerY-(y-self.screen.get_height()/2)/self.pixpu
        )
    def setcenterbyworldpos(self,pos):
        self.centerX,self.centerY=pos
    def tick(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = None
            elif event.type == pygame.KEYDOWN:
                self.world.onkeydown(event.key)
            elif event.type == pygame.KEYUP:
                if event.key==pygame.K_ESCAPE:
                    self.running = not self.running
                elif event.key==pygame.K_EQUALS:
                    self.pixpu+=1
                    self.rezoom()
                elif event.key==pygame.K_MINUS:
                    self.pixpu=max(1,self.pixpu-1)
                    self.rezoom()
                else:
                    self.world.onkeyup(event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseISdown=False
                #self.setcenterbyworldpos(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseISdown=True
        
            
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill(self.backroundColor)

        if self.running:
            self.world.tick()
        self.setcenterbyworldpos(self.world.player.eyepos)   
        self.world.draw(self.screen,self.world2screen,self.pixpu)
        if not self.running:
            self.screen.fill((56,56,56),None,pygame.BLEND_RGBA_MULT)

        # flip() the display to put your work on screen
        pygame.display.flip()

        self.clock.tick(60)  # limits FPS to 60
    def start(self):
        try:
            while self.running is not None:
                self.tick()
        except:
            raise
        finally:
            pygame.quit()
class Level:
    def __init__(self,gloop) -> None:
        self.gloop=gloop
        class myContactListener(b2ContactListener):
            def __init__(self):
                b2ContactListener.__init__(self)
            def BeginContact(self, contact):
                pass
            def EndContact(self, contact):
                pass
            def PreSolve(self, contact, oldManifold):
                if contact.fixtureA.userData is not None and contact.fixtureA.userData is not None:
                    if contact.fixtureA.userData.get("role",None) is contact.fixtureB.userData.get("role",...):
                        contact.enabled = False
                        return
                if contact.fixtureA.userData is not None and contact.fixtureA.userData.get("oneway"):
                    if contact.fixtureB.userData is not None and isinstance(thatplayer:=contact.fixtureB.userData.get("role"),NormalMob) and (thatplayer.wannadown or 
                                                                                                                                              ("up" == contact.fixtureB.userData["half"])):
                        contact.enabled = False
                        return
                    if contact.fixtureB.GetAABB(0).lowerBound[1]<contact.fixtureA.GetAABB(0).upperBound[1]:
                        contact.enabled = False
                        return
                if contact.fixtureB.userData is not None and contact.fixtureB.userData.get("oneway"):
                    if contact.fixtureA.userData is not None and isinstance(thatplayer:=contact.fixtureA.userData.get("role"),NormalMob) and (thatplayer.wannadown or 
                                                                                                                                              ("up" == contact.fixtureA.userData["half"])):
                        contact.enabled = False
                        return
                    if contact.fixtureA.GetAABB(0).lowerBound[1]<contact.fixtureB.GetAABB(0).upperBound[1]:
                        contact.enabled = False
                        return
            def PostSolve(self, contact, impulse):
                pass
                
        self.world = b2World(gravity=(0, -10),contactListener=myContactListener())
        self.world.world=self
        self.world.NPCs=[]
        self.world.normalBlocks={}
        self.world.JBlocks={}
        self.world.LBlocks={}
        self.world.onewayBlocks={}
        #self.ground=self.world.CreateBody()
        map="""
        ~~~~~~~~~~~~         O         J
                    ~~~~~~~~~~~~~~~~~~J
                                     J
                                    J
        ###                  J###  J  
        ###&  J#L    ^  o   #    ##
        #####~   ###########
        """
        for i,line in enumerate(map.splitlines()):
            for j,c in enumerate(line):
                if c == "#":
                    self.place_a_normal_block(self.world,j,-i)
                elif c == "^":
                    self.player=Player(self.world,j,-i)
                elif c == "o":
                    Slime(self.world,j,-i)
                elif c == "O":
                    Slime(self.world,j,-i).slimecolor=1
                elif c == "&":
                    NPC(self.world,j,-i)
                elif c == "J":
                    self.place_a_J_block(self.world,j,-i)
                elif c == "L":
                    self.place_a_L_block(self.world,j,-i)
                elif c == "~":
                    self.place_a_oneway_block(self.world,j,-i)
        
        
        
        self.pressed = {pygame.K_w:False,pygame.K_s:False,pygame.K_a:False,pygame.K_d:False}

    @staticmethod
    def place_a_normal_block(world,x,y):
        world.normalBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y), (1+x,y),(1+x, 1+y),(x, 1+y))),userData={"role":"ground"})
        )
    @staticmethod
    def place_a_J_block(world,x,y):
        world.JBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y), (1+x,y),(1+x, 1+y))),userData={"role":"ground"})
        )
    @staticmethod
    def place_a_L_block(world,x,y):
        world.LBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y), (1+x,y),(x, 1+y))),userData={"role":"ground"})
        )
    @staticmethod
    def place_a_oneway_block(world,x,y):
        world.onewayBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y+0.5), (1+x,y+0.5),(1+x, 1+y),(x, 1+y))),userData={"oneway":True,"role":"ground"})
        )
    def tick(self):
        with ExitStack() as Entityticks:
            self.player.wannajump=self.pressed[pygame.K_w]
            self.player.wannadown=self.pressed[pygame.K_s]
            Entityticks.enter_context(self.player.tick())

            _npcs=[]
            for i in self.world.NPCs:
                if i.died:
                    continue
                Entityticks.enter_context(i.tick())
                _npcs.append(i)
            self.world.NPCs[:]=_npcs
            #self.playermoving.localAnchorB=(34,56)
            self.player.walk(3*(self.pressed[pygame.K_d]-self.pressed[pygame.K_a]))
            self.world.Step(1/60,10,10)

        
            #self.player_foot.ApplyLinearImpulse((0,0.5),self.player_head.position,True)
            
            #self.player_head.ApplyForce(100*(self.player_foot.position-self.player_head.position),(0,0),True)
        
            
    def draw(self,surface,zoom_func,zoom):
        if not self.gloop.mapscreencache:
            for x,y in self.world.normalBlocks:
                X,x=divmod(x,CACHE_SIZE)
                Y,y=divmod(y,CACHE_SIZE)
                self.gloop.mapscreencache[(X,Y)].blit(self.gloop.Images[not(hash(x*0.3+0.01*y+0.1)%7)],(zoom*x,zoom*(CACHE_SIZE-1-y)))
            for x,y in self.world.LBlocks:
                X,x=divmod(x,CACHE_SIZE)
                Y,y=divmod(y,CACHE_SIZE)
                self.gloop.mapscreencache[(X,Y)].blit(self.gloop.Images[2],(zoom*x,zoom*(CACHE_SIZE-1-y)))
            for x,y in self.world.JBlocks:
                X,x=divmod(x,CACHE_SIZE)
                Y,y=divmod(y,CACHE_SIZE)
                self.gloop.mapscreencache[(X,Y)].blit(self.gloop.Images[3],(zoom*x,zoom*(CACHE_SIZE-1-y)))
            for x,y in self.world.onewayBlocks:
                X,x=divmod(x,CACHE_SIZE)
                Y,y=divmod(y,CACHE_SIZE)
                self.gloop.mapscreencache[(X,Y)].blit(self.gloop.Images[4],(zoom*x,zoom*(CACHE_SIZE-1-y)))
        if 0:
            for body in self.world.bodies:
                trans=body.transform
                for fixture in body.fixtures:
                    if fixture.userData is None:
                        fixture.userData={}
                    if isinstance( fixture.shape,b2CircleShape):
                        pygame.draw.circle(surface, fixture.userData.setdefault("color",[255,255,255]),zoom_func(*(trans*fixture.shape.pos)), zoom*fixture.shape.radius)
                    else:
                        pygame.draw.polygon(surface,fixture.userData.setdefault("color",[100,100,100]),[zoom_func(*trans*v) for v in fixture.shape.vertices])
            
        for npc in self.world.NPCs:
            npc.draw(surface,zoom_func,zoom)
        self.world.world.player.draw(surface,zoom_func,zoom)
        surface.blits((s,zoom_func(x*CACHE_SIZE,y*CACHE_SIZE+CACHE_SIZE)) for (x,y),s in self.gloop.mapscreencache.items())
        # for x,y in self.world.normalBlocks:
        #     surface.blit(self.gloop.Images[not(hash(x*0.3+0.01*y+0.1)%10)],zoom_func(x,y+1))
        # for x,y in self.world.LBlocks:
        #     surface.blit(self.gloop.Images[2],zoom_func(x,y+1))
        # for x,y in self.world.JBlocks:
        #     surface.blit(self.gloop.Images[3],zoom_func(x,y+1))
        # for x,y in self.world.onewayBlocks:
        #     surface.blit(self.gloop.Images[4],zoom_func(x,y+1))
            
                    
        


    def onkeydown(self,key):
        self.pressed[key]=True
    def onkeyup(self,key):
        self.pressed[key]=False

class NormalMob:
    walkspeed=1
    wannadown=False
    wannajump=False
    uppersize=(0.5,1.5/2)
    upperdensity=1
    buttomsize=0.5
    isSlime=False
    facing=1  #1 or -1
    def attack(self):
        pass
    def beharmed(self):
        pass
    def bekilled(self):
        pass
    def remove(self):
        pass
    def __init__(self,world,playerXinit,playerYinit) -> None:
        self.world=world
        self.player_foot=player_foot=self.world.CreateDynamicBody(
            fixtures=b2FixtureDef(userData={"role":self,"half":"down"},friction=10,
                shape=b2CircleShape(radius=self.buttomsize),
                density=1.0),
            bullet=False,
            position=(0.5+playerXinit, 0.5+playerYinit))
        self.player_head=player_head=self.world.CreateDynamicBody(
            fixedRotation = True,
            fixtures=b2FixtureDef(userData={"role":self,"half":"up"},friction=0,
                shape=b2PolygonShape(box=self.uppersize),
                density=self.upperdensity,isSensor=self.isSlime),
            bullet=False,
            position=(0.5+playerXinit, 1.5+playerYinit))
        self.playerJointPlan=b2WheelJointDef(
            bodyB=player_head,
            bodyA=player_foot,
            localAnchorB=(0,-1.5/2),
            localAnchorA=(0, 0),
            enableMotor=True,
            motorSpeed=0,
            maxMotorTorque=10000,
            )
        self.playermoving=None
    def jump(self):
        self.player_foot.angle=-40*self.facing
        self.playerJointPlan.localAnchorB=(0,-1)
        self.playerJointPlan.frequencyHz=50
        self.playermoving = self.world.CreateJoint(self.playerJointPlan)
    def unjump(self):  
        self.playerJointPlan.localAnchorB=(0,-1.5/2)
        self.playerJointPlan.frequencyHz=3
        self.playerJointPlan.dampingRatio=0.7
        self.playermoving = self.world.CreateJoint(self.playerJointPlan)
    def clean(self):
        self.world.DestroyJoint(self.playermoving)
    def walk(self,speed):
        speed*=self.walkspeed
        if speed > 0:
            self.facing=1
        if speed < 0:
            self.facing=-1
        self.playermoving.motorSpeed=speed
    @property
    def eyepos(self):
        return self.player_head.position
    def draw(self,surface,zoom_func,zoom):
        X=self.player_head.fixtures[0].GetAABB(0).lowerBound[0]
        Y=self.player_head.fixtures[0].GetAABB(0).upperBound[1]
        x=self.player_foot.fixtures[0].GetAABB(0).lowerBound[0]
        y=self.player_foot.fixtures[0].GetAABB(0).upperBound[1]
        if self.facing==1:
            surface.blit(self.world.world.gloop.Images[6+round(self.player_foot.angle)%2],zoom_func(x,y+1) )
            surface.blit(self.world.world.gloop.Images[5],zoom_func(X,Y) )
            surface.blit(self.world.world.gloop.Images[8],zoom_func(x,Y) )
        else:
            surface.blit(self.world.world.gloop.flipImages(6+round(self.player_foot.angle)%2),zoom_func(x,y+1) )
            surface.blit(self.world.world.gloop.flipImages(5),zoom_func(X,Y) )
            surface.blit(self.world.world.gloop.flipImages(8),zoom_func(x,Y) )
class Player(NormalMob):
    @contextmanager
    def tick(self):
        with FastShoes().onuse(self):
            with FastShoes().onuse(self):##temp
                yield self.jump() if self.wannajump else self.unjump()
                self.clean()
class NPC(NormalMob):
    def __init__(self, world, playerXinit, playerYinit) -> None:
        super().__init__(world, playerXinit, playerYinit)
        
        world.NPCs.append(self)
    died=0
    counter=0
    @contextmanager
    def tick(self):
        self.counter+=1
        if self.counter%60:
            self.unjump()
            self.walk(6*((self.counter//100)%2-0.5))
            yield
        else:
            yield self.jump()
        self.clean()
class Slime(NPC):
    isSlime=True
    buttomsize=0.5
    upperdensity=5000
    uppersize=(0.01,0.01)
    slimecolor=0
    @contextmanager
    def tick(self):
        self.counter+=1
        if not self.counter%180:
            self.facing*=-1
        if self.counter%60:
            self.unjump()
            yield
        else:
            yield self.jump()
        self.clean()
    def draw(self, surface, zoom_func, zoom):
        aabb=self.player_foot.fixtures[0].GetAABB(0)
        zom=zoom_func(aabb.lowerBound[0],aabb.upperBound[1])
        if self.slimecolor==0: 
            if self.player_foot.linearVelocity[1]>0:
                surface.blit(self.world.world.gloop.Images[9],zom)
                surface.blit(self.world.world.gloop.Images[10],zom)
            else:
                surface.blit(self.world.world.gloop.Images[11],zom)
                surface.blit(self.world.world.gloop.Images[12],zom)
        elif self.slimecolor==1:
            if self.player_foot.linearVelocity[1]>0:
                surface.blit(self.world.world.gloop.Images[13],zom)
                surface.blit(self.world.world.gloop.Images[10],zom)
            else:
                surface.blit(self.world.world.gloop.Images[14],zom)
                surface.blit(self.world.world.gloop.Images[12],zom)


class Item:
    @contextmanager
    def onuse(self,user):
        yield

class FastShoes(Item):
    @contextmanager
    def onuse(self,user:NormalMob):
        ori=user.walkspeed
        user.walkspeed*=1.5
        yield
        user.walkspeed=ori
Gloop().start()