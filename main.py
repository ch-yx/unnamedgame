
from Box2D import *
import pygame
from math import floor
from collections import defaultdict
from contextlib import contextmanager,ExitStack
from functools import lru_cache
from operator import itemgetter
def debugprint(x):
    print(x)
    return x
CACHE_SIZE=7
image_loader = lru_cache(maxsize=None)(lambda fname:pygame.image.load(f"res/{fname}"))
class Gloop:
    
    # pygame setup
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720),pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.world=Level(self, wmap="""
        
        
                H                       #
        ~~~~~~~~H~~~~~i                 #
                H                       #
               HH                       #
               HH            f          #
               HH                       #
        ~~~~~~~H~~~~         O         J
        #      H    ~~~~~~~~~~~~~~~~~~J
        #      H                     J
        #      H                    J
        ###    H             J###  J  
        ###&  J#L    ^  o   #    ##
        #####~   ###########
        """)
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
        ,pygame.transform.scale(image_loader('ladder.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('ladder_.png'),(self.pixpu,self.pixpu))
        ,pygame.transform.scale(image_loader('boots1.png'),(self.pixpu*0.75,self.pixpu*0.75))#17
        ,pygame.transform.scale(image_loader('shooter1.png'),(self.pixpu*0.75,self.pixpu*0.75))#18
        )
        self.flipImages=lru_cache(800)(lambda N:pygame.transform.flip(self.Images[N],1,0))
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
    def __init__(self,gloop,wmap) -> None:
        self.gloop=gloop
        class myContactListener(b2ContactListener):
            def __init__(self):
                b2ContactListener.__init__(self)
            def BeginContact(self, contact):
                pass
            def EndContact(self, contact):
                pass
            def PreSolve(self, contact, oldManifold):
                if contact.fixtureA.userData is not None and contact.fixtureB.userData is not None:
                    if contact.fixtureA.userData.get("role",None) is contact.fixtureB.userData.get("role",...):
                        contact.enabled = False
                        return
                    iA=isinstance(A:=contact.fixtureA.userData.get("role",None),Projectile)
                    iB=isinstance(B:=contact.fixtureB.userData.get("role",None),Projectile)
                    if iA or iB:
                        if contact.fixtureA.userData.get("team",None) is contact.fixtureB.userData.get("team",None):
                            contact.enabled = False
                            return
                    if iA and not iB:
                        contact.enabled = not A.hiton(B,contact.fixtureB.body)
                        return
                    if iB and not iA:
                        contact.enabled = not B.hiton(A,contact.fixtureA.body)
                        return
                    if iA and iB:
                        return
                    if isinstance(A,ItemEntity) and B !="ground":
                        A.onpickedup(B)
                        contact.enabled = False
                        return
                    if isinstance(B,ItemEntity) and A !="ground":
                        B.onpickedup(A)
                        contact.enabled = False
                        return
                if contact.fixtureA.userData is not None and contact.fixtureA.userData.get("oneway"):
                    if contact.fixtureB.userData is not None and isinstance(thatplayer:=contact.fixtureB.userData.get("role"),Humanoid) and (thatplayer.wannadown or 
                                                                                                                                              ("up" == contact.fixtureB.userData["half"])):
                        contact.enabled = False
                        return
                    if contact.fixtureB.GetAABB(0).lowerBound[1]<contact.fixtureA.GetAABB(0).upperBound[1]:
                        contact.enabled = False
                        return
                if contact.fixtureB.userData is not None and contact.fixtureB.userData.get("oneway"):
                    if contact.fixtureA.userData is not None and isinstance(thatplayer:=contact.fixtureA.userData.get("role"),Humanoid) and (thatplayer.wannadown or 
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
        self.world.futureNPCs=[]
        self.world.normalBlocks={}
        self.world.JBlocks={}
        self.world.LBlocks={}
        self.world.onewayBlocks={}
        self.world.ladders={*()}
        #self.ground=self.world.CreateBody()

        for i,line in enumerate(wmap.splitlines()):
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
                elif c == "H":
                    self.place_a_ladder(self.world,j,-i)
                elif c == "i":
                    ItemEntity(self.world,Shooter(),j,-i)
                elif c == "f":
                    ItemEntity(self.world,FastShoes(3),j,-i)
        
        

    @staticmethod
    def place_a_normal_block(world,x,y):
        world.normalBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y), (1+x,y),(1+x, 1+y),(x, 1+y))),userData={"role":"ground","team":None})
        )
    @staticmethod
    def place_a_J_block(world,x,y):
        world.JBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y), (1+x,y),(1+x, 1+y))),userData={"role":"ground","team":None})
        )
    @staticmethod
    def place_a_L_block(world,x,y):
        world.LBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y), (1+x,y),(x, 1+y))),userData={"role":"ground","team":None})
        )
    @staticmethod
    def place_a_oneway_block(world,x,y):
        world.onewayBlocks[(x,y)]=world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=((x, y+0.5), (1+x,y+0.5),(1+x, 1+y),(x, 1+y))),userData={"oneway":True,"role":"ground","team":None})
        )
    @staticmethod
    def place_a_ladder(world,x,y):
        world.ladders.add((x,y))
    def tick(self):
        with ExitStack() as Entityticks:
            pressed=pygame.key.get_pressed()
            self.player.wannajump=pressed[pygame.K_w]
            self.player.wannadown=pressed[pygame.K_s]
            Entityticks.enter_context(self.player.tick(pressed))
            self.world.NPCs.extend(self.world.futureNPCs)
            self.world.futureNPCs.clear()
            _npcs=[]
            for i in self.world.NPCs:
                if i.died:
                    i.onremove()
                    continue
                Entityticks.enter_context(i.tick())
                _npcs.append(i)
            self.world.NPCs[:]=_npcs
            #self.playermoving.localAnchorB=(34,56)
            #self.player.walk((pressed[pygame.K_d]-pressed[pygame.K_a]))
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
            for x,y in self.world.ladders:
                laddertype=(x+y)%2
                X,x=divmod(x,CACHE_SIZE)
                Y,y=divmod(y,CACHE_SIZE)
                self.gloop.mapscreencache[(X,Y)].blit(self.gloop.Images[15+laddertype],(zoom*x,zoom*(CACHE_SIZE-1-y)))
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
        #self.pressed[key]=True
        if key==pygame.K_SPACE:
            self.player.wannaattack=True
    def onkeyup(self,key):
        #self.pressed[key]=False
        pass
INF=float("inf")
NINF=-INF
class Damageable:
    @property
    def eyepos(self):
        return self.getAABB().center
    def getAABB(self,bs=None):
        aabb=b2AABB()
        aabb.lowerBound=(INF,INF)
        aabb.upperBound=(NINF,NINF)
        for body in self.bodies() if bs is None else bs:
            transform = body.transform
            for fixture in body.fixtures:
                shape = fixture.shape
                for childIndex in range(shape.childCount):
                    aabb.Combine(shape.getAABB(transform, childIndex))            
        return aabb
    team=None
    isPlayer=False
    def __init__(self, world:b2World) -> None:        
        if not self.isPlayer:world.futureNPCs.append(self)
        self.world=world
    def attack(self,other:"Damageable",hearts:float,flags:int,part=None):
        pass
    def beharmed(self,other:"Damageable",hearts:float,flags:int,part=None):
        pass
    def onkilled(self):
        self.died=True
    removed=False#already be removed
    died=False#should be removed
    def onremove(self):
        if self.removed:return
        self.removed=True
        self.clean()
    def clean(self):
        pass
    def draw(self,surface,zoom_func,zoom):
        pass
    def knockback(self,vec:b2Vec2,size,part=None):
        pass
    def bodies(s):
        yield from ()
    def pickup(s,i):
        return False
        
class Humanoid(Damageable):
    def bodies(s):
        yield s.player_foot
        yield s.player_head
    inventory:list
    def pickup(s,i):
        s.inventory.insert(0,i)
        return True
    def knockback(self,vec:b2Vec2,size,part=None):
        if part is None:part=self.player_foot
        part.ApplyLinearImpulse((size/vec.length)*vec,self.player_foot.worldCenter,True)
    walkspeed=3
    wannadown=False
    wannajump=False
    uppersize=(0.5,1.5/2)
    upperdensity=1
    buttomsize=0.5
    isSlime=False
    facing=1  #1 or -1
    maxHealth=20.0
    def attack(self,other:"Damageable",hearts:float,flags:int,part=None):
        other.beharmed(self,hearts,flags,part)
    def beharmed(self,other:"Damageable",hearts:float,flags:int,part=None):
        self.health-=hearts
        if self.health<=0:
            self.onkilled()
    
    def onremove(self):
        if self.removed:return
        self.removed=True
        self.clean()
        
        self.world.DestroyBody(self.player_foot)
        self.world.DestroyBody(self.player_head)
        self.player_foot=self.player_head=None
        
    def __init__(self,world:b2World,playerXinit,playerYinit) -> None:
        super().__init__(world)
        self.health=self.maxHealth
        self.inventory=[]
        self.player_foot=player_foot=self.world.CreateDynamicBody(
            fixtures=b2FixtureDef(userData={"role":self,"half":"down","team":self.team},friction=10,
                shape=b2CircleShape(radius=self.buttomsize),
                density=1.0),
            bullet=False,
            position=(0.5+playerXinit, 0.5+playerYinit))
        self.player_head=player_head=self.world.CreateDynamicBody(
            fixedRotation = True,
            fixtures=b2FixtureDef(userData={"role":self,"half":"up","team":self.team},friction=0,
                shape=b2PolygonShape(box=self.uppersize),
                density=self.upperdensity,isSensor=self.isSlime),
            bullet=False,
            position=(0.5+playerXinit, 1.5+playerYinit))
        self.playerspine=None

    playerJointPlan_jump=b2WheelJointDef(
            localAnchorB=(0,-1.5/2),
            localAnchorA=(0, 0),
            enableMotor=True,
            motorSpeed=0,
            maxMotorTorque=10000,
            )
    playerJointPlan_jump.localAnchorB=(0,-1)
    playerJointPlan_jump.frequencyHz=50

    playerJointPlan_unjump=b2WheelJointDef(
            localAnchorB=(0,-1.5/2),
            localAnchorA=(0, 0),
            enableMotor=True,
            motorSpeed=0,
            maxMotorTorque=10000,
            )
    playerJointPlan_unjump.localAnchorB=(0,-1.5/2)
    playerJointPlan_unjump.frequencyHz=3
    playerJointPlan_unjump.dampingRatio=0.7

    def jump(self):
        self.player_foot.angle=-40*self.facing
        self.playerJointPlan_jump.bodyB=self.player_head
        self.playerJointPlan_jump.bodyA=self.player_foot
        self.playerspine = self.world.CreateJoint(self.playerJointPlan_jump)
    def unjump(self):  
        self.playerJointPlan_unjump.bodyB=self.player_head
        self.playerJointPlan_unjump.bodyA=self.player_foot
        self.playerspine = self.world.CreateJoint(self.playerJointPlan_unjump)
    def clean(self):
        if self.playerspine is not None:
            self.world.DestroyJoint(self.playerspine)
        self.playerspine=None
    def walk(self,speed):
        speed*=self.walkspeed
        if speed > 0:
            self.facing=1
        if speed < 0:
            self.facing=-1
        self.playerspine.motorSpeed=speed
    @property
    def eyepos(self):
        return self.player_head.position
    def drawhealthbar(self,surface,zoom_func):
        temp=self.getAABB()
        
        L2=temp.upperBound
        L1=b2Vec2(temp.lowerBound[0],L2[1])
        L3=(self.maxHealth-self.health)/self.maxHealth*L1+self.health/self.maxHealth*L2
        h=b2Vec2(0,0.3)
        pygame.draw.polygon(surface,"green",tuple(zoom_func(*i) for i in (L1,L3,L3+h,L1+h)))
        pygame.draw.polygon(surface,"gray",tuple(zoom_func(*i) for i in (L3,L2,L2+h,L3+h)))
    def draw(self,surface,zoom_func,zoom):
        self.drawhealthbar(surface,zoom_func)
        h = self.getAABB((self.player_head,))
        X=h.lowerBound[0]
        Y=h.upperBound[1]
        t = self.getAABB((self.player_foot,))
        x=t.lowerBound[0]
        y=t.upperBound[1]
        # X=self.player_head.fixtures[0].GetAABB(0).lowerBound[0]
        # Y=self.player_head.fixtures[0].GetAABB(0).upperBound[1]
        # x=self.player_foot.fixtures[0].GetAABB(0).lowerBound[0]
        # y=self.player_foot.fixtures[0].GetAABB(0).upperBound[1]
        if self.facing==1:
            surface.blit(self.world.world.gloop.Images[6+round(self.player_foot.angle)%2],zoom_func(x,y+1) )
            surface.blit(self.world.world.gloop.Images[5],zoom_func(X,Y) )
            surface.blit(self.world.world.gloop.Images[8],zoom_func(x,Y) )
        else:
            surface.blit(self.world.world.gloop.flipImages(6+round(self.player_foot.angle)%2),zoom_func(x,y+1) )
            surface.blit(self.world.world.gloop.flipImages(5),zoom_func(X,Y) )
            surface.blit(self.world.world.gloop.flipImages(8),zoom_func(x,Y) )
TEAM_A="A"
TEAM_B="B"
class Player(Humanoid):
    keysetting=itemgetter(pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d)
    team=TEAM_A
    isPlayer=True
    wannaattack=False
    @property
    def inladder(self):
        x,y=self.eyepos
        return (floor(x),floor(y)) in self.world.ladders
    isflying=False
    @contextmanager
    def tick(self,pressed):
        with ExitStack() as items:
            for item in self.inventory:
                items.enter_context(item.ifhave(self))
            if self.wannaattack:
                self.wannaattack=False
                
                for item in self.inventory:
                    if isinstance(item,Weapon) and item.canbeused(self):
                        item.onuse(self,self.eyepos,(self.facing,0))
                        break
            if not (self.isflying or self.inladder):
                yield self.jump() if self.wannajump else (self.unjump(),self.walk((pressed[pygame.K_d]-pressed[pygame.K_a]))
)
                self.clean()
            else:
                olda,oldb=self.player_head.gravityScale,self.player_foot.gravityScale
                self.player_head.gravityScale=self.player_foot.gravityScale=0
                
                nowspeed=self.player_foot.linearVelocity
                targetspeed=2*b2Vec2(pressed[pygame.K_d]-pressed[pygame.K_a],self.wannajump-self.wannadown)
                self.player_foot.ApplyForce(5*(targetspeed-nowspeed),self.player_foot.worldCenter,True)
                yield (self.unjump(), self.walk((pressed[pygame.K_d]-pressed[pygame.K_a]))
)
                self.player_head.gravityScale,self.player_foot.gravityScale=olda,oldb
                self.clean()
                
class NPC(Humanoid):
    team=TEAM_B
    counter=0
    def onkilled(self):
        #Slime(self.world,self.eyepos[0]-0.5,self.eyepos[1]-0.5)
        #Slime(self.world,self.eyepos[0]-0.5,self.eyepos[1]-1.5)
        return super().onkilled()
    @contextmanager
    def tick(self):
        self.counter+=1
        if self.counter%60:
            self.unjump()
            self.walk(2*((self.counter//100)%2-0.5))
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
        self.drawhealthbar( surface, zoom_func)
        aabb=self.getAABB((self.player_foot,))#self.player_foot.fixtures[0].GetAABB(0)
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
    imageid=-999
    @contextmanager
    def ifhave(self,user):
        yield

class FastShoes(Item):
    imageid=17
    def __init__(self,k) -> None:
        super().__init__()
        self.k=k
    @contextmanager
    def ifhave(self,user:Damageable):
        ori=user.walkspeed
        user.walkspeed*=self.k
        yield
        user.walkspeed=ori

class Weapon(Item):
    def canbeused(self,user):
        pass
    def onuse(self,user,usepos,usedir):
        pass
class nWeapon(Weapon):#attack everything
    def canbeused(self, user):
        return True
    def onuse(self, user,usepos,usedir):
        for i in user.world.NPCs:
            user.attack(i,10,0b0)
            i.knockback(i.eyepos-user.eyepos,20)

class Shooter(Weapon):
    imageid=18
    def canbeused(self, user):
        return True
    def onuse(self, user,usepos,usedir):
        Projectile(user.world,*usepos,user,3*b2Vec2(usedir)+next(user.bodies()).linearVelocity)

class Projectile(Damageable):
    def bodies(s):
        yield s.body
    def __init__(self, world: b2World, x, y,owner,dir) -> None:
        super().__init__(world)
        self.team=owner.team
        self.owner=owner
        self.body=world.CreateDynamicBody(
            fixtures=b2FixtureDef(userData={"role":self,"owner":owner,"team":self.team},
                shape=b2CircleShape(radius=0.1),
                density=0),gravityScale=0,
            bullet=True,
            position=(x, y),linearVelocity=dir)
    def draw(self, surface, zoom_func, zoom):
        fixture=self.body.fixtures[0]
        trans=self.body.transform
        pygame.draw.circle(surface, [128,128,128],zoom_func(*(trans*fixture.shape.pos)), zoom*fixture.shape.radius)


    @contextmanager
    def tick(self):
        yield
    def hiton(self,other:Damageable,part:b2Body=None):#return true to pass through
        if isinstance(other,Damageable):
            self.owner.attack(other,3,0b0)
            other.knockback(other.eyepos-self.owner.eyepos,20,part)
        self.onkilled()
        return True
    def onremove(self):
        self.world.DestroyBody(self.body)
class ItemEntity(Damageable):
    def bodies(s):
        yield s.body
    @contextmanager
    def tick(s):
        yield
    team=TEAM_A
    def __init__(self, world: b2World,item:Item,Xinit,Yinit) -> None:
        super().__init__(world)
        self.item=item
        self.body=self.world.CreateDynamicBody(
            fixedRotation = True,
            fixtures=b2FixtureDef(userData={"role":self,"team":self.team},friction=0,
                shape=b2PolygonShape(box=(0.375,0.375)),
                isSensor=False),
            bullet=False,
            position=(0.5+Xinit, 0.5+Yinit))
    def onremove(self):
        self.removed=self.died=True
        if self.body is not None:
            self.world.DestroyBody(self.body)
        self.body = None
    def onpickedup(self,other):
        if self.died:return
        if self.team is not None:
            if self.team is not other.team:
                return
        if other.pickup(self.item):
            self.onkilled()
    def draw(self, surface, zoom_func, zoom):
        if self.item.imageid < 0:return
        aabb=self.getAABB()#self.player_foot.fixtures[0].GetAABB(0)
        zom=zoom_func(aabb.lowerBound[0],aabb.upperBound[1])
        surface.blit(self.world.world.gloop.Images[self.item.imageid],zom)

    
Gloop().start()