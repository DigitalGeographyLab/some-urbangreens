# Understanding the use of urban green spaces from user-generated geographic information

This repository provides supplementary information for the article **Understanding the use of urban green spaces from user-generated geographic information**. 
To cite the article, or any material in this repository, please use the following citation. 

## Citation

**APA:** 

Heikinheimo, V., Tenkanen, H., Bergroth, C., Järv, O., Hiippala, T., & Toivonen, T. (2020). Understanding the use of urban green spaces from user-generated geographic information. Landscape and Urban Planning, 201, 103845, https://doi.org/10.1016/j.landurbplan.2020.103845.


**BibTeX:**
```
@article{HEIKINHEIMO2020103845,
title = "Understanding the use of urban green spaces from user-generated geographic information",
journal = "Landscape and Urban Planning",
volume = "201",
pages = "103845",
year = "2020",
issn = "0169-2046",
doi = "https://doi.org/10.1016/j.landurbplan.2020.103845",
url = "http://www.sciencedirect.com/science/article/pii/S0169204619313635",
author = "Vuokko Heikinheimo and Henrikki Tenkanen and Claudia Bergroth and Olle Järv and Tuomo Hiippala and Tuuli Toivonen",
keywords = "Urban green space, Social media data, Sports tracking data, Mobile phone data, PPGIS",
abstract = "Parks and other green spaces are an important part of sustainable, healthy and socially equal urban environment. Urban planning and green space management benefit from information about green space use and values, but such data are often scarce and laborious to collect. Temporally dynamic geographic information generated by different mobile devices and social media platforms are a promising source of data for studying green spaces. User-generated data have, however, platform specific characteristics that limit their potential use. In this article, we compare the ability of different user-generated data sets to provide information on where, when and how people use and value urban green spaces. We compare four types of data: social media, sports tracking, mobile phone operator and public participation geographic information systems (PPGIS) data in a case study from Helsinki, Finland. Our results show that user-generated geographic information sources provide useful insights about being in, moving through and perceiving urban green spaces, as long as evident limitations and sample biases are acknowledged. Social media data highlight patterns of leisure time activities and allow further content analysis. Sports tracking data and mobile phone data capture green space use at different times of the day, including commuting through the parks. PPGIS studies allow asking specific questions from active participants, but might be limited in spatial and temporal extent. Combining information from multiple user-generated data sets complements traditional data sources and provides a more comprehensive understanding of green space use and preferences."
}
```
 


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



