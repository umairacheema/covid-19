<script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>
<script src="{{ base.url | prepend: site.url }}/covid-19/assets/js/plotly.min.js"></script>
## COVID-19 Data Analysis

The intent of this project is to share simple python scripts to visualize COVID-19 data shared through COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.

**All visualizations including maps are interactive.**

### Global Confirmed Cases and Deaths
  {% include metrics.html %}
  {% include confirmed-deaths-global.html %}
  [Full Screen](https://umairacheema.github.io/covid-19/interactive-plots/confirmed-deaths-global.html)
### Global Confirmed Cases over Time
  {% include cases-confirmed-global.html %}
  [Full Screen](https://umairacheema.github.io/covid-19/interactive-plots/cases-confirmed-global.html)
### Global Confirmed Cases Per 100,000 of population
  {% include cases-std_confirmed-global.html %}
  [Full Screen](https://umairacheema.github.io/covid-19/interactive-plots/cases-std_confirmed-global.html)
### Confirmed Cases by Continent
  {% include confirmed-continents.html %}
  [Full Screen](https://umairacheema.github.io/covid-19/interactive-plots/confirmed-continents.html)
### Comparison of COVID-19 metrics for 10 most populous countries
 __Circle size represents number of deaths per 100 Thousand persons__ 
  {% include cases-populous-standardized.html %}
  [Full Screen](https://umairacheema.github.io/covid-19/interactive-plots/cases-populous-standardized.html)
### Global Confirmed Cases, Recovered Cases and deaths (Latest)
  {% include cases-today-global.html %}
  [Full Screen](https://umairacheema.github.io/covid-19/interactive-plots/cases-today-global.html)
