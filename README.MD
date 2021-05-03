Straight Cylinder with Sinkers

This is a document for a fish cage that similar to the simulations in Section 4.3.4 from this [paper](https://doi.org/10.1016/j.aquaeng.2020.102070), but with a bottom netting. 

> Cheng, H., Li, L., Aarsæther, K.G. and Ong, M.C., 2020. Typical hydrodynamic models for aquaculture nets: A comparative study under pure current conditions. *Aquacultural Engineering*, *90*, p.102070.



![img](https://ars.els-cdn.com/content/image/1-s2.0-S014486091930216X-gr20_lrg.jpg)

*The fish cage in still water*



## File structures:

- **asterinput**
  - [**module**](/Documents/module.md)
  - asterinput1.py  --> calculation script
  - asterinput2.py --> calculation script
  - ASTERRUN.export  -->  submit job for code aster

* clean.sh --> clean the generated files

* run.sh --> start the simulation

* [setting.py](Documents/setting.md)



## Work environments

Required packages:

* [python 3.6 (or higher)](https://www.python.org/)

* [Numpy 1.20 (or higher)](https://numpy.org/)

* [Code_aster 14.6 (or higher stable version)](https://www.code-aster.org/spip.php?article272)

  Please check if `as_run` located at the following default installation path:

  > /opt/aster146/bin/as_run

  If not, you need to change Line 16  in [`run.sh`](Example/run.sh) and  Line 2 in [`ASTERRUN.export`](Example/asterinput/ASTERRUN.export) according to your environments.

* [salome_meca 2019.0.3](https://www.code-aster.org/spip.php?article303)

  Please check if `salome` located at the following default installation path:

  Default installation path:

  > /opt/salome_meca/appli_V2019.0.3_universal/salome
  
  If not, you need to change Line 2  in  [`run.sh`](Example/run.sh) according to your environments.
## How to start the job

*Easy and Fun*

1. Open a terminal and change the directory to the `Example`

2. Type the command:

   ``` shell
   sh run.sh
   ```

3. Wait until the job finish. If it shows `exit_code=0` at the end, it means the simulation finish without any error.

```
 
 ---------------------------------------------------------------------------------
                                            cpu     system    cpu+sys    elapsed
 ---------------------------------------------------------------------------------
   Preparation of environment              0.00       0.00       0.00       0.00
   Copying datas                           0.09       0.02       0.11       0.11
   Code_Aster run                       1380.66      31.55    1412.21    1394.90
   Copying results                         0.02       0.04       0.06       0.05
 ---------------------------------------------------------------------------------
   Total                                1381.01      31.67    1412.68    1395.36
 ---------------------------------------------------------------------------------

as_run 2020.0

------------------------------------------------------------
--- DIAGNOSTIC JOB : <A>_ALARM
------------------------------------------------------------


EXIT_CODE=0
Change the variable back to the default value....>>>>>>

```



* Want to clean the generated file and run a different cases? use `sh clean.sh ` to clean these files and run again. 

  



