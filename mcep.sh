#!/bin/bash 

sox $1.wav $1_short.raw
sptk x2x +sf $1_short.raw > $1.raw
sptk frame -l 320 -p 160 $1.raw | sptk window -l 320 -L 512 | sptk mcep -a 0.42 -m 12 -l 512 | sptk x2x +fa13 > ./mcep/$1_mcep.txt
#sptk frame -l 320 -p 160 $1.raw | sptk window -l 320 -L 512 | sptk mcep -a 0.42 -m 12 -l 512 | sptk vstat -l 13 -o 1 | sptk x2x +fa13 > ./mcep/$1_mcep_averege.txt
#sptk frame -l 320 -p 160 $1.raw | sptk window -l 320 -L 512 | sptk mcep -a 0.42 -m 12 -l 512 | sptk vstat -l 13 -o 2 | sptk x2x +fa13 > ./mcep/$1_mcep_covariant.txt

sptk x2x +sf ./zvucni_i_bezvucni/zvucni_short.raw > ./zvucni_i_bezvucni/zvucni.raw
sptk frame -l 320 -p 160 ./zvucni_i_bezvucni/zvucni.raw | sptk window -l 320 -L 512 | sptk mcep -a 0.42 -m 12 -l 512 | sptk vstat -l 13 -o 1 | sptk x2x +fa13 > ./mcep/zvucni_mcep_averege.txt
sptk frame -l 320 -p 160 ./zvucni_i_bezvucni/zvucni.raw | sptk window -l 320 -L 512 | sptk mcep -a 0.42 -m 12 -l 512 | sptk vstat -l 13 -o 2 | sptk x2x +fa13 > ./mcep/zvucni_mcep_covariant.txt

sptk x2x +sf ./zvucni_i_bezvucni/bezvucni_short.raw > ./zvucni_i_bezvucni/bezvucni.raw
sptk frame -l 320 -p 160 ./zvucni_i_bezvucni/bezvucni.raw | sptk window -l 320 -L 512 | sptk mcep -a 0.42 -m 12 -l 512 | sptk vstat -l 13 -o 1 | sptk x2x +fa13 > ./mcep/bezvucni_mcep_averege.txt
sptk frame -l 320 -p 160 ./zvucni_i_bezvucni/bezvucni.raw | sptk window -l 320 -L 512 | sptk mcep -a 0.42 -m 12 -l 512 | sptk vstat -l 13 -o 2 | sptk x2x +fa13 > ./mcep/bezvucni_mcep_covariant.txt
