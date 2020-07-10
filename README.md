## COVID-19 Data Analysis

The intent of this project is to share simple python scripts to visualize COVID-19 data shared through COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.The [data respository](https://github.com/CSSEGISandData/COVID-19) is updated by CSSE of Johns Hopkins University using public data sources on daily basis. 

There are two main python scripts.
- covid19_data.py
- covid19_plots.py

In order to generate the plots following steps should be followed after installing pre-requisites.

1. Clone this repository
```
git clone https://github.com/umairacheema/covid-19
```
2. Clone John Hopkins University Data Repositorty
```
git clone https://github.com/CSSEGISandData/COVID-19
```
3. Copy timeseries data folder from John Hopkins repository
```
cd covid-19
cp -R ../COVID-19/csse_covid_19_data .
```
4. Run data preprocessing script
```
python covid19_data.py
```
5. Run visualization generation script
```
python covid19_plot.py
```

The plots will be generated under docs/interactive-plots directory.

Live Demo is available at [COVID-19](https://umairacheema.github.io/covid-19).

## Prerequisites
- Anaconda
- Plotly
- pycountry-convert

## License
The scripts are licensed under GNU General Public License v3.0
