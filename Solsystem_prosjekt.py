#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import math

"""
Created on Mon Mar 14 09:06:48 2022

@author: nicholasrokenes
"""

pygame.init()

SKJERM_INFO = pygame.display.Info() # Henter oppløsning av skjermen
BREDDE = SKJERM_INFO.current_w*0.8 # Bredden på vinduet
HOYDE = SKJERM_INFO.current_h*0.8 # Høyden på vinduet
SENTRUM = (BREDDE/2, HOYDE/2)
G = 1 #Tyngekraft
#KOLLDIST = sol.radius + jord.radius
HIMMEL_FARGE = (0,0,100)
FPS =  200 #Frames Per Second, dvs kor fort animasjonen skal gå.
JORDMASSE = 1


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
sol = HimmelObjekt("Solen", 60, JORDMASSE*30, (255,255,0), SENTRUM, (0,0))
merkur = HimmelObjekt("Merkur", 10, JORDMASSE*0.0553, (100,0,0), (sol.X+100, sol.Y), (0, .55))
jord = HimmelObjekt("Jorden", 20, JORDMASSE, (155,255,200), (sol.X+300, sol.Y), (0, 0.3))
månen = HimmelObjekt("Månen", 2, JORDMASSE*0.0023, (255,255,255), (jord.X+40,jord.Y), (0, .4))


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
        jord.kalkuler_bane(sol)
        merkur.kalkuler_bane(sol)
        #månen.kalkuler_bane(sol)
        månen.kalkuler_bane(jord)
        
        # Tegnar systemet
        vindu.fill(HIMMEL_FARGE)
        sol.tegn_til_bilde()
        jord.tegn_til_bilde()
        merkur.tegn_til_bilde()
        månen.tegn_til_bilde()
        pygame.display.update()
        clock.tick(FPS)
        
game_loop()