# Using catalog csv files to map your data to Dash callbacks:
## 4 columns
- **title**: name that you want to appear in references on dash page
- **filename**: source file, can leave blank if you code an exception into aggregate() in utilities.py
- **titlevar**: column of your var within the source file, can leave blank if you code an exception into aggregate() in utilities.py
- **locvar**: name of the column in the sourcefile that maps to your geofile
  - in my example files, I use "PrecinctKey", which is the county-precinct numbering convention followed in the geojson data for TX31. Precincts in Bell county are '270[precinct#]' and precincts in Williamson county are '4910[precinct#]'. In our case this was necessary because there are some duplicate precinct numbers across both counties.
  - Be sure your locvar maps exactly to whatever you've assigned geovar to be in utilities.py.
  - e.g. Say a data point for Bell County precinct 113 is located in the source file in the row where 'PrecinctKey' [locvar] is 270113. Then, the geojson shape data for that precinct will be located in the geojson file in the row where 'PCTKEY' [geovar] is also 270113.
