from math import pi # pour le calcul du diametre et de la surface du cercle
from tkinter import *
from tkinter.messagebox import * # boite de dialogue

couleurs = ['blue','red','green','yellow','white','black']

# ***** classe Forme *****
class Forme:
    def __init__(self,x,y,c): # Constructeur
        self.__xc = x # attribut prive : le nom est precede de "__"
        self.__yc = y
        self.__couleur = c
        
    def get_centre(self): # retourne les coordonnes du centre
        return self.__xc,self.__yc
        
    def set_centre(self,x,y): # change les coordonnes du centre
        self.__xc = x
        self.__yc = y
    
    def get_couleur(self): # retourne la couleur choisie
        return self.__couleur
        
    def set_couleur(self,c): # change la couleur
        self.__couleur = c
        
    def deplacement(self,dx,dy): # ajoute dx et dy aux coordonnes du centre
        self.__xc += dx
        self.__yc += dy
        
    def affiche(self,can): # affiche la figure sur la zone graphique 'can'
        pass

    def selection(self,x,y): # verifie si x et y sont sur la forme
        pass

# ***** classe Rectangle *****
class Rectangle(Forme):
    def __init__(self,x,y,l,h,c): # Constructeur
        Forme.__init__(self,x,y,c) # Le constructeur de la classe derivee doit faire appel a celui de la classe de base
        self.__l = l  # largeur du rectangle
        self.__h = h # hauteur du rectangle
        
    def get_dim(self):
        return self.__l,self.__h # retourne les dimensions du rectangle
        
    def set_dim(self,l,h): # change les dimensions du rectangle
        self.__l = l
        self.__h = h
        
    def perimetre(self): # retourne le perimetre du rectangle
        return 2*(self.__l+self.__h)
        
    def surface(self): # retourne la surface du rectangle
        return self.__l*self.__h

    def __str__(self): # pour la partie optionnelle (Dessin). Permet d'afficher un objet avec la fonction print
        return 'Rectangle - centre : {} | dimensions : {} | couleur : {} | perimetre : {} | surface : {}'.format(self.get_centre(), self.get_dim(), self.get_couleur(), self.perimetre(),self.surface())

    def affiche(self,can):         # affiche le rectangle sur la zone graphique 'can'
        x,y = self.get_centre()
        can.create_rectangle(x-self.__l//2, y-self.__h//2, x+self.__l//2, y+self.__h//2, outline=self.get_couleur(), fill=self.get_couleur())

    def selection(self,x,y): # verifie si x et y sont sur le rectangle
        xc,yc = self.get_centre()
        return (x >= xc-self.__l//2) and (y>= yc-self.__h//2) and (x <= xc+self.__l//2) and (y <= yc+self.__h//2)
    
# ***** classe Carre *****
class Carre(Rectangle):
    def __init__(self,x,y,l,c): # Constructeur
        Rectangle.__init__(self,x,y,l,l,c) # Constructeur de la classe de base
        
    def get_dim(self): # retourne le cote du carre
        l,l = Rectangle.get_dim(self)
        return l
        
    def set_dim(self,l): # change le cote du carre
        Rectangle.set_dim(self,l,l)
# Remarque: il est inutile de surcharger perimetre et surface de Rectangle
# qui fonctionnent grace a l'initialisation h=l !

    def __str__(self): # pour la partie optionnelle (Dessin). Permet d'afficher un objet avec la fonction print
        return 'Carre - centre : {} | dimensions : {} | couleur : {} | perimetre : {} | surface : {}'.format(self.get_centre(), self.get_dim(), self.get_couleur(), self.perimetre(),self.surface())

        
# ***** classe Cercle *****
class Cercle(Forme):
    def __init__(self,x,y,d,c): # constructeur
        Forme.__init__(self,x,y,c) # constructeur de la classe de base
        self.__d = d
        
    def get_dim(self): # retourne le diametre du cercle
        return self.__d
        
    def set_dim(self,d): # change le diametre du cercle
        self.__d = d
        
    def perimetre(self): # retourne le perimetre du cercle
        return pi*self.__d
        
    def surface(self): # retourne la surface du cercle
        return pi*self.__d**2/4
        
    def __str__(self): # pour la partie optionnelle (Dessin). Permet d'afficher un objet avec la fonction print
        return 'Cercle - centre : {} | dimensions : {} | couleur : {} | perimetre : {} | surface : {}'.format(self.get_centre(), self.get_dim(), self.get_couleur(), self.perimetre(),self.surface())

    def affiche(self,can): # affiche le cercle sur la zone graphique 'can'
        x,y = self.get_centre()
        can.create_oval(x-self.__d//2, y-self.__d//2, x+self.__d//2, y+self.__d//2, outline=self.get_couleur(), fill=self.get_couleur())

    def selection(self,x,y): # verifie si x et y sont sur le cercle
        xc,yc = self.get_centre()
        return (x >= xc-self.__d//2) and (y>= yc-self.__d//2) and (x <= xc+self.__d//2) and (y <= yc+self.__d//2)

# ***** classe Dessin *****        
class Dessin:
    def __init__(self):
        self.__formes = [] # liste de formes

    def add_forme(self,f): # ajoute la forme f dans la liste formes
        self.__formes.append(f)
        
    def del_forme(self,position): # supprime la forme d'apres sa position dans la liste
        del(self.__formes[position])

    def print_formes(self):  # affiche toutes les formes dans la liste
        print('--- Dessin ----')
        for f in self.__formes:
            print(f)
            
    def affiche_formes(self,can,nb): # affiche les nb premiers formes dans la liste sur la zone graphique 'can' (nb maximum = nombre d'elements de la liste)
        i=0
        while (i<len(self.__formes) and i<nb):
            self.__formes[i].affiche(can)
            i+=1
            
    def selection_formes(self,x,y): # montre la forme selectionnee, s'il y en a 
        for f in self.__formes:
            if f.selection(x,y) : 
                showinfo('Forme sélectionnée',f.__str__())
                break
            
    def size(self): # retourne le nombre de formes dans la liste
        return len(self.__formes)
            