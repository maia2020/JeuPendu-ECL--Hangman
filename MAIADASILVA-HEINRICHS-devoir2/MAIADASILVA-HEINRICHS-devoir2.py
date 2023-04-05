from tkinter import *
from random import randint
from formes import *
from tkinter import colorchooser

class ZoneAffichage(Canvas): # classe de la zone d'affichage
	def __init__(self, parent, w, h, c):
		Canvas.__init__(self, master=parent, width=w, height=h, bg=c) # création de la zone d'affichage avec les paramètres donnés
		
		ymax= h;
	
		self.__dessin = Dessin() # Objet de la classe Dessin qui contient les formes à dessiner

		# Création des formes qui composent le pendu
		f = Rectangle(100,ymax-50,100,5,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(100,ymax-150,5,200,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(148,ymax-250,100,5,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(200,ymax-236,5,30,couleurs[5])
		self.__dessin.add_forme(f)

		f = Cercle(200,ymax-200,30,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(200,ymax-170,15,50,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(178,ymax-170,30,5,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(220,ymax-170,30,5,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(195,ymax-130,5,40,couleurs[5])
		self.__dessin.add_forme(f)

		f = Rectangle(205,ymax-130,5,40,couleurs[5])
		self.__dessin.add_forme(f)
		
	def afficher(self,n): #Associe la zone d'affichage a l'image du pendu correspondant au nombre d'erreurs
		self.__dessin.affiche_formes(self,n)

	def numbcoups(self): #Affiche le nombre de coups possible = nombre d'image  - 1
		return self.__dessin.size()	

	
class MonBouton(Button): # Classe des boutons du clavier, avec la lettre correspondante
	def __init__(self, parent, fenetre, lettre, w):
		Button.__init__(self, master=parent, text=lettre, width=w) # création du bouton avec la lettre correspondante
		self.__lettre = lettre
		self.__fenetre = fenetre #MonBoutonLettre est associé à la fenêtre de jeu

	def cliquer(self): # fonction qui est appelée quand on clique sur le bouton
		self.config(state=DISABLED) # Après avoir cliqué sur le bouton, il ne peut plus être cliqué et il devient plus clair
		self.__fenetre.traitement(self.__lettre) # On appelle la fonction traitement de la fenêtre de jeu

class Menu(Tk): # classe de la première fenêtre, le menu
	def __init__(self):
		Tk.__init__(self)
		self.title('Menu')

		f = open('historique.txt', 'r') # ouverture du fichier contenant l'historique des scores
		s = f.read() #Conversion du fichier en chaine de caractères
		self.__joueurs = s.split('\n') #Création d'une liste contenant les noms des joueurs
		#["Joueur1, nbparties, nbvictoire"]
		f.close()	

		Label(self, text='Entrez Votre Nom!').pack(side=TOP , padx=5, pady=5) # Création d'un label pour demander le nom du joueur

		f1 = Frame(self) # Création d'une frame pour contenir le champ de saisie et le bouton
		f1.pack(side=TOP, padx=5, pady=5)

		self.nom = StringVar() # Création d'une variable de type StringVar pour contenir le nom du joueur
		text = Entry(f1, textvariable=self.nom, bg ='white',fg='black') # Création d'un champ de saisie pour le nom du joueur
		text.focus_set() # Le curseur est placé dans le champ de saisie
		text.pack(side = TOP, padx=5, pady=5)

		# Création d'un bouton pour lancer la partie
		Button(f1,text='Jouer',width=15,command=self.traiterjoueur).pack(side=TOP,padx=5,pady=5)

		# Création d'un bouton pour quitter le menu
		Button(f1, text='Quitter', width=15, command=self.destroy).pack(side=TOP, padx=5, pady=5)
		
		# Création d'un bouton pour afficher l'historique des scores
		Button(f1, text='Historique', width=15, command=self.affiche_historique).pack(side=TOP, padx=5, pady=5)

		# Création d'un bouton pour effaer l'historique des scores
		Button(f1, text='Effacer Historique', width=15, command=self.clear).pack(side=TOP, padx=5, pady=5)
	
	def traiterjoueur(self): # Realise les actions en fonction du nom du joueur
		for j in self.__joueurs: # On parcourt la liste des joueurs
			if j.split(',')[0] == self.nom.get(): # Si le nom du joueur est dans la liste
				self.destroy() # On détruit la fenêtre du menu
				fen = FenPrincipale(j) # On crée la fenêtre de jeu
				fen.mainloop() # On lance la fenêtre de jeu
				return # On sort de la fonction
		with open('historique.txt', 'a') as f: # Si le nom du joueur n'est pas dans la liste, on l'ajoute
			f.write("\n" + self.nom.get() + ",0,0") # On ajoute le nom du joueur, le nombre de victoires et le nombre de parties
		with open('historique.txt', 'r') as f: #On actualise la liste des joueurs
			self.__joueurs = f.read().split('\n')
			print(self.__joueurs)
		self.destroy() # On détruit la fenêtre du menu
		fen = FenPrincipale(self.__joueurs[-1]) # On crée la fenêtre de jeu
		fen.mainloop() # On lance la fenêtre dex jeu

	def clear(self): # Fonction qui efface l'historique des scores
		open('historique.txt', 'w').close() # On ouvre le fichier en mode écriture et on le vide

	def affiche_historique(self): # Fonction qui affiche l'historique des scores
		text = open('historique.txt', 'r').read() # On ouvre le fichier en mode lecture et on le convertit en chaine de caractères
		s = text.split('\n') # On crée une liste contenant les noms des joueurs

		for e in s:
			if e != '': #Condition pour ne pas afficher les lignes vides
				Label(self, text = 'Nom : ' + e.split(',')[0] + ' Nombre de parties jouées : ' + e.split(',')[2] + ' Nombre de victoires : ' + e.split(',')[1]).pack(side=TOP , padx=5, pady=5) # Création d'un label pour afficher le nom du joueur et son taux de victoire

class FenPrincipale(Tk):
	def __init__(self, joueur): # Création de la fenêtre de jeu
		Tk.__init__(self)
		self.title('Pendu')
		self.__joueur = joueur # On récupère le nom du joueur
		self.__errours = 0 # On initialise le nombre d'erreurs à 0
		self.__motaaffiche = '' # On initialise le mot affiché à une chaine de caractères vide
		self.__mot = '' # On initialise le mot à trouver à une chaine de caractères vide
		self.__bonneslettres = [] # On initialise la liste des bonnes lettres à une liste vide
		self.__mauvaiseslettres = [] # On initialise la liste des mauvaises lettres à une liste vide
		f1 = Frame(self) #frame pour contenir les 2 boutons principaux
		f1.pack(side=TOP, padx=5, pady=5)

		#Creation du bouton pour quitter le jeu
		Button(f1, text='Quitter', width=15, command=self.destroy).pack(side=LEFT, padx=5, pady=5)

		#Creation du bouton pour lancer une nouvelle partie
		Button(f1, text='Nouvelle Partie', width=15, command=self.nouvelle_partie).pack(side=LEFT, padx=5, pady=5)

		#Creation du bouton pour undo une joue
		Button(f1, text='Undo', width=15, command=self.undo).pack(side=LEFT, padx=5, pady=5)

		#Creation du bouton pour changer le couleur du background
		Button(f1, text='Couleur BG', width=15, command=self.changer_couleurbg).pack(side=LEFT, padx=5, pady=5)

		#Creation du bouton pour changer le couleur du clavier
		Button(f1, text='Couleur Clavier', width=15, command=self.changer_couleurclavier).pack(side=LEFT, padx=5, pady=5)

		#Creation du bouton pour changer le couleur de la zone d'affichage
		Button(f1, text='Couleur ZoneAffichage', width=15, command=self.changer_couleurzoneaffichage).pack(side=LEFT, padx=5, pady=5)

		self.__zoneAffichage = ZoneAffichage(self,320,320,'snow2') # Création de la zone d'affichage
		self.__zoneAffichage.pack(side=TOP, padx=5, pady=5)
		self.__zoneAffichage.afficher(0)
		self.__lmot = Label(self, text='Mot : ') # Création d'un label pour afficher le mot à trouver
		self.__lmot.pack(side=TOP)
		self.__flag = 0 # On initialise le flag à 0
		

		f2 = Frame(self) # Création d'une frame pour contenir le clavier
		f2.pack(side=TOP, padx=5, pady=5)

		self.__boutons = [] # Création d'une liste pour contenir les boutons du clavier
		for i in range(26): # Création des boutons du clavier
			t = chr(ord('A')+i) # On crée une chaine de caractères contenant la lettre du bouton
			self.__boutons.append(MonBouton(f2,self,t,4)) # On ajoute le bouton à la liste
			self.__boutons[i].config(command = self.__boutons[i].cliquer) # On associe une fonction au bouton

		for i in range(3): #Affiche les 3 premières lignes du clavier
			for j in range(7):
				self.__boutons[i*7+j].grid(row=i, column=j)

		for j in range(5):
			self.__boutons[21+j].grid(row=3, column=j+1)

		self.nouvelle_partie() # On lance une nouvelle partie

	def changer_couleurbg(self):
		coulor = colorchooser.askcolor()[1]
		self.configure(background= coulor)

	def changer_couleurclavier(self):
		coulor = colorchooser.askcolor()[1]
		for i in range(26):
			self.__boutons[i].configure(background= coulor)

	def changer_couleurzoneaffichage(self):
		coulor = colorchooser.askcolor()[1]
		self.__zoneAffichage.configure(background= coulor)
		
	
	def traitement(self,lettre):
		k = 0
		lettres = list(self.__motaaffiche) # On crée une liste contenant les lettres du mot affiché

		for i in range(len(self.__mot)): # On parcourt le mot à trouver
			if self.__mot[i] == lettre: # Si la lettre du mot à trouver est égale à la lettre cliquée
				k += 1 # On incrémente k
				lettres[i] = lettre # On remplace les * par lettre cliquée

		self.__motaaffiche = ''.join(lettres) # On convertit la liste en chaine de caractères

		if k ==0: #si la lettre n'est pas dans le mot
			self.__errours += 1 # On incrémente le nombre d'erreurs
			self.__mauvaiseslettres.append(lettre) # On ajoute la lettre à la liste des mauvaises lettres
			self.__flag = 0 # On remet le flag à 0
			self.__zoneAffichage.afficher(self.__errours-1) # On affiche l'image correspondante
			if self.__errours-1 >= self.__zoneAffichage.numbcoups(): # Si le nombre d'erreurs est supérieur au nombre d'images
				self.fin(False) # False pour dire que le joueur a perdu
		else: # Si la lettre est dans le mot
			self.__lmot.config(text='Mot : '+self.__motaaffiche) # On affiche le mot avec les lettres trouvées
			self.__bonneslettres.append(lettre) # On ajoute la lettre à la liste des bonnes lettres
			self.__flag = 1 # On met le flag à 1
			
			if self.__mot == self.__motaaffiche: # Si le mot est trouvé
				self.fin(True) # True pour dire que le joueur a gagné

	def undo(self): #Fonction pour undo le dernier coup
		#Si le flag est à 1, on undo la derniere lettre bonne
		if self.__flag == 1:
			l = self.__bonneslettres.pop() #On enleve la derniere lettre bonne de la liste
			self.__motaaffiche = self.__motaaffiche.replace(l,'*') #On remplace la lettre par un *
			self.__lmot.config(text='Mot : '+self.__motaaffiche)

			#On change l'etat du bouton
			for b in self.__boutons:
				if b['text'] == l:
					b.config(state=NORMAL)
		
		if self.__flag == 0:
			l = self.__mauvaiseslettres.pop() #On enleve la derniere lettre mauvaise de la liste
			self.__errours -= 1 #On enleve une erreur
			#on delete l'image et on affiche la precedente
			self.__zoneAffichage.delete(ALL)
			self.__zoneAffichage.afficher(self.__errours-1)
			for b in self.__boutons:
				if b['text'] == l:
					b.config(state=NORMAL)			

	def nouvelle_partie(self):
		self.__zoneAffichage.delete(ALL) # pour supprimer tout ce qui se trouve sur le Canvas
		self.__zoneAffichage.afficher(0) # On affiche l'image de départ
		self.chargeMots() # On charge la liste des mots
		self.__mot = self.nouveaumot() # On choisit un mot au hasard dans la liste des mots
		self.__motaaffiche = len(self.__mot)*'*' # On crée une chaine de caractères contenant autant de * que de lettres dans le mot
		self.__lmot.config(text='Mot : '+self.__motaaffiche) # On affiche le mot avec les * à la place des lettres
		self.__errours = 1 # On remet le nombre d'erreurs à 1 (car on a déjà affiché l'image de départ)


		for b in self.__boutons:
			b.config(state=NORMAL) # On réactive tous les boutons du clavier

	def chargeMots(self):
		f = open('mots.txt','r') # On ouvre le fichier mots.txt en lecture
		s = f.read() # On lit le fichier
		self.__mots = s.split('\n') # On convertit le fichier en liste
		f.close() # On ferme le fichier

	def nouveaumot(self):
		return self.__mots[randint(0,len(self.__mots)-1)] # On choisit un mot au hasard dans la liste des mots
	
		



	def fin(self,resultat):
		for b in self.__boutons:
			b.config(state=DISABLED) # On désactive tous les boutons du clavier
		
		if resultat : # Si le joueur a gagné
			self.__lmot.config(text=self.__mot + '------VICTORY!') # On affiche le mot et VICTORY!

			f = open('historique.txt','r')  # On ouvre le fichier historique en lecture
			s = f.read().split("\n") # On lit le fichier et on le convertit en liste
			f.close() # On ferme le fichier

			for i in range(len(s)):

				if s[i] == self.__joueur: # On cherche le joueur dans la liste
					s[i] = s[i].split(',')[0]+','+ str(int(s[i].split(',')[1])+1)+','+str(int(s[i].split(',')[2])+1) # On incrémente le nombre de parties jouées et le nombre de parties gagnées
					self.__joueur=s[i] # On met à jour le joueur

			with open('historique.txt','w') as f: # On ouvre le fichier historique en écriture
				f.write('\n'.join(s)) # On écrit la liste dans le fichier

		else: # Si le joueur a perdu
			self.__lmot.config(text='DEFEAT! Le mot était : '+self.__mot) # On affiche le mot et DEFEAT!

			f=open('historique.txt','r') # On ouvre le fichier historique en lecture
			s=f.read().split("\n") # On lit le fichier et on le convertit en liste
			f.close() # On ferme le fichier

			for i in range(len(s)):
				if s[i] == self.__joueur:
					s[i] = s[i].split(',')[0]+','+ str(int(s[i].split(',')[1]))+','+str(int(s[i].split(',')[2])+1) # On incrémente le nombre de parties jouées
					self.__joueur=s[i] # On met à jour le joueur

			with open('historique.txt','w') as f: # On ouvre le fichier historique en écriture
				f.write('\n'.join(s)) # On écrit la liste dans le fichier

fen = Menu() # On ouvre la fenêtre du menu
fen.mainloop()