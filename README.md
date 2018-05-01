Projet Vision (Réaliter augmenter)
=====================================

Python version
==============
Développer avec Anaconda python 3.6 sur Windows 10
- https://www.anaconda.com/download/

Dépendance
==========

- OpenCv 3 (traitement image)
- Numpy (Matrice)
- pymunk (Moteur physisque)

Installation
============
- Installation Anaconda python 3.6 voir la lien: https://www.anaconda.com/download/

- Installation de OpenCv3 avec anaconda: ``conda install -c conda-forge opencv``
- Installation de OpenCv3 avec pip: ``python -m pip install opencv-python``
- Lien d'un bon tutoriel pour l'installation OpenCv3: https://www.scivision.co/install-opencv-python-windows/

- Installation de numpy avec pip: ``pip install numpy``
- Installation Pymunk: ``pip install pymunk``

Utilisation
===========
Pour exécuter le programme il faut avoir une webcam mobile pour pouvoir l'orienter
- Démarrer le fichier main.py Suivre le menu

- L'application Ball tracking game n'écessite une balle de couleur jaune. Il est possible de changer la couleur de tracking dans le fichier BouncingCube/Traking.py "color_hsv_low=(29, 86, 6), color_hsv_hight=(64, 255, 255)"
Pour faire une conversion RGB a HSV d'opencv voici un lien qu'il l'explique http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#how-to-find-hsv-values-to-track

- L'application Image translation n'écessite une caméra mobile.

Pour vous aider une vidéo est disponible 'video_tuto.wmv'

