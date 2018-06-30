# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib
import matplotlib.pyplot as plt
import seaborn
import scipy
import shutil
import os
import subprocess
from scipy.optimize import fsolve
import Levenshtein

seaborn.set_style("dark")
matplotlib.rcParams['figure.figsize'] = (16, 6)

import numpy as np
import pysptk
from scipy.io import wavfile

# plotting utility
def pplot(sp, envelope, title="no title"):
    plt.plot(sp, "b-", linewidth=2.0, label="Original log spectrum 20log|X(w)|")
    plt.plot(20.0/np.log(10)*envelope, "r-", linewidth=3.0, label=title)
    plt.xlim(0, len(sp))
    plt.xlabel("frequency bin")
    plt.ylabel("log amplitude")
    plt.legend(prop={'size': 20})

def brisanjeIStvaranjeFoldera():
    files=os.listdir('.')
    for i in (files):
        if i == 'spojeni':
            shutil.rmtree(i)
        if i == 'mcep':
            shutil.rmtree(i)
        if i == 'zvucni_i_bezvucni':
            shutil.rmtree(i)
    os.mkdir('spojeni')
    os.mkdir('mcep')
    os.mkdir('zvucni_i_bezvucni')
    
    alphabet=[]
    for letter in range (97,113):
        alphabet.append(chr(letter))
    for letter in range (114,119):
        alphabet.append(chr(letter))
    alphabet.append('S')  #š
    alphabet.append('cc') #č
    alphabet.append('DZ') #dž
    alphabet.append('z')
    alphabet.append('Z') #ž
    alphabet.append('L') #lj
    alphabet.append('N') #nj

    
    for letter in alphabet:
        f= open('./spojeni/'+letter+'.txt','w')
        f.close
        f= open('./spojeni/'+letter+':.txt','w')
        f.close
    
    alphabet.append('uzdah')
    f= open('./spojeni/uzdah.txt','w')
    f.close
    alphabet.append('sil')
    f= open('./spojeni/sil.txt','w')
    f.close
    f= open('./zvucni_i_bezvucni/zvucni.txt','w')
    f.close
    f= open('./zvucni_i_bezvucni/bezvucni.txt','w')
    f.close
    return

def rezanjeGlasova(ucitani_lab, zvucni_signal):
    for i in range (np.size(ucitani_lab)):
        simbol = ucitani_lab[i]['simbol'].decode('UTF-8')
        begin= int(ucitani_lab[i]['start']*0.0016)
        end = int(ucitani_lab[i]['end']*0.0016)
        signal_glasa = zvucni_signal[begin:end]
        f = open('./spojeni/'+simbol+'.txt','a')
        for i in signal_glasa:
            f.write(str(i)+'\n')
        f.close()
    return

brisanjeIStvaranjeFoldera()
n_uciti=20
wav_files = os.listdir( './wav datoteke' )[0:n_uciti]
lab_files = []
for i in wav_files:
    lab_files.append(i[0:-4]+'.lab')
#print(wav_files)
#print(lab_files)

for i in range(len(wav_files)):    
    fs, zvucni_signal = wavfile.read( './wav datoteke/' + wav_files[i])
    assert fs == 16000
    content = np.loadtxt( './lab datoteke/' + lab_files[i], dtype={'names': ('start', 'end', 'simbol'), \
                                             'formats': (np.int, np.int, 'S4')})#, unpack=True)
    rezanjeGlasova(content, zvucni_signal)

def brisanjePraznihZvukova():
    file_path='./spojeni'
    files=os.listdir(file_path)
    for i in files:
        f = open(file_path+'/'+i,'r')
        content = f.readlines()
        f.close()
        duljina_f=len(content)
        if (duljina_f==0):
            os.remove(file_path+'/'+i)

def zvucniIBezvucni():
#   zapisivanje signala u zvucne i bezvucne tekstualne datoteke
#   zvucni glasovi = a, e, i, o, u, j, l, lj, m, n, nj, r, v, b, d, g, z, ž, dž, đ
#   bezvucni = p, t, k, s, š, č, ć, c, h, f 
    file_path='./spojeni'
    file=os.listdir(file_path)
    content_bezucni = [] #bezvucni.readlines()
    content_zvucni = [] #zvucni.readlines()
    for i in file:
        doc = open('./spojeni/' + i,'r')
        content = doc.readlines()
        doc.close()
        if i == 'p.txt' or i == 't.txt' or i == 'k.txt' or i == 's.txt' or i == 'S.txt'\
        or i == 'C.txt' or i == 'cc.txt' or i == 'c.txt' or i == 'h.txt' or i == 'f.txt':
            for i in range(len(content)):
                content_bezucni.append(content[i])
        if i != 'uzda.txt' or i != 'sil.txt' or i != 'uzdah.txt':
            for i in range(len(content)):
                content_zvucni.append(content[i])
        #else:
        #    for i in range(len(content)):
        #        content_zvucni.append(content[i])
    bezvucni = open('./zvucni_i_bezvucni/bezvucni.txt','w')
    bezvucni.writelines(content_bezucni)
    bezvucni.close()
    zvucni = open('./zvucni_i_bezvucni/zvucni.txt','w')
    zvucni.writelines(content_zvucni)
    zvucni.close()
            
brisanjePraznihZvukova()
zvucniIBezvucni()

zvucni=np.genfromtxt('./zvucni_i_bezvucni/zvucni.txt')
bezvucni=np.genfromtxt('./zvucni_i_bezvucni/bezvucni.txt')
zvucni.astype('int16').tofile('./zvucni_i_bezvucni/zvucni_short.raw')
bezvucni.astype('int16').tofile('./zvucni_i_bezvucni/bezvucni_short.raw')

#Provjera raw datoteke
#fs, x = wavfile.read('proba.wav')
#assert fs == 16000
#bezvucni=np.genfromtxt('./zvucni_i_bezvucni/bezvucni.txt')
#zvucni=np.genfromtxt('./zvucni_i_bezvucni/zvucni.txt')
#
#x.astype('int16').tofile('svasta.raw')
#
#stvaranje_txt = open('provjera_x.txt','w')
#stvaranje_txt.write(' ')
#stvaranje_txt.close()
#content=[]
#for i in range(len(x)):
#    content.append(str(x[i])+'\n')
#pisanje_txt = open('provjera_x.txt','w')
#pisanje_txt.writelines(content)
#pisanje_txt.close()
#otvori_provjera_x=np.genfromtxt('provjera_x.txt')
#otvori_provjera_x.astype('int16').tofile('provjera_x.raw')

#mcep_srednja_vrijednost = np.average(mcep_transp, axis = 1)
#mcep_covariant = np.cov(mcep_transp)
#print(mcep_covariant)
#napraviti za zvucne i bezvucne mcep


#__________________________________________________

file = 'proba'
cmd = 'bash mcep.sh %s' % (file)
proc = subprocess.Popen(cmd.split(), cwd='./', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()
print (out, err)
print(' - Obrada Govora finished! %s' % file)
exit_code = proc.wait()
print(' - Return code:', exit_code)

mcep_bezvucni_average = np.loadtxt('./mcep/bezvucni_mcep_averege.txt')#, usecols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
mcep_bezvucni_covariant = np.loadtxt ('./mcep/bezvucni_mcep_covariant.txt')
mcep_zvucni_average = np.loadtxt('./mcep/zvucni_mcep_averege.txt')
mcep_zvucni_covariant = np.loadtxt ('./mcep/zvucni_mcep_covariant.txt')
mcep_test = np.loadtxt('./mcep/'+file+'_mcep.txt')

mcep_covariant_b_transp = np.linalg.inv(mcep_bezvucni_covariant)
mcep_covariant_z_transp = np.linalg.inv(mcep_zvucni_covariant)

lista_charactera_euclidean=[]
for i in range (len(mcep_test)):
    euclidean_distance_bezvucni = scipy.spatial.distance.euclidean( mcep_test [i][1:13], mcep_bezvucni_average [1:13])
    euclidean_distance_zvucni = scipy.spatial.distance.euclidean( mcep_test [i][1:13], mcep_zvucni_average [1:13])
    if euclidean_distance_bezvucni < euclidean_distance_zvucni:
#        print('bezvucni glas')
        for i in range(10):
            lista_charactera_euclidean.append('B')
    else:
        for i in range(10):
            lista_charactera_euclidean.append('Z')
#        print('zvucni glas')

lista_charactera_mahalanobis=[]
for i in range (len(mcep_test)):
    mahalanobis_distance_bezvucni = scipy.spatial.distance.mahalanobis( mcep_test [i], mcep_bezvucni_average, mcep_covariant_b_transp )
    mahalanobis_distance_zvucni = scipy.spatial.distance.mahalanobis( mcep_test [i], mcep_zvucni_average, mcep_covariant_z_transp )
    if mahalanobis_distance_bezvucni < mahalanobis_distance_zvucni:
#        print('bezvucni glas')
        for i in range(10):
            lista_charactera_mahalanobis.append('B')
    else:
        for i in range(10):
            lista_charactera_mahalanobis.append('Z')
#        print('zvucni glas')

#print(lista_charactera)
#
#ponavljanje=[0]
#for i in range (len(glas)-1):
#    if glas[i] == glas[i+1]:
#        ponavljanje.append(1)
#    else:
#        ponavljanje.append(0)
#print (ponavljanje)

min_ponavljanja = 3
ponavljanje = 1
flag = 0

for i in range (1,len(lista_charactera_mahalanobis)-2):
    if (i == (len(lista_charactera_mahalanobis)-3)) :
        flag = 0
        print ("false")
    if (lista_charactera_mahalanobis[i] == lista_charactera_mahalanobis[i-1]):
        ponavljanje = ponavljanje + 1
        flag = 0
    else : flag = 1
    if (flag == 1) :
#        print('ponavljanje'+str(ponavljanje))
        if (ponavljanje < min_ponavljanja):
            for j in range (i-ponavljanje,i) :
#                print('i= '+str(i))
#                print('j= '+str(j))
                lista_charactera_mahalanobis[j] = lista_charactera_mahalanobis[j-1]
                #if (lista_charactera[j] == 'B'): lista_charactera[j] = 'Z'
                #else : lista_charactera[j] = 'B'               
        ponavljanje = 1

#for i in range (len(lista_charactera_mahalanobis)-3, len(lista_charactera_mahalanobis)):
#    lista_charactera_mahalanobis[i]=lista_charactera_mahalanobis[i-1]

test_to_lab = []
broj_ponavljanja = 1
for i in range (1,len(lista_charactera_mahalanobis)):
    if lista_charactera_mahalanobis[i] == lista_charactera_mahalanobis[i-1]:
        broj_ponavljanja = broj_ponavljanja + 1
        flag = 0
    else:
        flag = 1
    if flag == 1:
        test_to_lab.append([ (i-broj_ponavljanja)*10000 , i*10000 , lista_charactera_mahalanobis[i-1] ])
        broj_ponavljanja = 1
        
#print(test_to_lab)
content = []
for i in range(len(test_to_lab)):
    content.append( str(test_to_lab[i][0])+'\t'+str(test_to_lab[i][1])+'\t'+test_to_lab[i][2]+'\n')
    
f= open('obrada.lab','w')
f.writelines(content)
f.close()

test_lab = np.loadtxt( 'proba.lab', dtype={'names': ('start', 'end', 'simbol'), \
                                          'formats': (np.int, np.int, 'S4')})#, unpack=True)    

#treba usporediti udaljenost izmedu vektora simbols_in_lab i vektora lista_charactera_mahalanobis
simbols_in_lab = []
for i in range (len(test_lab)):
    simbol = test_lab[i]['simbol'].decode('UTF-8')
    begin= int(test_lab[i]['start'])
    end = int(test_lab[i]['end'])
    trajanje_signala = int ((end-begin)/1e4)
    #print (trajanje_signala)
    if simbol == 'p' or simbol == 't' or simbol == 'k' or simbol == 's' or simbol == 'S'\
    or simbol == 'C' or simbol == 'cc' or simbol == 'c' or simbol == 'h' or simbol == 'f'\
    or simbol == 'sil' or simbol == 'uzdah' or simbol == 'uzda':
        for i in range (trajanje_signala):
            simbols_in_lab.append('B')
    else:
        for i in range (trajanje_signala):
            simbols_in_lab.append('Z')

proba_to_lab = []
broj_ponavljanja = 1
for i in range (1,len(simbols_in_lab)):
    if simbols_in_lab[i] == simbols_in_lab[i-1]:
        broj_ponavljanja = broj_ponavljanja + 1
        flag = 0
    else:
        flag = 1
    if flag == 1:
#        print('i, broj_ponavljanja %s %s' % (str(i), str(broj_ponavljanja)) )
        proba_to_lab.append([ (i-broj_ponavljanja)*10000 , i*10000 , simbols_in_lab [i-1] ])
        broj_ponavljanja = 1
        
content = []
for i in range(len(proba_to_lab)):
    content.append( str(proba_to_lab[i][0])+'\t'+str(proba_to_lab[i][1])+'\t'+proba_to_lab[i][2]+'\n')
    
f= open('proba_za_usporeit.lab','w')
f.writelines(content)
f.close()

levenstein_distance_euclid = Levenshtein.distance(''.join(lista_charactera_euclidean[0:len(simbols_in_lab)]), ''.join(simbols_in_lab ))
levenstein_distance_mahalanobis = Levenshtein.distance(''.join(lista_charactera_mahalanobis[0:len(simbols_in_lab)]), ''.join(simbols_in_lab ))
corect_mahalanobis = (len(simbols_in_lab) - levenstein_distance_mahalanobis)/len(simbols_in_lab)
corect_euclid = (len(simbols_in_lab) - levenstein_distance_euclid)/len(simbols_in_lab)
print('mahalanobis %s' %str(corect_mahalanobis))
print('euclid %s' %str(corect_euclid))

