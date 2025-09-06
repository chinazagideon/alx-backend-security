# Django IP Tracking and Security Suite
<p>This project is a Django application designed to enhance web application security by tracking IP addresses, managing IP blacklists, and performing analytics and anomaly detection. It provides a robust, layered defense against malicious traffic and bot activity.</p>

## Features
#### IP Logging: A custom middleware logs every request's IP address, path, and timestamp for analysis.

### IP Blacklisting: 
<p>A Django management command and middleware work together to block specific IP addresses from accessing the site.</p>

### Geolocation Analytics: 
<p>The app uses the ipinfo_django library to enrich logged IP data with country and city information. The data is cached for 24 hours to ensure high performance.</p>

### Rate Limiting: 
<p>The django-ratelimit package is used to restrict the number of requests per minute, preventing brute-force attacks and abuse of sensitive views like login pages.</p>

### Anomaly Detection: 
<p>An hourly Celery task analyzes request logs to automatically flag and store suspicious IPs that either exceed a request threshold or attempt to access sensitive paths like /admin or /login.</p>

## Models
<p>The project uses several key models to store and manage security data.</p>

##### RequestLog: Stores detailed information about each incoming request, including IP address, path, and timestamp. It also includes fields for geolocation data.

##### BlockedIP: A simple model used to store IP addresses that have been manually blacklisted.

##### SuspiciousIP: A model that stores IP addresses flagged by the anomaly detection system, along with a reason for the flagging.

## Implementation Details
##### Task 1: IP Blacklisting
###### This feature is composed of a middleware that checks every incoming request against the BlockedIP model. It also includes a management command for easily adding new IPs to the blacklist from the command line.

##### Task 2: IP Geolocation Analytics
###### The ipinfo_django package is used to add geolocation data to each request log. The middleware retrieves this data and stores it in the RequestLog model, with the package automatically handling the 24-hour caching to optimize performance and prevent excessive API calls.

##### Task 3: Rate Limiting
###### The @ratelimit decorator from the django-ratelimit package is applied to views to control request frequency. A custom function distinguishes between authenticated and anonymous users, applying different limits to each group to prevent abuse while still allowing legitimate users to operate freely.

##### Task 4: Anomaly Detection
###### This is a Celery-powered feature. A scheduled task runs hourly to analyze the RequestLog table, identifying IPs that meet specific criteria for suspicious behavior (e.g., high request count, access to sensitive paths) and saving them to the SuspiciousIP model.
