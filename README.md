# Web Dashboard

### Notes
For PyCharm, mark /dashboard_app as sources root. Right click the folder | Mark directory as
Requirements.txt generated with> pipreqs --force
```
# docker build -t $DOCKER_ACC/$DOCKER_REPO:$IMG_TAG .
docker build -t paulmz/dashboard:alpha .
docker push paulmz/dashboard
docker run -it -p 8080:8080 --rm --name dashboard-app paulmz/dashboard:alpha
```

### References
https://datatables.net/  
https://github.com/datasets/covid-19/blob/master/data/countries-aggregated.csv  
https://github.com/datasets/population/blob/master/data/population.csv  
https://datatables.net/forums/discussion/22482/howto-save-row-selection-and-highlighting-if-page-refresh  
https://stackoverflow.com/questions/39733422/sorting-se  
https://code.tutsplus.com/tutorials/charting-using-plotly-in-python--cms-30286  
https://www.osano.com/cookieconsent/download/  
