# datascience_project4
Repository for Udacity's Data Scientist Nanodegree - Capstone Project

- - - -
![alt text](https://github.com/Andrea-Schulz/datascience_project4/blob/master/icons/Logo.jpg?raw=true)
- - - -

### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

- - - -
## Installation <a name="installation"></a>

* Python 3.6.x
* Jupyter Notebook - as a useful tool to improve readability of the Jupyter Notebooks I recommend the [Unofficial Jupyter Extensions](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/index.html)

## Project Motivation<a name="motivation"></a>

...becoming a Data Scientist, duh.

For the Data Scientist Capstone Project, I set out to explore a current topic - the development of the Coronavirus pandemic in Germany in 2020.

The core issue I wanted to tackle was to look beyond the content of popular dashboards and **estimate the number of undetected cases, that is "dark figures", throughout the the year**. This required a thorough analysis of the dynamics of the pandemic first, and hence I focused on two leading questions:

* How did Coronavirus infections spread across the country and what were the affected groups?
* Based on this, how can we estimate “dark figures”, that is, undetected Coronavirus infections?

In order to validate the approach taken for the estimation, I analyzed socio-demographic aspects of the spreading of the virus as well as the reliability of the data in terms of documented breakouts and testing/reporting statistics.

## File Descriptions <a name="files"></a>

This repository contains a Notebook `COVID19_Analysis.ipynb` with the commented analysis itself, including the estimation of dark figures. 

The `data_preprocess.py` and `plot_functions.py` modules contain custom functions for data preprocessing and visualizations.

To complete the project, the following publicly available data was used:
* official data on the Coronavirus pandemic by the German federal government agency and research institute responsible for disease control and prevention Robert Koch Institute or RKI ([link](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/nCoV_node.html))
* official data derived from German Federal Statistics Office (used by RKI) on:
	* German population per federal state ([link](https://de.statista.com/statistik/daten/studie/71085/umfrage/verteilung-der-einwohnerzahl-nach-bundeslaendern/))
	* German population per age group ([link](https://www-genesis.destatis.de/genesis/online?operation=abruftabelleBearbeiten&levelindex=1&levelid=1611959825818&auswahloperation=abruftabelleAuspraegungAuswaehlen&auswahlverzeichnis=ordnungsstruktur&auswahlziel=werteabruf&code=12411-0005&auswahltext=&werteabruf=Werteabruf#abreadcrumb)) or ([link](https://service.destatis.de/bevoelkerungspyramide/index.html#!))
* data derived for dark figures calculation:
	* Study "Social Contacts and Mixing Patterns Relevant to the Spread of Infectious Diseases" by Mossong et.al. ([link](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0050074))

## Results<a name="results"></a>

The global pandemic was, and still is, an overwhelming experience to which we had to adapt to in many ways. Analyzing such a novel disease poses some major challenges to making any estimations.
* systematic reporting and collection of data was implemented over the course of the pandemic. The documentation of breakouts, test rates and other information put into question the reliability and completeness of (some of) the given given data.
* the limited amount of data is further distorted by alternating phases with low case numbers and specific breakouts on the one hand and exponentially growing infections in diffuse locations on the other.
* unprecedented political and economic measures taken to prevent a spread of infections make many assumptions or estimations hard to validate.
* given the novelty of the disease, there are a lot of uncertainties in general, including the prevalence of symptoms, mechanisms of transmission, death rates etc.

Due to this, I will not give away numbers without context here, and spare you the detailed discussion. You'll find the full analysis and discussion in this [blog post](https://andrea-s-schulz.medium.com/covid-19-beyond-the-dashboards-d3b503e7c360).

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

Shout out to:
* Robert Koch Institute RKI for providing detailed [resources](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Steckbrief.html;jsessionid=778741D021B29A2808C6D24EAF79A2DC.internet052?nn=13490888) and [data](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/nCoV_node.html) on the novel Coronavirus
* [Fraunhofer ITWM](https://www.itwm.fraunhofer.de/de/abteilungen/mf/aktuelles/blog-streuspanne/corona-dunkelziffer.html) and [DunkezifferRadar](https://covid19.dunkelzifferradar.de/) for their research on estimating undetected Coronavirus cases 
* Github for their official [Markdown Cheat Sheet](https://gtribello.github.io/mathNET/assets/notebook-writing.html)
