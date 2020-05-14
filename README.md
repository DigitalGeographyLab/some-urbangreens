# Understanding the use of urban green spaces from user-generated geographic information

This repository provides supplementary information for the article **Understanding the use of urban green spaces from user-generated geographic information**. 
To cite the article, or any material in this repository, please use the following citation:

Heikinheimo, V. V., Tenkanen, H., Bergroth, C., Järv, O., Hiippala, T., & Toivonen, T. (Accepted/In press). Understanding the use of urban green spaces from user-generated geographic information. Landscape and Urban Planning. 


## Scripts

1. **Point data pre-processing**
    * [Preprocess PPGIS data](scripts/preprocess_ppgis.py)
    * [Get data from postGIS](scripts/get_postgis_data.py)
    * [Preprocess Social media data](scripts/preprocess_socialmedia.py)
2. **Hotspot comparison**
    * [Join points to grid](scripts/data_to_grid.py) 
    * [Join data to green finger polygons](scripts/data_to_greenfingers.py)
    * [Calculate jaccard index](scripts/calculate_jaccard_quantiles.py)
3. **Plotting temporal trends**
    * [Social media](scripts/plot_temporal_social_media.py) 
    * [Strava](scripts/plot_temporal_strava.py)
    * [Mobile phone data](scripts/plot_temporal_mobilephone.py)
4. **Content analysis of social media data**
    * [Plot Venn-diagrams](scripts/plot_venndiagram.py)
    * [Treemap](scripts/plot_treemap.py)
5. **Languages**
    * For language detection using FastText, see [Hiippala et al. 2019](https://doi.org/10.1093/llc/fqy049)
    * [Summarize language info for green areas](scripts/summarize_languages.py)

*Please note that the scripts might contain custom input and output paths outside this repository.*
 
## Data

Details of input data. 

### User-generated data sets

*Input data sets covering the city of Helsinki. Number of records and users before any kind of filtering or further selection.*


|    Name                 |    Type                  |    Source                                                                   |    Date range                    |    Records, whole city    |    Users, whole city    |
|-------------------------|--------------------------|-----------------------------------------------------------------------------|----------------------------------|---------------------------|-------------------------|
|    Flickr               |    Social media          |    Flickr API                                                               |    1/1/2015-31/12/2015           |    29287                  |    902                  |
|    Instagram            |    Social media          |    Instagram API                                                            |    1/1/2015-31/12/2015           |    602466                 |    113754               |
|    Twitter              |    Social media          |    Twitter API                                                              |    1/1/2017-31/12/2017           |    31359                  |    5386                 |
|    PPGIS 2050           |    PPGIS Survey          |    City of Helsinki;    [Helsinki 2050 survey](https://hri.fi/data/en_GB/dataset/helsinki-2050-kyselyn-vastaukset)                                |    4/11/2013-9/12/2013           |    28250                  |    2588                 |
|    PPGIS Park           |    PPGIS Survey          |    City of Helsinki; [questionnaire about Helsinki’s   national city park](https://hri.fi/data/en_GB/dataset/helsingin-kansallinen-kaupunkipuisto-kyselyn-vastaukset)    |         25/10/2017-17/12/2017    |    10939                  |    1385                 |
|    Strava               |    Sports application    |    Strava METRO data set                                                    |    1/1/2015-31/12/2015           |    161946                 |    4044                 |
|    Mobile phone data    |    Mobile phone data     |    Elisa Oyj (the mobile phone operator)                                                   |    28/10/2017–9/1/2018           |                           |                         |

### Green space polygons 

#### Register of public areas

We acquired the extent of public green areas in Helsinki from the register of public areas in the city of Helsinki.

[Description of the data in Helsinki Region Infoshare](https://hri.fi/data/fi/dataset/helsingin-kaupungin-yleisten-alueiden-rekisteri).

WFS query used for retrieving the data:
```
https://kartta.hel.fi/ws/geoserver/avoindata/wfs?request=GetFeature&service=WFS&version=1.1.0&typeName=avoindata:YLRE_Viheralue_alue&outputFormat=kml
```
The database is updated daily, we acquired the latest version on July 1 2019.


#### Green fingers

Green fingers, mostly comprised of recreational forests, form a network of recreational areas across the city.
We acquired a spatial layer of the green fingers based on the VISTRA plan (Jaakkola et al. 2016) from the City of Helsinki. The layer can be viewed online here: https://kartta.hel.fi/link/79hgpR. Read more about the green fingers from the VISTRA II plan (Jaakkola et al. 2016), and the article in Helsinki Quarterly 2/2016 (Hannikainen 2016).

Hannikainen, M. (2016) Helsinki- a compact green city. Helsinki Quarterly 2/2016. Available online at:
http://www.kvartti.fi/en/articles/helsinki-compact-green-city

Jaakkola, M., Böhling, A., Nicklén, M., & Lämsä, A. (2016). Helsingin viher- ja virkistysverkoston kehittämissuunnitelma VISTRA osa II. Helsingin Kaupunkisuunnitteluviraston Asemakaavaosaston Selvityksiä, 2016(2).



