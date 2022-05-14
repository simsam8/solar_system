#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import math

"""
Created on Mon Mar 14 09:06:48 2022

@author: nicholasrokenes
"""
pygame.init()

AU = 149.6e6 * 1000 # Astronomisk enhet. Ganget med 1000 for meter
G = 6.67428e-11 # Gravitasjon
SCALE = 10 / AU # Skala
TIMESTEP = 3600*24 # Tidsrom for 1 dag


SKJERM_INFO = pygame.display.Info() # Henter oppløsning av skjermen
BREDDE = SKJERM_INFO.current_w*0.5 # Bredden på vinduet
HOYDE = SKJERM_INFO.current_h*0.5 # Høyden på vinduet
SENTRUM = (BREDDE/2, HOYDE/2)
#G = 1 #Tyngekraft
#KOLLDIST = sol.radius + jord.radius
HIMMEL_FARGE = (0,0,100)
FPS =  200 #Frames Per Second, dvs kor fort animasjonen skal gå.
JORDMASSE = 1
JORDRADIUS = 10


class HimmelObjekt():
    
    
    
    def __init__(self, navn, radius, masse, farge, koordinater, fart) -> None:
        self.navn = navn
        self.radius = radius
        self.masse = masse
        self.farge = farge
        self.X, self.Y = koordinater
        self.vX, self.vY = fart
        self.rX, self.rY = [0,0]
        
    def kalkuler_bane(self, legeme):
        
        # r-vektor går frå self til legeme
        self.rX, self.rY = legeme.X - self.X, legeme.Y - self.Y
        self.r2 = self.rX**2 + self.rY**2 # Kvadratet av avstanden
        self.r = math.sqrt(self.r2) # Avstanden
        self.r3 = self.r**3
        
        if self.r == 0:
            raise ValueError(f"Kollisjon mellom {self.navn} og {legeme.navn}")
        
        # Finn kraftkomponentane på objekt 2 ("Jorden")
        self.fX = G*legeme.masse*self.masse/self.r3*self.rX
        self.fY = G*legeme.masse*self.masse/self.r3*self.rY
        
        # Finn akselerasjonen i x- og y-retning
        self.aX = self.fX/self.masse
        self.aY = self.fY/self.masse
        
        # Finn farten i x- og y-retning
        self.vX += self.aX
        self.vY += self.aY
        
        # Finn ny posisjon (x- og y-koordinater)
        self.X += self.vX
        self.Y += self.vY
        
        
    def tegn_til_bilde(self):
        pygame.draw.circle(vindu, self.farge, (self.X, self.Y), self.radius, 0)


# Oppretter himmellegemer
sol = HimmelObjekt("Solen", JORDRADIUS*10, JORDMASSE*50, (255,255,0), SENTRUM, (0,0))
merkur = HimmelObjekt("Merkur", JORDRADIUS*0.38, JORDMASSE*0.0553, (100,0,0), (sol.X+140, sol.Y), (0, .6))
venus = HimmelObjekt("Venus", JORDRADIUS*0.95, JORDMASSE*0.815, (95,100,0), (sol.X+200, sol.Y), (0, 0.5))
jord = HimmelObjekt("Jorden", JORDRADIUS, JORDMASSE, (155,255,200), (sol.X+300, sol.Y), (0, 0.4))
månen = HimmelObjekt("Månen", 2, JORDMASSE*0.0023, (255,255,255), (jord.X+40,jord.Y), (0, .4))
mars = HimmelObjekt("Mars", JORDRADIUS*0.53, JORDMASSE*0.1075, (100,55,0), (sol.X+380, sol.Y), (0, 0.4))
jupiter = HimmelObjekt("Jupiter", JORDRADIUS*4, JORDMASSE*4, (95,84,18), (sol.X+800, sol.Y), (0, 0.25))



vindu = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("Planetbane: ")
clock = pygame.time.Clock()

def game_loop():
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit() 
    
        # kalkulerer banen til planetene
        merkur.kalkuler_bane(sol)
        jord.kalkuler_bane(sol)
        venus.kalkuler_bane(sol)
        mars.kalkuler_bane(sol)
        jupiter.kalkuler_bane(sol)
        #månen.kalkuler_bane(sol)
        månen.kalkuler_bane(jord)
        
        # Tegnar systemet
        vindu.fill(HIMMEL_FARGE)
        sol.tegn_til_bilde()
        merkur.tegn_til_bilde()
        venus.tegn_til_bilde()
        jord.tegn_til_bilde()
        mars.tegn_til_bilde()
        jupiter.tegn_til_bilde()
        månen.tegn_til_bilde()
        pygame.display.update()
        #clock.tick(FPS)
        
game_loop()