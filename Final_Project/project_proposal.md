# Final Project Proposal
**Course:** EAS-G690 – Advanced Earth Science Data Analysis  
**Author:** Rafaela Quintella Veiga  
**Date:** November 2025  

---

## 1. Introduction

Since the beginning of the 21st century, there has been a continuous rise in the global mean temperature. Combined with the current regime of anthropogenic climate change, this warming trend clearly shows that extreme events—particularly heat extremes—have become more frequent, intense, long-lasting, and spatially extensive (NOAA, 2018; Geirinhas et al., 2019). The Sixth Assessment Report of the Intergovernmental Panel on Climate Change (IPCC-AR6) states that it is very likely that both the magnitude and frequency of heat extremes will continue to increase, even under a global mean temperature rise of only 1.5 °C (IPCC, 2021; Seneviratne et al., 2021). This situation is especially concerning in tropical regions, where temperature variability is naturally low, such as Africa, Southeast Asia, and South America. In Brazil, these changes are particularly evident, as studies have already documented increasing frequency and intensity of extreme heat events since the second half of the 20th century (Renom et al., 2011; Cerne e Vera, 2011; Rusticucci, 2012; Hannart et al., 2015; Bitencourt et al., 2016; Ceccherini et al., 2016; ; Rusticucci et al., 2016, 2017; Geirinhas et al., 2017; 2019).

In the Brazilian context, the Southeast Region stands out as one of the most vulnerable areas to extreme heat events, having experienced a steady increase in their frequency, intensity, and duration in recent decades (Geirinhas et al., 2019; 2021). Perkins-Kirkpatrick and Lewis (2020) identified significant positive trends in the intensity and duration of the longest annual heatwaves across South America between 1950 and 2014. Among the most notable events are the summers of 2001 and 2014 (Geirinhas et al., 2019), marked by exceptionally hot and dry conditions that triggered a severe water crisis, deficits in hydropower generation (Herring et al., 2015; Coelho et al., 2016), and an alarming rise in wildfires (Rodrigues et al., 2018). 

The state of Rio de Janeiro has emerged as one of the areas most susceptible to extreme heat events within Southeast Region of Brazil. The year 2023, recognized as the hottest on record globally and in South America (WMO, 2023; Moreira et al., 2024), saw the entire state classified as under “major hazard” by the Brazilian National Institute of Meteorology (INMET), in an alert issued on November 8, 2023, referring to the eighth heatwave recorded in Brazil that year (Dereczynski et al., 2024). In these areas, temperatures up to 5 °C above average were forecast for more than five consecutive days (Dereczynski et al., 2024). During this period, the state’s capital recorded maximum temperatures exceeding 40 °C at several meteorological stations. On November 17, 2023, during a Taylor Swift concert at the Nilton Santos Olympic Stadium in Rio de Janeiro, the extreme heat caused dozens of cases of heat exhaustion, leading to the death of a 23-year-old woman (AP News, 2023; Dereczynski et al., 2024). It is noteworthy that this heatwave occurred prior to the official start of the 2024 summer season (December 2023 to February 2024). According to Marengo and Nobre (2024), 2023 was the hottest year ever recorded in Brazil, with nine heatwave events—representing a nearly sevenfold increase in their national occurrence.

The city of Rio de Janeiro is historically known for its high temperatures, having popularized since the 1990s the expression “Rio 40 Graus” (“Rio 40 Degrees”), in reference to the intense summer heat (Marengo; Camargo, 2008; Moreira et al., 2024). Monteiro dos Santos et al. (2024) reported an increase in both the frequency and duration of heatwaves in Brazilian metropolitan regions, particularly in Rio de Janeiro, between 1970 and 2020. While in the 1970s and 1980s the average frequency was 2.5 events per year (lasting 4 days), in the 2000s and 2010s these values increased to 4 events per year (lasting 5 days). Between 2000 and 2018, an estimated 48,075 excess deaths were attributed to the growing number of heatwaves—over 20 times the number of landslide-related deaths in the same period. During the first quarter of 2024, Rio de Janeiro once again recorded record-breaking air temperatures, with heat index values surpassing 60 °C, as reported by the Alerta Rio municipal system, an event that drew international media attention (Dereczynski et al., 2024).

Beyond the extreme temperatures, Rio de Janeiro exhibits complex socio-spatial vulnerabilities that amplify the impacts of heat extremes (Moreira et al., 2024). These include the increase in respiratory and cardiovascular diseases, the spread of epidemic illnesses (such as dengue, which peaks in summer), and adverse effects on mental health (Câmara et al., 2009; Prosdocimi; Klima, 2020; Ebi et al., 2021; Moreira et al., 2024). However, the territory of Rio de Janeiro is far from homogeneous. Its complex physiography, marked by mountain ranges, valleys, lowlands, bays, and coastal zones, combined with maritime influence and the action of synoptic systems (such as cold fronts, the South Atlantic Convergence Zone (SACZ), and the South Atlantic Subtropical High (SASH)), generates high spatial climate variability (Luiz-Silva; Dereczynski, 2014; Dereczynski et al., 2024). These factors create microclimates that affect temperature distribution and, consequently, the occurrence and spatial behavior of heatwaves.

Although previous studies have pointed to an increase in extreme heat events across the state, detailed spatial analyses that account for intra-state geospatial differences remain scarce. Understanding how heatwaves vary spatially and how their intensity and frequency evolve across the heterogeneous territory of Rio de Janeiro is essential for improving climate risk management and guiding local adaptation strategies, particularly in the current context of global climate change.
Based on this framework, the present study aims to analyze changes in the frequency and magnitude of heatwaves across the state of Rio de Janeiro and its municipalities between 1940 and 2024, using daily maximum temperature (Tmax) data from the ERA5 reanalysis. The study applies the methodology proposed by João L. Geirinhas et al. (2021), which identifies heatwave events using a relative threshold, defined by consecutive days when Tmax exceeds a given percentile of the local Tmax climatology for that specific calendar day, calculated within a 15-day moving window.

The analysis considers different percentiles (80th, 90th, and 95th) and durations (3–4 days, 5–7 days, and >7 days). In addition, the study develops a Python library designed to detect heatwaves from daily temperature data and quantify temporal changes in their frequency and magnitude, both for the entire state of Rio de Janeiro and each of its municipalities.

Finally, this research seeks to answer the following questions:

1. How do heatwaves vary spatially across the state of Rio de Janeiro?
2.	How has the frequency of heatwaves changed between 1940–1960 and 1994–2024 across the state’s municipalities?
3.	What are the differences in the temporal trends of heatwaves among the city of Rio de Janeiro (the capital), Petrópolis (a high-altitude municipality), and the state as a whole?

**References:**

AP News. 2023, ‘Taylor Swift’s Brazil tour marred by deaths and a dangerous heat wave’, viewed August 13, 2024, <https:// apnews.com/article/taylor-swift-concert-brazil-rio-eras-tour713f3e0051d60c4f280f1f3b242b1569>.

Bitencourt, D.P., Fuentes, M.V., Maia, P.A., Amorim, F.T., 2016. Frequência, duração, abrangência espacial e intensidade das ondas de calor no Brasil. Rev. Bras. Meteorol. 31, 506–517. https://doi.org/10.1590/0102-778631231420150077.

Câmara, F.P.; Gomes, A.F.; Dos Santos, G.T.; Câmara, D.C.P. Clima e Epidemias de Dengue No Estado Do Rio de Janeiro. Rev. Soc. Bras. Med. Trop. 2009, 42, 137–140.

Ceccherini, G., Russo, S., Ameztoy, I., Patricia Romero, C., Carmona-Moreno, C., 2016. Magnitude and frequency of heat and cold waves in recent decades: the case of South America. Nat. Hazards Earth Syst. Sci. 16, 821–831. https://doi.org/10.5194/nhess16-821-2016.

Cerne, S.B., Vera, C.S., 2011. Influence of the intraseasonal variability on heat waves in subtropical South America. Clim. Dyn. 36, 2265–2277. https://doi.org/10.1007/ s00382-010-0812-4.

Coelho, C.A.S., de Oliveira, C.P., Ambrizzi, T., Reboita, M.S., Carpenedo, C.B., Campos, J.L.P.S., Tomaziello, A.C.N., Pampuch, L.A., Custódio, M. de S., Dutra, L.M.M., Da Rocha, R.P., Rehbein, A., 2016. The 2014 southeast Brazil austral summer drought: regional scale mechanisms and teleconnections. Clim. Dyn. 46, 3737–3752. https://doi.org/ 10.1007/s00382-015-2800-1.

Dereczynski, C., Luiz-Silva, W., Bazzanela, A. C., Bodstein, A., & Chou, S. C. (2024). Case Study of an Extreme Heat Wave in Rio de Janeiro on November 2023: Synoptic Conditions and Climatological Trends. Anuário do Instituto de Geociências, 47, 66182.

Ebi, K.L.; Capon, A.; Berry, P.; Broderick, C.; de Dear, R.; Havenith, G.; Honda, Y.; Kovats, R.S.; Ma, W.; Malik, A.; et al. Hot Weather and Heat Extremes: Health Risks. Lancet 2021, 398, 698–708.

Geirinhas, J. L., Russo, A., Libonati, R., Sousa, P. M., Miralles, D. G., & Trigo, R. M. (2021). Recent increasing frequency of compound summer drought and heatwaves in Southeast Brazil. Environmental Research Letters, 16(3), 034036. https://doi.org/10.1088/1748-9326/abe0eb.

Geirinhas, J. L., Trigo, R. M., Libonati, R., Castro, L. C., Sousa, P. M., Coelho, C. A., ... & Magalhaes, M. D. A. F. (2019). Characterizing the atmospheric conditions during the 2010 heatwave in Rio de Janeiro marked by excessive mortality rates. Science of the Total Environment, 650, 796-808.

Geirinhas, J.L., Trigo, R.M., Libonati, R., Coelho, C.A.S., Palmeira, A.C., 2017. Climatic and synoptic characterization of heat waves in Brazil. Int. J. Climatol. 38, 1760–1776. https://doi.org/10.1002/joc.5294.

Hannart, A., Vera, C., Otto, F.E.L., Cerne, B., 2015. Causal influence of anthropogenic forcings on the Argentinian heat wave of December 2013. Bull. Am. Meteorol. Soc. https://doi.org/10.1175/BAMS-D-15-00137.1.

Herring, S.C., Hoerling, M.P., Kossin, J.P., Peterson, T.C., Stott, P.A., 2015. Explaining extreme events of 2014 from a climate perspective. Bull. Am. Meteorol. Soc. 96 (12), S1–S172. https://doi.org/10.1175/BAMS-ExplainingExtremeEvents2014.1.

IPCC, 2021: Summary for Policymakers. In: Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change [Masson-Delmotte, V., P. Zhai, A. Pirani, S.L. Connors, C. Péan, S. Berger, N. Caud, Y. Chen, L. Goldfarb, M.I. Gomis, M. Huang, K. Leitzell, E. Lonnoy, J.B.R. Matthews, T.K. Maycock, T. Waterfield, O. Yelekçi, R. Yu, and B. Zhou (eds.)]. Cambridge University Press, Cambridge, United Kingdom and New York, NY, USA, pp. 3−32, DOI: 10.1017/9781009157896.001. Karl, T.R., Nicholls, N. & Ghazi, A. 1999, ‘CLIVAR/GCOS/WMO workshop on indices and indicators for climate extremes: Workshop summary’, Weather and Climate Extremes, vol. 42, pp. 3-7, DOI: 10.1007/978-94-015-9265-9_2.

Luiz-Silva, W. & Dereczynski, C.P. 2014,  ́Climatological Characterization and Observed Trends in Climatic Extremes in the State of Rio de Janeiro ́, Anuário do Instituto de Geociências, vol. 37, no. 2, pp. 123-138, https://revistas. ufrj.br/index.php/aigeo/article/view/7828.

Marengo, J.A. & Nobre, C.A. 2024.  ́Secas e cheias mais que dobraram no Brasil entre 2014 e 2023 ́, viewed 17 August 2024, <https://amda.org.br/opiniao/secas-e-cheias-mais-quedobraram-no-brasil-entre-2014-e-2023/#:~:text=Foram%20 406%20epis%C3%B3dios%20de%20secas>.

Marengo, J.A.; Camargo, C.C. Surface Air Temperature Trends in Southern Brazil for 1960–2002. Int. J. Climatol. 2008, 28, 893–904. 

Monteiro dos Santos, D., Libonati, R., Garcia, B.N., Geirinhas, J.L., Salvi, B.B, Lima e Silva, E., Rodrigues, J.A., Peres, L.F., Russo, A., Gracie, R., Gurgel, H. & Trigo, R.M. 2024,  ́Twentyfirst-century demographic and social inequalities of heat-related deaths in Brazilian urban areas ́, PLoS ONE, vol. 19, no. 1, e0295766, DOI: 10.1371/journal.pone.0295766.

Moreira, A. B., Wanderley, L. S. D. A., Duarte, C. C., & Matzarakis, A. (2024). Atmospheric Conditions Related to Extreme Heat and Human Comfort in the City of Rio de Janeiro (Brazil) during the First Quarter of the Year 2024. Atmosphere, 15(8), 973.

NOAA. (2018). National Centers for Environmental Information, State of the Climate: Global Climate Report for Annual 2017. https://www.ncdc.noaa.gov/sotc/global/201713.

Perkins-Kirkpatrick, S. E., & Lewis, S. C. (2020). Increasing trends in regional heatwaves. Nature communications, 11(1), 3357.
Prosdocimi, D.; Klima, K. Health Effects of Heat Vulnerability in Rio de Janeiro: A Validation Model for Policy Applications. SN Appl. Sci. 2020, 2, 1948.

Renom, M., Rusticucci, M., Barreiro, M., 2011. Multidecadal changes in the relationship between extreme temperature events in Uruguay and the general atmospheric circulation. Clim. Dyn. 37, 2471–2480. https://doi.org/10.1007/s00382-010-0986-9.

Rodrigues, J.A., Libonati, R., Peres, L., Setzer, A., 2018. Mapeamento de áreas queimadas em Unidades de Conservação da região serrana do Rio de Janeiro utilizando o satélite Landsat-8 durante a seca de 2014. Anuário do IGEO 41, 318–327. http://dx.doi.org/ 10.11137/2018_1_318_327.

Rusticucci, M., 2012. Observed and simulated variability of extreme temperature events over South America. Atmos. Res. 106, 1–17. https://doi.org/10.1016/j. atmosres.2011.11.001.

Rusticucci, M., Barrucand, M., Collazo, S., 2017. Temperature extremes in the Argentina central region and their monthly relationship with the mean circulation and ENSO phases. Int. J. Climatol. 37, 3003–3017. https://doi.org/10.1002/joc.4895.

Seneviratne, S.I., Zhang, X., Adnan, M., Badi, W., Dereczynski, C. et al. 2021, ‘Weather and climate extreme events in a changing climate’. In Climate Change, 2021: The physical science basis. contribution of working group I to the sixth assessment report of the intergovernmental panel on climate change [MassonDelmotte V, Zhai P, Pirani A, Connors SL, Pean C, Berger S, Caud N, Chen Y, Goldfarb L, Gomis MI, Huang M, Leitzell K, Lonnoy E, Matthews JBR, Maycock TK, Waterfield T, Yelekci O, Yu R, and Zhou B (eds.)]. Cambridge University Press, Cambridge, United Kingdom and New York, NY, USA, pp 1513–1766. Weather and Climate Extreme Events in a Changing Climate (Chapter 11) – Climate Change 2021 – The Physical Science Basis (cambridge.org). <https://www.cambridge.org/ core/books/climate-change-2021-the-physical-science-basis/ weather-and-climate-extreme-events-in-a-changing-climate/ 5BCB24C5699F1D42B2DE379BDD4E2119>.

World Meteorological Organization. Provisional State of the Global Climate 2023; WMO: Geneva, Switzerland, 2023; Volume 6. Available online: https://www.un.org/en/climatechange/reports?gad_source=1&gclid=CjwKCAjwnqK1BhBvEiwAi7o0X9 ZVol0FF6yR9j-vtXsOt6yqLzD0qUczYnXSLsacS-SIamAkDTjwIhoCrl8QAvD_Bw.

---

## 2. Project Overview

The main goal of this project is to **analyze the temporal trends and spatial variability of heatwaves across the state of Rio de Janeiro**. To achieve this, we will develop a **Python Small library** capable of automatically detecting heatwave events from daily maximum temperature (Tmax) data and quantifying their frequency and magnitude over time.The function will operate at two spatial scales:

(1) **State-level**, to identify large-scale temporal trends and long-term variability;

(2) **Municipality-level** , to assess how the intensity and frequency of heatwaves differ across the heterogeneous territory of Rio de Janeiro.

Datasets:

- Gridded data (Reanalysis): ERA5 – Tmax (daily data) – Period: 1940–2024 

- Shapefile of the areas (State of Rio de Janeiro and municipalities) – Source: IBGE (Brazilian Institute of Geography and Statistics) 

The final outputs will include:

- **Organized tables (CSV and GeoJSON formats)** summarizing heatwave characteristics—frequency, duration, and magnitude—computed for multiple percentile thresholds (80th, 90th, and 95th) and duration ranges (3–4 days, 5–7 days, and >7 days).

- **Spatial maps illustrating the geographical** distribution of heatwave frequency and intensity across the state of Rio de Janeiro and its municipalities, under different percentile thresholds.

- **Comparative graphs showing temporal** trends across municipalities and between selected case studies (e.g., Rio de Janeiro, Petrópolis, and the state average), highlighting how results vary according to the chosen thresholds and event durations 

**References:**

Hersbach, H. et al. (2020). The ERA5 global reanalysis. Q. J. R. Meteorol. Soc., 146, 1999–2049.  

Instituto Brasileiro de Geografia e Estatística (IBGE, 2024). Malha Municipal do Brasil: edição 2024.

---

## 3. Advanced Topic

The project will incorporate **parallelization** to efficiently handle large datasets, particularly during spatial analyses that calculate heatwave metrics across multiple municipalities simultaneously. This approach aims to significantly reduce runtime and improve scalability when processing long time series. If time permits, a brief performance comparison between serial and parallel implementations will be conducted to evaluate computational efficiency gains.

---

## 4. Project Timeline

The following timeline outlines the planned stages for completing the project. Each task can be marked as complete in GitHub using Markdown checkboxes.

## Project Timeline

- [ ] (Nov 10) Download temperature data (ERA5) and shapefiles (IBGE)
- [ ] (Nov 10) Develop the data extraction code for the shapefile
- [ ] (Nov 17) Implement the heatwave detection code
- [ ] (Nov 24) Integrate all components into a Python library
- [ ] (Nov 24) Apply parallelization to the data extraction module
- [ ] (Dec 01) Conduct trend analyses and create notebooks (Generate plots)

---

## 5. Mockup of the Main Figure

The final figure will combine spatial and temporal visualizations to illustrate the distribution and evolution of heatwaves across Rio de Janeiro.

- A time series plot will display the number of heatwave events for three selected regions — the city of Rio de Janeiro, the state of Rio de Janeiro (aggregate), and Petrópolis (a high-altitude municipality) — within the same graph, allowing for direct comparison of temporal trends.

- Spatial maps will show the average number of heatwaves per municipality, computed for two distinct 30-year periods (e.g., 1940–1970 and 1994–2024), enabling the visualization of long-term changes.

- Each map will be generated for different percentile thresholds (80th, 90th, and 95th) to highlight how heatwave frequency and spatial distribution vary depending on the threshold used.

- All visualizations will employ a continuous color scale (e.g., matplotlib colormap YlOrRd) to represent heatwave intensity and will be produced using matplotlib and seaborn for consistency and high-quality outputs.
 


