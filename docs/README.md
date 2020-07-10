<script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>
<script src="{{ base.url | prepend: site.url }}/covid-19/assets/js/plotly.min.js"></script>
## COVID-19 Data Analysis

The intent of this project is to share rudimentary snippets to analyze and visualize COVID-19 data shared through COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.

### Global Confirmed Cases and Deaths
  {% include metrics.html %}
  {% include confirmed-deaths-world.html %}

### Global Confirmed Cases over Time
  {% include cases-confirmed-global.html %}

### Global Confirmed Cases Per 100,000 of population
  {% include cases-std_confirmed-global.html %}

### Confirmed Cases by Continent
  {% include confirmed-continents.html %}

### Comparison of COVID-19 metrics for 10 most populous countries
    {% include cases-populous-standardized.html %}
