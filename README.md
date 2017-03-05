Web Service (only API links available at the moment): https://oorjan-sv.herokuapp.com

Created a service that measures performance of solar systems against reference/estimated performance, and sends daily alerts highlighting hours of the day when actual solar power (DC, in watts) was less than 80% of reference/estimated solar power (DC, in watts).

Technologies: Python 2.7 with Django Framework, REST API (Web), PostgreSQL (Database), Heroku (Deployment)


API end points:

*	Setup Reference Data either by admin interface OR using Postman / cURL:

> curl -D - -X POST https://oorjan-sv.herokuapp.com/solarsys/api/postreference/ -d 'lat=19&long=73&system_capacity=4'
(DC Output - 8760 data points, will be automatically fetched from NREL API and stored in a JSONField in the same table/row as its Ref Installation Metadata – Lat/Lon/SC)


*	Setup Installation Key either by admin interface OR using Postman / cURL:

> curl -D - -X POST https://oorjan-sv.herokuapp.com/solarsys/api/postinstallationkey/ -d 'lat=19&long=73&sc=10'


*	Store LiveDC with installation key using Postman / cURL OR command (simulatelivedc.py):

> curl -D - -X POST https://oorjan-sv.herokuapp.com/solarsys/api/livedc/ -d 'installationkey=c97bc848-047a-4940-957d-b70cfd9be1ba&date=2017-03-03'

OR

> python simulatelivedc c97bc848-047a-4940-957d-b70cfd9be1ba 2017-03-03


*	Get Performance of Live DC (compared to nearest Ref DC) using Postman / cURL OR command (dailyReport.py):

> https://oorjan-sv.herokuapp.com/solarsys/api/performance/?installationkey=1c51c1ad-734a-4fb2-996f-b1b423092e2e&date=05-03-2017 

OR

> python manage.py dailyReport 05-03-2017 1c51c1ad-734a-4fb2-996f-b1b423092e2e

(python manage.py dailyReport -date> -installation_key : Setup on Heroku Scheduler for 8.00 PM to be sent to settings.EMAIL_TO)



Other API end points:

* Get Live DC for installation key and date:

https://oorjan-sv.herokuapp.com/solarsys/api/getlivedc/?installationkey=722066cc-50a7-47d1-9bb5-04e287d6033c&date=2017-03-01

* Get Reference Data based on SC and approx. lat/long (from database):

https://oorjan-sv.herokuapp.com/solarsys/api/getreference/?lat=28.1&long=77.1&sc=3&date=04-03-2017


NOTE: Please use cURL/Postman (or a script, if specified) for API calls. Links may not work on browsers as the content type is x-www-form-urlencoded.
Also refer to Design-Docs folder for more information.
