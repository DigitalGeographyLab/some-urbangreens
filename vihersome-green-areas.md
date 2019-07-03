# Green areas


### Green fingers

Green fingers, mostly comprised of recreational forests, form a network of recreational areas across the city.
We acquired a spatial layer of the green fingers based on the VISTRA plan (Jaakkola et al. 2016). The layer can be viewed online here:
 https://kartta.hel.fi/link/79hgpR 

Read more about the green fingers from the VISTRA II plan (Jaakkola et al. 2016), and the article in Kvartti 2/2016 (Hannikainen 2016).

Hannikainen, M. (2016) Helsinki- a compact green city. Helsinki Quarterly 2/2016. Available online at:
http://www.kvartti.fi/en/articles/helsinki-compact-green-city

Jaakkola, M., Böhling, A., Nicklén, M., & Lämsä, A. (2016). Helsingin viher- ja virkistysverkoston kehittämissuunnitelma VISTRA osa II. 
Helsingin Kaupunkisuunnitteluviraston Asemakaavaosaston Selvityksiä, 2016(2).

### Other green areas

We acquired the extent of public green areas in Helsinki from the register of public areas in the city of Helsinki.

**Description of the data in Helsinki Region Infoshare:**

https://hri.fi/data/fi/dataset/helsingin-kaupungin-yleisten-alueiden-rekisteri

**WFS query used for retrieving the data:**
```
https://kartta.hel.fi/ws/geoserver/avoindata/wfs?request=GetFeature&service=WFS&version=1.1.0&typeName=avoindata:YLRE_Viheralue_alue&outputFormat=kml
```
note: the database is updated every day, we acquired the latest version on July 1 2019.


### Open STreet Map

We also explored the possibility of using Open Street Map as input for the green area extent. 