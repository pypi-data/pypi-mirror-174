# datameteo: herramienta para el análisis de datos meterológicos

<p dir="auto">
 <a href="https://pypi.org/project/pandas/" rel="nofollow"><img src="https://camo.githubusercontent.com/74cb3c88c43d4266705ae6ec7fddc1bbf603eb6d15bf2202ceb3416cd26b7c0d/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f70616e6461732e737667" alt="PyPI Latest Release" data-canonical-src="https://img.shields.io/pypi/v/pandas.svg" style="max-width: 100%;"></a>
 <a href="https://pypi.org/project/pandas/" rel="nofollow"><img src="https://camo.githubusercontent.com/caf1bfd611737461f1d62e150d6753e05602727131be954051dd3a41dc901101/68747470733a2f2f696d672e736869656c64732e696f2f707970692f7374617475732f70616e6461732e737667" alt="Package Status" data-canonical-src="https://img.shields.io/pypi/status/pandas.svg" style="max-width: 100%;"></a>
 <img src="https://readthedocs.org/projects/datameteo/badge/?version=latest" />
 <a href="https://datameteo.readthedocs.io/en/latest/?badge=latest" style="text-decoration: none;" onclick="$('#badge_markup').toggle(); return false;">
 <span class="badge-info" title="Get this badge"></span>
 </a>
 <div id="badge_markup" class="badge" style="display: none;"></p>
      
## ¿Qué es?
datameteo es un paquete de Python que proporciona el acceso a datos meteorológicos para que el análisis de estos sea más rápido y sencillo. Después de definir cualquier ubicación, descarga datos metereológicos de temperatura, humedad, viento, precipitación y estado del cielo de las últimas 48 horas. Ofrece la posibilidad de mostrar los datos por pantalla como texto o por visualizaciones generando imágenes.     


## Principales características
La librería puede hacer las siguientes cosas:
* Muestra coordenadas de latitud y longitud de la ubicación introducida a través de Nominatim.
* Descarga de los datos en formato json.
* Temperatura de las últimas 48 horas en ºC.
* Humedad de las últimas 48 horas en g/m3.
* Rachas de viento de las últimas 48 horas en m/s.
* Precipitación de los últimos 48 minutos en l/m2.
* Tipos de estados de cielo.
* Posibilidad de mostrar gráficamnete los datos descargados mediante descriptivos numéricos, boxplots, gráficos de líneas y barras.

## Dónde conseguirlo
El código fuente está actualmente alojado en GitHub en: https://github.com/Leirebarturen/datameteo.
Los instaladores para la última versión publicada están disponibles en Python Package Index (PyPI).
<div class="highlight highlight-source-shell notranslate position-relative overflow-auto" dir="auto" data-snippet-clipboard-copy-content="# PyPI
pip install datameteo"><pre><span class="pl-c"><span class="pl-c">#</span> PyPI</span>
pip install datameteo</pre></div>
Comando para actualizar el paquete.
<div class="highlight highlight-source-shell notranslate position-relative overflow-auto" dir="auto" data-snippet-clipboard-copy-content="# PyPI
pip install datameteo --upgrade"><pre><span class="pl-c"><span class="pl-c">#</span> PyPI</span>
pip install datameteo --upgrade</pre></div>

## Dependencias
<li><a href="https://pypi.org/project/requests/" rel="nofollow">requests - Realiza la petición de los datos a la API.</a></li>
<li><a href="https://geopy.readthedocs.io/en/stable/" rel="nofollow">geopy - Ofrece as coordenadas de la ubicación introducida a través de la API Nominatim.</a></li>
<li><a href="https://pypi.org/project/pandas/" rel="nofollow">pandas - Ofrece soporte y funciones para realizar descriptivos numéricos de los datos.</a></li>
<li><a href="https://matplotlib.org/" rel="nofollow">matplotlib - Ofrece funciones para realizar gráficos de lineas de los datos.</a></li>
<li><a href="https://seaborn.pydata.org/" rel="nofollow">seaborn - Ofrece funciones para realizar gráficos de líneas y barras de los datos.</a></li>

## Documentación
La documentación oficial está alojada en PyData.org: https://datameteo.readthedocs.io/en/latest/
