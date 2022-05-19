#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from turtle import distance
import pygame
import math

"""
Created on Mon Mar 14 09:06:48 2022

@author: nicholasrokenes
"""
pygame.init()

AU = 149.6e6 * 1000 # Astronomisk enhet. Ganget med 1000 for meter
G = 6.67428e-11 # Gravitasjon
SCALE = 60 / AU # Skala
TIMESTEP = 3600*24 # Tidsrom for 1 dag


SKJERM_INFO = pygame.display.Info() # Henter oppløsning av skjermen
BREDDE = SKJERM_INFO.current_w # 0.5 Bredden på vinduet
HOYDE = SKJERM_INFO.current_h # 0.5 Høyden på vinduet
SENTRUM = (BREDDE/2, HOYDE/2)
FPS =  60 #Frames Per Second, dvs kor fort animasjonen skal gå.


# Farger
HIMMEL_FARGE = (0,0,100)
GREY = (128,128,128)
YELLOWISH = (165,124,27)
BLUE = (0,0,225)
RED = (198,123,92)
BROWN = (144,97,77)
KARAMEL = (195,161,113)
URANUS_BLUE = (79,208,231)
NEPTUNE = (62,84,232)
WHITE = (255,255,255)
YELLOW = (255,255,0)
DARK_GREY = (80,78,81)

# Tekst 
FONT = pygame.font.SysFont('comicsans', 16)



class HimmelObjekt():
    def __init__(self, navn, radius, masse, farge, koordinater) -> None:
        self.navn = navn
        
        self.X, self.Y = koordinater
        self.radius = radius
        self.farge = farge
        self.masse = masse
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        self.vX, self.vY = 0,0
        self.rX, self.rY = [0,0]

   
   # Regner ut tiltrekning til annen planet
    def attraction(self, other):
        other_x, other_y = other.X, other.Y
        distance_x = other_x - self.X
        distance_y = other_y - self.Y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if other.sun:
            self.distance_to_sun = distance
        
        force = G * self.masse * other.masse / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x,force_y  
    
    
    # Regner ut totale krefter fra alle planeter og oppdaterer position til planet
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.vX += total_fx / self.masse * TIMESTEP
        self.vY += total_fy / self.masse * TIMESTEP
        
        self.X += self.vX * TIMESTEP
        self.Y += self.vY * TIMESTEP
        self.orbit.append((self.X, self.Y))
    
    
    def draw(self, vindu):
        x = self.X * SCALE + BREDDE / 2
        y = self.Y * SCALE + HOYDE / 2
        
        # Tegner banen til planeten
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + BREDDE / 2
                y = y * SCALE + HOYDE / 2
                updated_points.append((x,y))
                
            pygame.draw.lines(vindu, self.farge, False, updated_points, 2)
        
        # tegner selve planeten
        pygame.draw.circle(vindu, self.farge, (x,y), self.radius)
        
        if not self.sun:
            name = FONT.render(self.navn, 1, WHITE)
            #distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            vindu.blit(name, (x - name.get_width()/2, y - name.get_width()/2))


# Oppretter himmellegemer
sol = HimmelObjekt("Solen", 20, 1.98892*10**30, YELLOW, SENTRUM)
merkur = HimmelObjekt("Merkur", 5, 3.30*10**24, GREY, (0.387*AU, 0))
merkur.vY = 47.4 * 1000

venus = HimmelObjekt("Venus", 7, 4.8685*10**24, YELLOWISH, (0.723*AU, 0))
venus.vY = -35.02 * 1000

jord = HimmelObjekt("Jorden", 8, 5.9742*10**24, BLUE, (-1*AU,0))
jord.vY = 29.783 * 1000

# verdiene på månene må tweakes
#månen = HimmelObjekt("Månen", 2, 0.073*10**24, GREY, ((-1-0.384)*AU,0))
#månen.vY = 30.783 * 1000

mars = HimmelObjekt("Mars", 9, 6.39*10**23, RED, (-1.524*AU, 0))
mars.vY = 24.077 * 1000

jupiter = HimmelObjekt("Jupiter", 16, 1898.13*10**24, BROWN, (5.203*AU, 0))
jupiter.vY = 13.06 * 1000

saturn = HimmelObjekt("Saturn", 13, 568.32*10**24, KARAMEL, (9.537*AU,0))
saturn.vY = 9.68 * 1000

uranus = HimmelObjekt("Uranus", 11, 86.811*10**24, URANUS_BLUE, (19.191*AU,0))
uranus.vY = 6.80 * 1000

neptune = HimmelObjekt("Neptune", 9, 102.409*10**24, NEPTUNE, (30.068*AU,0))
neptune.vY = 5.43 * 1000

pluto = HimmelObjekt("Pluto", 10, 0.01303*10**24, BROWN, (39.481*AU,0))
pluto.vY = 4.67 * 1000

planeter = [sol, merkur, venus, jord, mars, jupiter, saturn, uranus, neptune, pluto]



vindu = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("Planetbane: ")
clock = pygame.time.Clock()

def game_loop():
    
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit() 
        
        # Tegnar systemet
        vindu.fill(HIMMEL_FARGE)
        for planet in planeter:
            planet.update_position(planeter)
            planet.draw(vindu)
        
        pygame.display.update()
        
game_loop()