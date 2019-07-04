# some-urbangreens

### Understanding the use of urban green spaces from user-generated geographic information
Scripts and documentation related to the analysis of urban green area use.

1. [**Green space polygons**](vihersome-green-areas.md)
2. **Point data pre-processing**
    * [PPGIS data](preprocess_ppgis.py)
    * [Social media data](preprocess_socialmedia.py)
3. **Hotspot comparison**
    * [join points to grid](data_to_grid.py)
    * [calculate jaccard index](calculate_jaccard.py)
4. **Plotting temporal trends**
5. **Content analysis of social media data**
    * **Venn-diagrams**
    * **Treemap**
6. **languages**


#### Input data about green area use / values

*Input data sets covering the city of Helsinki. Number of records and users before any kind of filtering or further selection*


|    Name                 |    Type                  |    Source                                                                   |    Date range                    |    Records, whole city    |    Users, whole city    |
|-------------------------|--------------------------|-----------------------------------------------------------------------------|----------------------------------|---------------------------|-------------------------|
|    Flickr 2015          |    Social media          |    Flickr API                                                               |    1/1/2015-31/12/2015           |    29287                  |    902                  |
|    Instagram 2015       |    Social media          |    Instagram API                                                            |    1/1/2015-31/12/2015           |    602466                 |    113754               |
|    Twitter 2017         |    Social media          |    Twitter API                                                              |    1/1/2017-31/12/2017           |    31359                  |    5386                 |
|    PPGIS 2013           |    PPGIS Survey          |    City of Helsinki;    [Helsinki 2050 survey](https://hri.fi/data/en_GB/dataset/helsinki-2050-kyselyn-vastaukset)                                |    4/11/2013-9/12/2013           |    28250                  |    2588                 |
|    PPGIS 2017           |    PPGIS Survey          |    City of Helsinki; [questionnaire about Helsinki’s   national city park](https://hri.fi/data/en_GB/dataset/helsingin-kansallinen-kaupunkipuisto-kyselyn-vastaukset)    |         xx/xx/2017-17/12/2017    |    10939                  |    1385                 |
|    Strava 2015          |    Sports application    |    Strava METRO data set                                                    |    1/1/2015-31/12/2015           |    161946                 |    4044                 |
|    Mobile phone data    |    Mobile phone data     |    Mobile phone operator                                                    |                                  |                           |                         |
