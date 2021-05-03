# ----------------------------------
# --   University of Stavanger    --
# --           Hui Cheng          --
# ----------------------------------
# Any questions about this code,
# please email: hui.cheng@uis.no

{
'Environment':
{
    'current':[0.5,0,0],   
    'fluidDensity':1025,  
},
'CageShape':
  {
    'origin':[[0,0,0]],
    'cageCircumference':120, 
    'bottom_top_ratio':1,
    'cageHeight':34,  
    'cageConeHeight':3,
    'element_length':2.5,   
  },
'Frame':
    {
    'topringDensity':110,
    'topring_sec_dia':0.35,
    'topring_thickness':0.0185,
    'rope_dep':3, 
    'rope_sec_dia':0.05,
    'weight_tip':9800,
    'weight_per_metter':38.13,
    },    
'Net':
  {
    'nettingType':'square',
    'Sn': 0.194,   
    'twineDiameter': 2.42e-3, 
    'meshLength': 25.5e-3, 
    'netYoungmodule':4e7,
    'netRho':1140.0, 
  },
}

