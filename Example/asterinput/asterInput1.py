# ----------------------------------
# --   University of Stavanger    --
# --           Hui Cheng          --
# ----------------------------------
# Any questions about this code,
# please email: hui.cheng@uis.no
import sys
import os
import time
import numpy as np


cwd="PATH_OF_THE_CURRENT_FOLDER"
sys.path.append(os.path.join(cwd,'asterinput/module'))  
import hydroModules as hdm


DEBUT(PAR_LOT='NON',
IGNORE_ALARM=("SUPERVIS_25","DISCRETE_26","UTILITAI8_56")
)
# read meshinfo
INCLUDE(UNITE=90)

dt=0.1

duration=10
itimes=int(duration/dt)
tend=itimes*dt
Uinput = meshinfo['caseInfo']['Environment']['current']
Fnh= []
NODEnumber=meshinfo['numberOfNode']
l=['None']*((NODEnumber+1))

# define hydrodynamic objects
netting=hdm.two_dimensional.screenModel("S4",
                                        meshinfo['surfs_netting'],
                                        meshinfo['caseInfo']['Net']['Sn'], 
                                        meshinfo['caseInfo']['Net']['twineDiameter'], 
                                        meshinfo['dwh'])
pipes_top=hdm.one_dimensional.morisonModel("M4",
                                       meshinfo['Lines_pipe_top'],
                                       0, 
                                       meshinfo['caseInfo']['Frame']['topring_sec_dia'], 
                                       meshinfo['caseInfo']['Frame']['topring_sec_dia'])

rope=hdm.one_dimensional.morisonModel("M4",
                                       meshinfo['Lines_rope'],
                                       0, 
                                       meshinfo['caseInfo']['Frame']['rope_sec_dia'], 
                                       meshinfo['caseInfo']['Frame']['rope_sec_dia'])

wake=hdm.weak_effect.net2netWeak('factor-0.8',meshinfo['Nodes'],netting.output_hydro_element(),Uinput,meshinfo['caseInfo']['Net']['Sn'])
NO_net=len(netting.output_hydro_element())
# output info for the hydrodynamic elements
with open(cwd+'/asteroutput/hydro_elements.txt', "w") as file:
    file.write('netting\n')
    file.write(str(netting.output_hydro_element()))
    file.write("\n\n")
    file.write('pipes_top\n')
    file.write(str(pipes_top.output_hydro_element()))
    file.write("\n\n")
    file.write('rope\n')
    file.write(str(rope.output_hydro_element()))
    file.write("\n\n")
file.close()

# read mesh
mesh = LIRE_MAILLAGE(UNITE=20)

# define element type
model = AFFE_MODELE(AFFE=(_F(GROUP_MA=('twines','ropes'),
                             MODELISATION=('CABLE'),
                             PHENOMENE='MECANIQUE'),
                          _F(GROUP_MA=('topRings',),
                             MODELISATION=('POU_D_E'),
                             PHENOMENE='MECANIQUE')                             
                          ),
                    MAILLAGE=mesh)

# define element geometrical properties                    
elemprop = AFFE_CARA_ELEM(CABLE=(_F(GROUP_MA=('twines'),
                                   N_INIT=10.0, 
                                   SECTION=0.25*np.pi*pow(meshinfo['caseInfo']['Net']['twineDiameter']*25,2)), # 25 twines as a seam
                                 _F(GROUP_MA=('ropes'),
                                   N_INIT=40.0,
                                   SECTION=0.25*np.pi*pow(meshinfo['caseInfo']['Frame']['rope_sec_dia'],2)),
                                ),                                 
                       POUTRE=(_F(GROUP_MA=('topRings' ),
                                    SECTION='CERCLE',
                                    CARA=('R', 'EP'),
                                    VALE=(meshinfo['caseInfo']['Frame']['topring_sec_dia']/2, 
                                          meshinfo['caseInfo']['Frame']['topring_thickness'])),  
                              ),                                      
                          MODELE=model)
# material base
# netting according to SCTsetting.py
net = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                     ELAS=_F(E=meshinfo['caseInfo']['Net']['netYoungmodule'], 
                             NU=0.3,  # No meaning for 1D element
                             RHO=meshinfo['caseInfo']['Net']['netRho'])) 
# PE rope
pe = DEFI_MATERIAU(CABLE=_F(EC_SUR_E=0.0001),
                     ELAS=_F(E=1e9, 
                             NU=0.2,
                             RHO=1100.0))  
# hdpe                             
hdpe = DEFI_MATERIAU(ELAS=_F(E=3e9,
                             NU=0.2,
                             RHO=958.0))                       

fieldmat = AFFE_MATERIAU(AFFE=(_F(GROUP_MA=('twines',),
                                  MATER=(net)),
                               _F(GROUP_MA=('ropes',),
                                  MATER=(pe)),
                               _F(GROUP_MA=('topRings'),
                                  MATER=(hdpe)),                      
                               ),
                         MODELE=model)
                                              
# load
gF = AFFE_CHAR_MECA(PESANTEUR=_F(DIRECTION=(0.0, 0.0, -1.0),
                                 GRAVITE=9.81,
                                 GROUP_MA=('twines','ropes','topRings')),
                      MODELE=model)
          
fixed = AFFE_CHAR_MECA(DDL_IMPO=_F(GROUP_NO=("ring_top"),
                                   LIAISON='ENCASTRE'),
                             MODELE=model)

                                               
sinkF1= AFFE_CHAR_MECA(FORCE_NODALE=(_F(GROUP_NO=("bottom_tip"),
                                      FX=0,
                                      FY=0,
                                      FZ=-meshinfo['caseInfo']['Frame']['weight_tip'],  
                                      ),
                                    _F(GROUP_NO=("ring_bottom"),
                                      FX=0,
                                      FY=0,
                                      FZ=-meshinfo['weight_NT'],  
                                      ),
                                      ),
                      MODELE=model) 
                                               

listr = DEFI_LIST_REEL(DEBUT=0.0,
                       INTERVALLE=_F(JUSQU_A=tend,PAS=dt))

times = DEFI_LIST_INST(DEFI_LIST=_F(LIST_INST=listr,PAS_MINI=1e-8),
                       METHODE='AUTO')



for k in range(0,itimes):
    INCLUDE(UNITE=91,INFO=0)



#group HDPE pipes
stat2=CALC_CHAMP(
	RESULTAT=resn,
	GROUP_MA = ('topRings',),
	CONTRAINTE=(
      'EFGE_ELGA',
      'EFGE_ELNO',
      'SIPO_ELNO',),
)


#group CABLE
stat3=CALC_CHAMP(
	RESULTAT=resn,
	GROUP_MA = ('twines','ropes'),
	CONTRAINTE=(
      'EFGE_ELGA',
      'EFGE_ELNO',
      ),
)
# reaction force 
stat = CALC_CHAMP(RESULTAT=resn,
                  CONTRAINTE=('SIEF_ELNO',
                              ),
                  FORCE=('REAC_NODA', ),
                  )
# write results
IMPR_RESU(FORMAT='MED',
          RESU=(_F(CARA_ELEM=elemprop,
                  LIST_INST=listr,
                  NOM_CHAM=('DEPL','SIEF_ELGA'),
                  # TOUT_CMP=(DEPL','ACCE','VITE' ),
                  RESULTAT=resn,
                  TOUT_CMP='OUI'),
               _F(GROUP_MA=('topRings',),
                  RESULTAT=stat2,
                  NOM_CHAM=('EFGE_ELGA', 'EFGE_ELNO','SIPO_ELNO'
                           ),),
               _F(GROUP_MA=('twines','ropes'),
                  RESULTAT=stat3,
                  NOM_CHAM=('EFGE_ELGA', 'EFGE_ELNO',
                           ),),                           
               ),
          UNITE=80)

reac1 = POST_RELEVE_T(ACTION=_F(GROUP_NO=('ring_top'),
                               INTITULE='sum reactions',
                               MOMENT=('DRX', 'DRY', 'DRZ'),
                               NOM_CHAM=('REAC_NODA'),
                               OPERATION=('EXTRACTION', ),
                               POINT=(0.0, 0.0, 0.0),
                               RESULTANTE=('DX', 'DY', 'DZ'),
                               RESULTAT=stat))                            


IMPR_TABLE(FORMAT_R='1PE12.3',
           TABLE=reac1,
           UNITE=10)                    

FIN()
            
    







