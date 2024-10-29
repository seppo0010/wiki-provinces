import os.path
from pprint import pprint
from collections import Counter
import pickle
import re
import wikipedia
from unidecode import unidecode
wikipedia.set_lang("es")

provinces = [
    'Buenos_Aires',
    'Provincia_de_Buenos_Aires',
    'Provincia_de_Catamarca',
    'Provincia_del_Chaco',
    'Provincia_del_Chubut',
    'Provincia_de_Córdoba_(Argentina)',
    'Provincia_de_Corrientes',
    'Provincia_de_Entre_Ríos',
    'Provincia_de_Formosa',
    'Provincia_de_Jujuy',
    'Provincia_de_La_Pampa',
    'Provincia_de_La_Rioja_(Argentina)',
    'Provincia_de_Mendoza',
    'Provincia_de_Misiones',
    'Provincia_del_Neuquén',
    'Provincia_de_Río_Negro',
    'Provincia_de_Salta',
    'Provincia_de_San_Juan_(Argentina)',
    'Provincia_de_San_Luis',
    'Provincia_de_Santa_Cruz',
    'Provincia_de_Santa_Fe_(Argentina)',
    'Provincia_de_Santiago_del_Estero',
    'Provincia_de_Tierra_del_Fuego,_Antártida_e_Islas_del_Atlántico_Sur',
    'Provincia_de_Tucumán',
]
forbidden_words = '''
#yanquetruz
#camelidos
#habitante
#schiaretti
#fascio
#virasoro
#candioti
#tonocotes
georgias
tucumano
trelew
riojanos
sanogasta
anillaco
chamical
chaya
cataratas
misionera
piray
eldorado
pepiri
irigoyen
garupa
montecarlo
puntano
dupuy
quijadas
talampaya
mendocinas
lanin
sanjuanino
cholila
arauco
aconcagua
angaco
valdes
picun
leufu
chepes
pocito
chapelco
colo
sanjuaninos
camarones
trevelin
anelo
sanagasta
llancanelo
poma
ullum
feliciano
olta
tupungato
lerma
calingasta
morro
formoseno
rafaela
cordobeses
ushuaia
necochea
esquel
quequen
correntinos
gualeguaychu
clorinda
xibi
calfucura
chilecito
tunuyan
obera
bariloche
salteno
jachal
tolhuin
tafi
madryn
domuyo
moron
goya
concordia
pirane
vilama
cobres
rmba
gualeguay
lomitas
nogoya
laishi
riojano
he
aimogasta
guaymallen
saltena
tulum
paramillos
uspallata
'''.split('\n')
pickle_path = 'data.pickle'
if os.path.exists(pickle_path):
    with open(pickle_path, 'rb') as f:
        counters = pickle.load(f)
else:
    counters = {}
    for p in provinces:
        text = wikipedia.page(p).content
        text = unidecode(text).lower()
        text = re.sub(r'[^a-z]+', ' ', text)
        words = [word for word in text.split(' ') if len(word) > 0]
        counters[p] = Counter(words)
    with open(pickle_path, 'wb') as f:
        pickle.dump(counters, f)

result = {}
for p in provinces:
    for (word, occ) in counters[p].most_common():
        if word in forbidden_words: continue
        found = False
        for other_p in provinces:
            if other_p == p: continue
            if word in counters[other_p]:
                found = True
                break
        if not found:
            result[p] = word
            break
pprint(result)
