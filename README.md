Link: https://oorjan-sv.herokuapp.com

Created a service that measures performance of solar systems against reference/estimated performance, and sends daily alerts highlighting hours of the day when actual solar power (DC, in watts) was less than 80% of reference/estimated solar power (DC, in watts).

Technologies: Python 2.7 with Django Framework, PostgreSQL (Database), HTML (Web), Heroku (Deployment)

Sample reference data: Hourly DC solar power (in watts), key “dc”, which includes 365*24=8760 data points is the reference/estimated data.
* API endpoint with sample parameters: https://developer.nrel.gov/api/pvwatts/v5.json?api_key=DEMO_KEY&lat=19&lon=73&system_capacity=4&azimuth=180&tilt=19&array_type=1&module_type=1&losses=10&dataset=IN&timeframe=hourly 


DB Tables: 
* solarsys_reference (Model- Reference): Reference Metadata (Inputs) and DC values (Outputs['DC']) for 8760 data points, using jsonfield (key=Day of Year, values=DC power values of 24 hours for each day) - Data load through Admin page
* solarsys_installationkey (Model- InstallationKey): Auto-generated Installation Key (UUID) with correspoonding 'lat','long','system_capacity' values
* solarsys_livedc (Model- LiveDC): DC Power records simulated per hour for each installation key, inserted here

Scripts:
* simDCLive.py (/solarsys/management/commands): Hourly script that simulates DC Power for each installation key (scheduled using Heroku Scheduler)
* dailyReport.py (/solarsys/management/commands): Daily script that compares Live DC Power values of the day with Reference DC Power values, based on nearest lat/long, and same SC/timestamp (Date+Hour), and sends an email alert at 8PM, consisting of those Live DC values which are less than 80% of Ref Dc values

Web Pages (/solarsys/templates/solarsys):
* reference_data.html (View- reference_data): lists all the Reference DC values for the day
* live_data.html (View- live_data): lists all the Live DC values for the day
* performance_report.html (View- performance_report): list of flagged Live DC values (<80% of DC) for the day along with its corresponding DC values and installation key
* 2 API links (pending)

Other:
* Logic and functions (/solarsys/utilities.py)
* Basic tests (/solarsys/views.py)
* App URLs (/solarsys/urls.py)

Ongoing/Pending Tasks:
* API link provision
* Additional test cases for data validation, email and error logs
* Improvement in front end
