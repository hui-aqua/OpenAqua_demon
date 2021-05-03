loadr = []
loadr.append(_F(CHARGE=gF), )
loadr.append(_F(CHARGE=fixed), )
loadr.append(_F(CHARGE=sinkF1), )

if k == 0:
    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                         CHAM_MATER=fieldmat,
                         COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                          GROUP_MA=('twines', 'ropes'),
                                          RELATION='CABLE'),
                                       _F(DEFORMATION='PETIT',
                                          GROUP_MA=('topRings',),
                                          RELATION='ELAS'),
                                       ),
                         CONVERGENCE=_F(ITER_GLOB_MAXI=1000,
                                        RESI_GLOB_RELA=2e-5),
                         EXCIT=(loadr),
                         OBSERVATION=_F(GROUP_MA=('twines', 'ropes', 'topRings',),
                                        NOM_CHAM='DEPL',
                                        NOM_CMP=('DX', 'DY', 'DZ'),
                                        INST=k+dt,
                                        OBSE_ETAT_INIT='NON'),
                         SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                         SCHEMA="HHT",
                                         ALPHA=-0.3,
                                         ),
                         # add damping stablize the oscilations Need to study in the future
                         INCREMENT=_F(LIST_INST=times, INST_FIN=(1+k)*dt),
                         MODELE=model)
else:
    Fnh = tuple(Fnh)
    for i in range(1, NODEnumber+1):
        grpno = 'node%01g' % i
        l[i] = AFFE_CHAR_MECA(FORCE_NODALE=_F(GROUP_NO=(grpno),
                                              FX=Fnh[i-1][0],
                                              FY=Fnh[i-1][1],
                                              FZ=Fnh[i-1][2],),
                              MODELE=model)
    for i in range(1, NODEnumber+1):
        loadr.append(_F(CHARGE=l[i],), )

    resn = DYNA_NON_LINE(CARA_ELEM=elemprop,
                         CHAM_MATER=fieldmat,
                         reuse=resn,
                         ETAT_INIT=_F(EVOL_NOLI=resn),
                         COMPORTEMENT=(_F(DEFORMATION='GROT_GDEP',
                                          GROUP_MA=('twines', 'ropes'),
                                          RELATION='CABLE'),
                                       _F(DEFORMATION='PETIT',
                                          GROUP_MA=('topRings',),
                                          RELATION='ELAS'),
                                       ),
                         CONVERGENCE=_F(ITER_GLOB_MAXI=1000,
                                        RESI_GLOB_RELA=2e-5),
                         EXCIT=(loadr),
                         OBSERVATION=_F(GROUP_MA=('twines', 'ropes', 'topRings',),
                                        NOM_CHAM='DEPL',
                                        NOM_CMP=('DX', 'DY', 'DZ'),
                                        INST=k+dt,
                                        OBSE_ETAT_INIT='NON'),
                         SCHEMA_TEMPS=_F(FORMULATION='DEPLACEMENT',
                                         SCHEMA="HHT",
                                         ALPHA=-0.3
                                         ),
                         # add damping stablize the oscilations Need to study in the future
                         INCREMENT=_F(LIST_INST=times, INST_FIN=(1+k)*dt),
                         MODELE=model,
                         )

tblp = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                                INTITULE='Nodal Displacements',    # Name of the table in .resu file
                                # The result from which values will be extracted(STAT_NON_LINE)
                                RESULTAT=resn,
                                # Field to extract. DEPL = Displacements
                                NOM_CHAM=('DEPL'),
                                # TOUT_CMP='OUI',
                                # Components of DISP to extract
                                NOM_CMP=('DX', 'DY', 'DZ'),
                                GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                                # STAT_NON_LINE calculates for 10 INST. I want only last INST
                                INST=(1+k)*dt,
                                ),),
                     )
tblp2 = POST_RELEVE_T(ACTION=(_F(OPERATION='EXTRACTION',      # For Extraction of values
                                 INTITULE='Nodal Displacements',    # Name of the table in .resu file
                                 # The result from which values will be extracted(STAT_NON_LINE)
                                 RESULTAT=resn,
                                 # Field to extract. VITE = velocity,
                                 NOM_CHAM=('VITE'),
                                 # TOUT_CMP='OUI',
                                 # Components of DISP to extract
                                 NOM_CMP=('DX', 'DY', 'DZ'),
                                 GROUP_NO='allnodes',               # Extract only for nodes of group DISP
                                 # STAT_NON_LINE calculates for 10 INST. I want only last INST
                                 INST=(1+k)*dt,
                                 ),),
                      )

posi = hdm.aster.get_position_aster(tblp)
velo_nodes = hdm.aster.get_velocity_aster(tblp2)

if k < itimes-1:
    del Fnh

timeFE = dt*k

elev = np.zeros_like(posi)
u = np.ones((NO_net,3))*Uinput

wake.update_reduction(posi)
u*=wake.reduction_factors


if max(np.linalg.norm(u, axis=1)) > 1500:
    exit()
if k ==0:
    velo_nodes =np.zeros_like(posi)
else:
    velo_nodes = (posi-posi_0)/dt

# netting buoy + dyna
# top pipes buoy + dyna
# rope buoy + dyna
np.savetxt(os.path.join(cwd, 'pythonOutput/netting_'+str(round((k)*dt, 3))+'.txt'),
           netting.cal_buoy_force(posi, elev) + netting.force_on_element(posi, u, velo_nodes*0.1, elev),
           fmt='%.3e')
np.savetxt(os.path.join(cwd, 'pythonOutput/pipe_top_'+str(round((k)*dt, 3))+'.txt'),
           pipes_top.cal_buoy_force(posi, elev) + pipes_top.force_on_element(posi, u, velo_nodes*0.1, elev),
           fmt='%.3e')
np.savetxt(os.path.join(cwd, 'pythonOutput/rope_'+str(round((k)*dt, 3))+'.txt'),
           rope.cal_buoy_force(posi, elev) + rope.force_on_element(posi, u, velo_nodes*0.1, elev),
           fmt='%.3e')

Fnh = netting.distribute_force(len(posi))+pipes_top.distribute_force(len(posi))+rope.distribute_force(len(posi))

np.savetxt(os.path.join(cwd, 'pythonOutput/Fnh_' +
                        str(round((k)*dt, 3))+'.txt'), Fnh, fmt='%.3e')
np.savetxt(os.path.join(cwd, 'pythonOutput/posi_' +
                        str(round((k)*dt, 3))+'.txt'), posi, fmt='%.3e')
np.savetxt(os.path.join(cwd, 'pythonOutput/velo_' +
                        str(round((k)*dt, 3))+'.txt'), velo_nodes, fmt='%.3e')
posi_0=posi

print("save results.....at "+str(timeFE))

DETRUIRE(CONCEPT=_F(NOM=(tblp)))
DETRUIRE(CONCEPT=_F(NOM=(tblp2)))
if k != 0:
    if k < itimes-1:
        for i in range(1, NODEnumber+1):
            DETRUIRE(CONCEPT=_F(NOM=(l[i])))
