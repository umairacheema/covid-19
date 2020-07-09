<script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>
<script src="{{ base.url | prepend: site.url }}/covid-19/assets/js/plotly.min.js"></script>
## COVID-19 Data Analysis
{% site.data.common.date %}
The intent of this project is to share rudimentary snippets to analyze and visualize COVID-19 data shared through COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.

### Confirmed Cases and Deaths (Aggregated)


  {% include confirmed-deaths-world.html %}

### Confirmed Cases by Continent

  {% include confirmed-continents.html %}
