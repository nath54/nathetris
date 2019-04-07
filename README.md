# Nathetris

Introduction :
--------------

C'est un remix du célèbre jeu tétris, il y ajoute des fonctionnalités, comme le mode coopération ou 1v1(pas encore disponible).
Il utilise la librairie pygame et il est conseillé de le lancer avec python3.
Si vous voulez lancer avec python, il ne faut télécharger que le fichier 'jeu.py'.
On peut aussi y jouer directement sur windows en téléchargant le fichier 'jeu.zip', en le dézippant et en lancant l'éxécutable qui se trouve dans le dossier extrait.
Le fichier 'jeu.zip' a été compilé avec pyinstaller. Attention, le fichier 'jeu.zip' n'est pas mis à jour à chaque commit.

Description :
-------------

C'est un jeu basé sur le jeu tétris : il y a des blocs de différentes formes qui tombent et il faut bien les arranger entre eux pour remplir des lignes complètes et que les blocs posés ne dépassent pas une certaine hauteur.
Dans ce jeu, il y a différents modes de jeux, il y a : 
    
    -le mode normal
    
    -le mode coopération ( 2 joueurs jouent sur le même plateau )
    
    -le mode coopération avec un bot ( le joueur joue avec un bot qui fait tomber des blocs aléatoirement )
    
Des nouveaux modes vont bientôt être ajoutés :

    -le mode coopération avec une IA ( le joueur joue avec une IA , qui est différente du simple bot )
    
    -le mode IA ( une IA joue toute seule )
    
    -le mode 1v1 ( deux joueurs jouent l'un contre l'autre )
    
    -le mode 1v1 IA ( le joueur joue contre une IA )

IL y a aussi plusieurs modes de couleurs :

    -le mode couleur standar ( chaque bloc a une couleur aléatoire , deux blocs de même forme n'ont pas la même couleur )
    
    -le mode couleur unique ( chaque forme a une couleur aléatoire )
    
    -le mode noir et blanc ( tous les blocs sont en blanc, sur un fond noir )
    
    -le mode dégradé ( le premier bloc a une couleur aléatoire, et a chaque fois qu'un nouveau bloc apparaît, la couleur change un petit peu, se qui forme une sorte de dégradé )

Le joueur peut modifier la difficulté du jeu, il y a le mode facile , le mode moyen , le mode difficile et le mode hardcore.
La difficulté est indépendante de l'augmentation de la vitesse des blocs, la difficulté change la vitesse de base et la vitesse maximale des blocs.

Il y a quatres accélérations disponibles :
    
    -constante ( la vitesse ne change pas )
    
    -lent ( les blocs tombent 0.00001 secondes plus vite )
    
    -moyen ( les blocs tombent 0.0001 secondes plus vite )
    
    -rapide ( les blocs tombent 0.001 secondes plus vite )

La taille de la fenetre du jeu s'adapte en fonction des écrans, le jeu a une résolution de base de 700 * 900 sur un écran 1280 * 1024.


commandes:
----------

__Les touches du joueur 1 sont :__

    -bas     : flèche bas
    
    -gauche  : flèche gauche
    
    -droite  : flèche droite
    
    -pivoter : flèche gauche

__Les touches du joueur 2 sont :__

    -bas     : k
    
    -gauche  : j
    
    -droite  : l
    
    -pivoter : i



Si vous rencontrez des problèmes, vous pouvez créer une nouvelle issue, ou bien me contacter par mail : cerisara.nathan@gmail.com


