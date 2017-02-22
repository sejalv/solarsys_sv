"# oorjan_sv" 
Link: https://oorjan-sv.herokuapp.com

Created a service that measures performance of solar systems against reference/estimated performance, and sends daily alerts highlighting hours of the day when actual solar power (DC, in watts) was less than 80% of reference/estimated solar power (DC, in watts).

Technologies: Python 2.7 with Django Framework, PostgreSQL (Database), HTML (Web), Heroku (Deployment)

Sample reference data: Hourly DC solar power (in watts), key “dc”, which includes 365*24=8760 data points is the reference/estimated data.
URL: https://developer.nrel.gov/api/pvwatts/v5.json?api_key=DEMO_KEY&lat=19&lon=73&system_capacity=4&azimuth=180&tilt=19&array_type=1&module_type=1&losses=10&dataset=IN&timeframe=hourly 
Path: /Data/oorjan_ref.json

DB Tables: 
* solarsys_solarreference (Model- SolarReference): Entire reference data, using jsonfield
* solarsys_referencedc (Model- ReferenceDC): Outputs['DC'] of reference data for 8760 data points, using jsonfield (keys=24 hours, values=365 days for each hour)
* solarsys_installationkey (Model- InstallationKey): Inputs['lat','long','system_capacity'] of referencce data (1 record), and 3 additional records (simulated)
* solarsys_livedcdump (Model- LiveDCDump): DC Power records simulated per hour for each installation key, inserted here

Scripts :
* simLive.py (/solarsys/management/commands): Hourly script that simulates DC Power for each installation key (scheduled using Heroku Scheduler)
* dailyReport.py (/solarsys/management/commands): Daily script that compares Live DC Power values of the day with Reference DC Power values, across same installation key and timestamp (Date+Hour), and sends an email alert at 8PM, consisting of those Live DC values which are less than 80% of Ref Dc values
* simLive_prev.py (/solarsys/management/commands): Batch script to simulate Live DC Power records for previous days
* load_references.py: Batch script to load Reference Data - Metadata/Installation Key, DC output (8760 data points)

Web Pages (/solarsys/templates/solarsys):
* reference_data.html (View- reference_data): lists all the Reference DC values for the day
* live_data.html (View- live_data): lists all the Live DC values for the day
* performance_report.html (View- performance_report): list of flagged Live DC values (<80% of DC) for the day along with its corresponding DC values and installation key

Ongoing/Pending Tasks:
* Dynamic report generation for performance measurement (eg. based on any date)
* Additional test cases for data validation, email and error logs
* Improvement in views, web app
