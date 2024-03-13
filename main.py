
from Box2D import *
import pygame

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
    def world2screen(self,x,y):
        return (
        (x-self.centerX)*self.pixpu+self.screen.get_width()/2,
        (self.centerY-y)*self.pixpu+self.screen.get_height()/2
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
                else:
                    self.world.onkeyup(event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseISdown=False
                #self.setcenterbyworldpos(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseISdown=True
        
            
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("purple")

        if self.running:
            self.world.tick()
        self.setcenterbyworldpos(self.world.player.eyepos)   
        self.world.draw(self.screen,self.world2screen,self.pixpu)

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
                if contact.fixtureA.userData is not None and contact.fixtureA.userData.get("oneway"):
                    if contact.fixtureB.GetAABB(0).lowerBound[1]<contact.fixtureA.GetAABB(0).upperBound[1]:
                        contact.enabled = False
                if contact.fixtureB.userData is not None and contact.fixtureB.userData.get("oneway"):
                    if contact.fixtureA.GetAABB(0).lowerBound[1]<contact.fixtureB.GetAABB(0).upperBound[1]:
                        contact.enabled = False
            def PostSolve(self, contact, impulse):
                pass
                
        self.world = b2World(gravity=(0, -10),contactListener=myContactListener())
        self.world.NPCs=[]
        self.ground=self.world.CreateBody()
        map="""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~J
                             J
                            J
###                  L###  J  
###&  J#L    ^      #    ##
#####~   ###########
        """
        for i,line in enumerate(map.splitlines()):
            for j,c in enumerate(line):
                if c == "#":
                    self.place_a_normal_block(self.world,j,-i)
                elif c == "^":
                    self.player=NormalMob(self.world,j,-i)
                elif c == "&":
                    self.player=NPC(self.world,j,-i)
                elif c == "J":
                    self.place_a_J_block(self.world,j,-i)
                elif c == "L":
                    self.place_a_L_block(self.world,j,-i)
                elif c == "~":
                    self.place_a_oneway_block(self.world,j,-i)
        
        
        
        self.pressed = {pygame.K_w:False,pygame.K_s:False,pygame.K_a:False,pygame.K_d:False}

    @staticmethod
    def place_a_normal_block(world,x,y):
        world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=[(x, y), (1+x,y),(1+x, 1+y),(x, 1+y)]),userData={"color":[50,100,20]})
        )
    @staticmethod
    def place_a_J_block(world,x,y):
        world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=[(x, y), (1+x,y),(1+x, 1+y)]),userData={"color":[50,100,20]})
        )
    @staticmethod
    def place_a_L_block(world,x,y):
        world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=[(x, y), (1+x,y),(x, 1+y)]),userData={"color":[50,100,20]})
        )
    @staticmethod
    def place_a_oneway_block(world,x,y):
        world.CreateStaticBody(angle=0,
            fixtures=b2FixtureDef(friction=10,shape=b2LoopShape(vertices=[(x, y+0.5), (1+x,y+0.5),(1+x, 1+y),(x, 1+y)]),userData={"color":[50,100,20],"oneway":True})
        )
    def tick(self):
        if self.pressed[pygame.K_w]:
            self.player.jump()
        else:
            self.player.unjump()
        _npcs=[]
        for i in self.world.NPCs:
            if i.died:
                continue
            i.tick()
            _npcs.append(i)
        self.world.NPCs[:]=_npcs
        #self.playermoving.localAnchorB=(34,56)
        self.player.walk(3*(self.pressed[pygame.K_d]-self.pressed[pygame.K_a]))
        self.world.Step(1/60,10,10)
        self.player.clean()
        for i in self.world.NPCs:
            if i.died:
                continue
            i.clean()
        
            #self.player_foot.ApplyLinearImpulse((0,0.5),self.player_head.position,True)
            
            #self.player_head.ApplyForce(100*(self.player_foot.position-self.player_head.position),(0,0),True)
        
            
    def draw(self,surface,zoom_func,zoom):
        for body in self.world.bodies:
            trans=body.transform
            for fixture in body.fixtures:
                if fixture.userData is None:
                    fixture.userData={}
                if isinstance( fixture.shape,b2CircleShape):
                    pygame.draw.circle(surface, fixture.userData.setdefault("color",[255,255,255]),zoom_func(*(trans*fixture.shape.pos)), zoom*fixture.shape.radius)
                else:
                    pygame.draw.polygon(surface,fixture.userData.setdefault("color",[100,100,100]),[zoom_func(*trans*v) for v in fixture.shape.vertices])
            
        


    def onkeydown(self,key):
        self.pressed[key]=True
    def onkeyup(self,key):
        self.pressed[key]=False

class NormalMob:
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
            fixtures=b2FixtureDef(userData={"role":self},friction=10,
                shape=b2CircleShape(radius=0.5),
                density=1.0),
            bullet=False,
            position=(0.5+playerXinit, 0.5+playerYinit))
        self.player_head=player_head=self.world.CreateDynamicBody(
            fixedRotation = True,
            fixtures=b2FixtureDef(userData={"role":self},friction=0,
                shape=b2PolygonShape(box=[0.5,1.5/2]),
                density=1.0),
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
        self.playermoving.motorSpeed=speed
    @property
    def eyepos(self):
        return self.player_head.position

class NPC(NormalMob):
    def __init__(self, world, playerXinit, playerYinit) -> None:
        super().__init__(world, playerXinit, playerYinit)
        
        world.NPCs.append(self)
    died=0
    counter=0
    def tick(self):
        self.counter+=1
        if self.counter%60:
            self.unjump()
        else:
            self.jump()
Gloop().start()

