### Préambule:
merci de ⭐ si cette repo vous a été utile, pas besoin de me créditer dans ce cas.

sur-ce: bonne lecture! Je suis ouvert à tout push request de clarification/mise en page sur les documents d'explication.

<img width="16" height="16" alt="image" src="https://github.com/user-attachments/assets/14889153-4cfe-4c81-976a-332bc530d2f6" />
Téléchargement: Zip/git en haut à droite. écrit: "**<> Code**"

### Résumé:
L'objectif de ce  TIPE était de retrouver par la mesure des résultats physiques théoriques étudiés en cours (lois de maxwell etc...).
Le tout sur un dispositif de dynamo de vélo sans contact (inspiré de la techno Reelight) et de voir les approximations envisageables pour simuler un tel dispositif.

Une première étape a été de faire un système de fixation d'aimants sur la roue du vélo et faire des bobines adaptées au dispositif, juste assez larges pour observer une fem induite mesurable.

Par le tracé de courbes/scatter vitesse/amplitude pour des mesures avec différentes distances rotor/stator on peut observer l'influence de la vitesse sur l'amplitude en sortie.

Un des challenge a été de réaliser le script python adapté pour leur analyse, pour déduire du signal une période de révolution et avec la dimension de la roue calculer la vitesse au sol théorique. 

AVEC UNE ASTUCE MAGIQUE ET ACCIDENTELLE:
Pour moi le signal caractéristique du tour se présente comme un décrochage ponctuel et plus long de la tension mesurée. 
- elle s'explique par le nombre d'aimants (6) et le nb de cadrans pour les caser (7)
  ajouter un 7eme aimant aurait été inutile pour avoir une alternance de poles N/S et maximiser la variation de flux on impose typiquement un nombre pair d'aimants
  et il y a donc un cadran sans aimant sur mon montage => peu de flux du champ magnétique => où la tension est vraiment faible.
  
( d'après les simulations cette méthode par pointage ne fonctionnera sans doute pas si il y a trop d'aimants car la zone "peu aimantée" disparaitra et on passera rapidement du champ d'un aimant à l'autre, l'assymétrie du dispositif sera plsu compliquée à voir. Mais on peut faire par analyse de fréquence ou temps entre coupures du 0 après filtrage passe bas judicieux, le tout est de savoir la disposition des aimants, d'où viennent les données, comment on les regroupe pour avoir plusieurs mesures cohérentes de la même expérience, et comment on les traite)



Les frottements sont désirables pour que la roue ralentisse et parcourre une large gamme de vitesses sur un temps de mesure raisonnable, mais ne ralentisse pas trop vite non plus car l'hypothèse de vitesse constante sur un tour ne tient alors plus. :(
L'appareil de mesure utilisé et la longueur maximale de l'enregistrement importe aussi. A des vitesses raisonnables un sampling rate 1kHz suffit à avoir des courbes bien échantillonées mais me limitait à ~8sec d'enregistrement.

Attention aussi au matériau de l'axe support pour la bobine, un axe en aluminium fait baisser la fem induite, tandis qu'un axe en fer l'augmente mais en ajoutant un problème de fixation: quand aimant passe il est viollemment attiré vers celui-ci.

Pour les aimants: des aimants en néodyme rectangulaires ont été utilisés.

### contenu du répertoire:
❤ = important

-> data & data_old (mesures au format csv)\
-> **viz** (tracé des mesures au format jpeg) utile de regarder vite fait\
-> assets (images et autres uties pour compte rendu)\
-> sim (je sais plus... pour la vraie simul /!\ voir -> `teslametre`)\
-> ❤ **teslametre** (mesures de B(vecteur) . n (vecteur normal à la bobine) dans l'espace 5mm/5mm sur un large carré de 10cm de côté 21x21 mesures)\
  ----> mesuresB_n.csv - (les mesures en question /!\ décalage sur les x sûrement dû à un décalage de l'élément hall dans la sonde du lycée pas forcément au "0" car plastique devant pour protéger)\
  ----> mod_dist, mod_lat, et viz normalement commentés? je sais plus...\
-> ❤ **pipeline**: gestion des fichiers de mesure et traitement du signal avec interface visuelle - voir [Pipeline.md](https://github.com/FuriousBird/TIPE_Dynamo/tree/main/pipeline#readme) pour plus  d'explication sur l'usage\
  ----> labeling.py: outil visuel de pointage (que si les choses à pointées sont centrées sur le 0 mais modifiable rapidos avec chatGpt *wink wink*\
  ----> ❤ **speed_dist.py/speed_dist.ipynb**: utilise les mesures spécifiées dans [/interesting_mes.txt](https://github.com/FuriousBird/TIPE_Dynamo/blob/main/interesting_mes.txt) pour tracer les courbes vitesse / amplitude (à modifier en fait je sais plus ce qu'il fait exactement)\
main.py\
⚠ MCOT PAS EXEMPLAIRE (CATASTROPHE mais c'est passé)\
tout ce qui touche à reelight et son dispositif d'induction est accessible en démontant votre dispositif perso avec du matériel de consommateur et je me dégage de toute responsabilité sur l'utilisation que vous ferez de ces infos, le dispositif pouvant être breveté, je peux seulement conclure qu'ils utilisent les effets magnétiques démontrés dans ce TIPE pour optimiser leur circuit.\
[Présentation finale PowerPoint](https://github.com/FuriousBird/TIPE_Dynamo/blob/main/presentation_final.pdf) ON REMARQUERA QUE JE PARS D'UN PROBLEME DE SOCIETE DE SECURITE ROUTIERE et de signalisation de nuit pour introduire l'importance vitale du sujet. Sur un autre thème cette intro doit être adaptée.\
README.md

# ⚠⁉ WHAT
> bref c'est le bordel ça a évolué et tout est pas toujours bien rangé mais il y a des mesures vraiment utiles et on peut voir ci-dessous l'efficacité du processus pour obtenir des résultats cohérents.

### Commentaires de mesure:

data: mesures récentes après avoir observé (malheureusement un peu tard) un mauvais départ de la plupart des mesures.
les mesures anciennes sont appellées "zcope", les nouvelles: "gcope".
points les plus intéressants: interesting_mes.txt

![une mesure correcte avec un bon nombre de périodes](viz/gcope_27.jpg)

après labellisation avec mon outil: `pipeline/labeling`
on peut calculer la vitesse du vélo par rapport à la route 2\*pi\*R/T avec T la période de rotation et R le rayon de la roue\
si on scatter les amplitudes de chaque mesure intéressante en fonction de la vitesse pour différentes distances. On montre la linéarité de l'amplitude en fonction de la vitesse. Pondérée par un facteur de distance à l'évolution plus compliquée et loin de l'idéalité (dipôle parfait cours de e-mag)

![](assets/ampl_vitesse.png)

Mesures de champ mag, carto: forte possibilité d'erreur au centre car valeur importante et décroissance latérale très rapide

<img width="463" height="495" alt="Untitled" src="https://github.com/user-attachments/assets/4ee05938-da45-4b84-8b4c-a1b8bf9f7aed" />


Résultats de simul superposés avec vraie mesure ~15km/h l'amplitude double est dûe au modèle de bobine plate considéré, loin de la bobine réelle qui possède une profondeur.
Le dispositif commercial utilise aussi des fils de cuivre plus fins (plus de tours sur une même surface) sur un coeur en ferrite pour guider les lignes de champ magnétique et augmenter son flux dans la bobine et donc sa variation depuis/vers cette valeur max élevée qui se traduit en Force Electromotrice Induite -> attention à la chute de tension sur des dispositifs à faible impédance, qui peut aussi être étudiée.

<img width="544" height="756" alt="image" src="https://github.com/user-attachments/assets/e4ce8f85-9739-4b9a-9b84-7244d7cee3bb" />
