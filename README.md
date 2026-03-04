# AI-for-Health-IITGN
**Due to dataset size constraints, raw data is not included.
Please place participant folders inside Data/ directory.**
**1 understanding data & visualization** 
the dataset is huge instead of doing for every data i selected one and did for that it passed so every data will pass this code
the data cointains elements values in single line separated by ";"
so i want to separate those so i used split for that
i converted them into datetime format %d%m%y %h%m%s
i need to do  this for all nasal thoracic spo2 
instaed of repeating this to every thing 
i created base path that will be common for every thing
-------data understanding--------
now comes to plot the graph 
the graph that plot nasal airflow , thoracic movement and spo2 for the full 8hrs of one participant, overlayyy
i create events i used library called pandas  matplotlib.pypllot
for events overlays etc red 
at last visualization.pdf 
import os saved
---------pdf and plotting-------
**2 signal preprocessing and dataset creation**
0.17-0.4hz should be good higher noide lower baseline drift
if Overlap duration / Window duration > 0.5 assign event label
else normal

