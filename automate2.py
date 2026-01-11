# version 2: correction d'un bug dans la fonction minimisation
import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})
    
    
def concatenation(a1, a2): 
    """Retourne l'automate qui reconnaît la concaténation des 
    langages reconnus par les automates a1 et a2"""
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)

    a = automate("O")
    a.transition = {}
    a.final = []

    decalage = a1.n
    a.n = a1.n + a2.n

    #copies des transitions de a1
    for etat_source, symbole in a1.transition:
        etats_cibles = a1.transition[(etat_source, symbole)]
        a.transition[(etat_source, symbole)] = list(etats_cibles)

    #copies des transitions de a2 en décalant les états
    for etat_source, symbole in a2.transition:
        etats_cibles = a2.transition[(etat_source, symbole)]
        a.transition[(etat_source + decalage, symbole)] = [d + decalage for d in etats_cibles]

    #ajout des ε transitions de tous les états finaux de a1 vers le début de a2
    for q in a1.final:
        a.ajoute_transition(q, "E", [decalage])

    a.final = [q + decalage for q in a2.final]  #les états finaux de a sont ceux de a2 décalés

    a.name = "(" + a1.name + "." + a2.name + ")"
    
    return a


def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2""" 
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)
    a = automate("O") #automate vide

    decalage_a1 = 1
    decalage_a2 = 1 + a1.n

    a.n = 1 + a1.n + a2.n #nb états nouvel automate

    #parcourt toutes les transitions de a1
    for etat_source, symbole in a1.transition:
        etats_cibles = a1.transition[(etat_source, symbole)]
        
        #décale tous les états
        nouvel_etat_source = etat_source + decalage_a1
        nouveaux_etats_cibles = [etat + decalage_a1 for etat in etats_cibles]
        
        #ajoute la transition dans le nouvel automate
        a.transition[(nouvel_etat_source, symbole)] = nouveaux_etats_cibles

    #pareil pour a2
    for etat_source, symbole in a2.transition:
        etats_cibles = a2.transition[(etat_source, symbole)]
        
        nouvel_etat_source = etat_source + decalage_a2
        nouveaux_etats_cibles = [etat + decalage_a2 for etat in etats_cibles]

        a.transition[(nouvel_etat_source, symbole)] = nouveaux_etats_cibles

    a.transition[(0, "E")] = [decalage_a1, decalage_a2]  #ajoute les ε-transitions depuis le nouvel état initial

    a.final = [q + decalage_a1 for q in a1.final] + [q + decalage_a2 for q in a2.final]  #décalage des états finaux et ajout dans a

    a.name = "(" + a1.name + "+" + a2.name + ")"

    return a


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a""" 

    a=cp.deepcopy(a)
    res=automate("O")
    res.name=a.name +"*"

    decalage=1
    res.n=a.n+1
    res.final=[0]
    res.transition={}

    for (etat_source, symbole), etat_cibles in a.transition.items():
                res.transition[(etat_source + decalage, symbole)]=[
                    q + decalage for q in etat_cibles
                ]


    res.ajoute_transition(0,"E", [decalage])

    for qf in a.final:
        res.ajoute_transition(qf+decalage, "E", [decalage,0])
        
        
    return res

def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res
        
        
def determinisation(a):
    """ retourne l'automate équivalent déterministe
        la construction garantit que tous les états sont accessibles
        automate d'entrée sans epsilon-transitions
    """        

    a=cp.deepcopy(a)

    res=automate("O")
    res.name=a.name + "_det"
    res.transition={}
    res.final=[]
    

    etat={}
    L=[]
  
    init=(0,)
    etat[init]=0
    L.append(init)
    res.n=1

    if any(q in a.final for q in init):
        res.final.append(0)

    while L:
        courant=L.pop(0)
        current_index=etat[courant]

        for c in a.alphabet:
          new_part=[]

          for q in courant:
            if(q,c) in a.transition:
                new_part+=a.transition[(q,c)]
            
          if not new_part:
             continue

          new_part=sorted(set(new_part))
          new_part2=tuple(new_part)

          if new_part2 not in etat:
              etat[new_part2]=res.n
              res.n+=1
              L.append(new_part2)

              if any(q in a.final for q in new_part2):
                 res.final.append(etat[new_part2])
 
          res.transition[(current_index,c)]=[etat[new_part2]]

    return res
    
    
def completion(a):
    """Retourne l'automate a complété (a déterministe)"""
    a = cp.deepcopy(a)

    etat_poubelle = a.n 
    besoin_poubelle = False

    #vérifier s'il manque une transition
    for q in range(a.n):
        for c in a.alphabet:
            if (q, c) not in a.transition:
                besoin_poubelle = True

    if not besoin_poubelle:
        return a

    a.n += 1  #ajouter l'état poubelle

    #ajouter les transitions manquantes vers l'état poubelle
    for q in range(a.n):
        for c in a.alphabet:
            if (q, c) not in a.transition:
                a.transition[(q, c)] = [etat_poubelle]

    #boucles sur l'état poubelle
    for c in a.alphabet:
        a.transition[(etat_poubelle, c)] = [etat_poubelle]

    return a


###################################################
# version corrigée de la fonction de minimisation #
###################################################

def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    
    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part
    # on réordonne la partition pour que le premier sous-ensemble soit celui qui contient l'état initial
    for i, e in enumerate(part):
        if 0 in e:
            part[0], part[i] = part[i], part[0]
            break
 
     
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res
    

def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4





def egal(a1, a2):
  """ retourne True si a1 et a2 sont isomorphes
      a1 et a2 doivent être minimaux
  """
  #vérifie le nb d'états
  a1=tout_faire(a1)
  a2=tout_faire(a2)
  if a1.alphabet!=a2.alphabet:
      return False
  if a1.n != a2.n:
      return False
  
  mapping={0: 0}
  reverse={0: 0}
  queue=[0]

  while queue:
        q1=queue.pop(0)
        q2=mapping[q1]

        if (q1 in a1.final)!=(q2 in a2.final):
            return False

        for c in a1.alphabet:
          r1=a1.transition[(q1,c)][0]
          r2=a2.transition[(q2,c)][0]
          
          if r1 in mapping:
              if mapping[r1]!=r2:
                  return False

              continue
          if r2 in reverse:
              return False
          
          mapping[r1]=r2
          reverse[r2]=r1
          queue.append(r1)
  return True


# TESTS
# à écrire









# TESTS
# à écrire

