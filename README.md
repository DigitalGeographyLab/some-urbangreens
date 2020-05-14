# Understanding the use of urban green spaces from user-generated geographic information

This repository provides supplementary information for the article **Understanding the use of urban green spaces from user-generated geographic information**. 
To cite the article, or any material in this repository, please use the following citation:

Heikinheimo, V. V., Tenkanen, H., Bergroth, C., Järv, O., Hiippala, T., & Toivonen, T. (Accepted/In press). Understanding the use of urban green spaces from user-generated geographic information. Landscape and Urban Planning. 


## Contents

Additional details and processing scripts:

1. [**Green space polygons**](vihersome-green-areas.md)
2. **Point data pre-processing**
    * [Preprocess PPGIS data](scripts/preprocess_ppgis.py)
    * [get data from postGIS](scripts/get_postgis_data.py)
    * [Preprocess Social media data](scripts/preprocess_socialmedia.py)
3. **Hotspot comparison**
    * [join points to grid](scripts/data_to_grid.py) 
    * [join data to green finger polygons](scripts/data_to_greenfingers.py)
    * [calculate jaccard index](scripts/calculate_jaccard_quantiles.py)
4. **Plotting temporal trends**
    * [social media](scripts/plot_temporal_social_media.py) 
    * [strava](scripts/plot_temporal_strava.py)
    * [mobile phone data](scripts/plot_temporal_mobilephone.py)
5. **Content analysis of social media data**
    * [Venn-diagrams](scripts/plot_venndiagram.py)
    * [treemap](scripts/plot_treemap.py)
6. **languages**
    * For language detection using FastText, see [Hiippala et al. 2019](https://doi.org/10.1093/llc/fqy049)
    * [summarize language info for green areas](scripts/summarize_languages.py)

#### Input data about green area use / values

*Input data sets covering the city of Helsinki. Number of records and users before any kind of filtering or further selection*


|    Name                 |    Type                  |    Source                                                                   |    Date range                    |    Records, whole city    |    Users, whole city    |
|-------------------------|--------------------------|-----------------------------------------------------------------------------|----------------------------------|---------------------------|-------------------------|
|    Flickr               |    Social media          |    Flickr API                                                               |    1/1/2015-31/12/2015           |    29287                  |    902                  |
|    Instagram            |    Social media          |    Instagram API                                                            |    1/1/2015-31/12/2015           |    602466                 |    113754               |
|    Twitter              |    Social media          |    Twitter API                                                              |    1/1/2017-31/12/2017           |    31359                  |    5386                 |
|    PPGIS 2050           |    PPGIS Survey          |    City of Helsinki;    [Helsinki 2050 survey](https://hri.fi/data/en_GB/dataset/helsinki-2050-kyselyn-vastaukset)                                |    4/11/2013-9/12/2013           |    28250                  |    2588                 |
|    PPGIS Park           |    PPGIS Survey          |    City of Helsinki; [questionnaire about Helsinki’s   national city park](https://hri.fi/data/en_GB/dataset/helsingin-kansallinen-kaupunkipuisto-kyselyn-vastaukset)    |         25/10/2017-17/12/2017    |    10939                  |    1385                 |
|    Strava               |    Sports application    |    Strava METRO data set                                                    |    1/1/2015-31/12/2015           |    161946                 |    4044                 |
|    Mobile phone data    |    Mobile phone data     |    Mobile phone operator                                                    |    28/10/2017–9/1/2018           |                           |                         |
