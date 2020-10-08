# Akamai Tools
This repo is a collection of various tools or utilities I have developed to help customers and Akamai employees to improve their daily work with Akamai CDN. Please feel free to download and explore them.

# Installation of Dependencies
```
$pip install -r requirements.txt
```


# Utility 1: Comparitive Testing: Response Comparision between Staging and Production Environments

When SA does the implementation of new behavior, modify existing behavior, or delete the behavior, SA first pushes to staging to test. Comparing the behavior between staging and production is a common task to see if the new version in staging is working as expected. Many times I copy the response in a text file from both environments and use comparison tools like Beyond Compare. It would be great if we can have a side by side comparison of responses between staging and production networks without having to do manual work.

## Usage

```
$python comparitive_testing.py 'http://achuth-autest.edgesuite.net/products.html' ff

+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|          Header           |                         Staging                         |                       Production                        |
+===========================+=========================================================+=========================================================+
|          Status           |                           200                           |                           200                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|       Content-Type        |                text/html; charset=UTF-8                 |                text/html; charset=UTF-8                 |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|          Server           |                 Apache/2.2.15 (CentOS)                  |                 Apache/2.2.15 (CentOS)                  |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|       Last-Modified       |              Tue, 15 Mar 2016 22:48:08 GMT              |              Tue, 15 Mar 2016 22:48:08 GMT              |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|           ETag            |                "12da-8d83-52e1e30e89a00"                |                "12da-8d83-52e1e30e89a00"                |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|     X-Check-Cacheable     |                           YES                           |                           YES                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|    X-Akamai-Request-ID    |                  4399aa.dd4e4b                   |                 14d29e8f.1ee0026                 |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|   X-Akamai-Transformed    |                   9 4639 0 pmb=mRUM,1                   |                   9 4639 0 pmb=mRUM,1                   |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|           Vary            |                     Accept-Encoding                     |                     Accept-Encoding                     |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|           Date            |          Fri, 21 Aug 2020 10:50:36 GMT           |          Fri, 21 Aug 2020 10:50:38 GMT           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|      Content-Length       |                      39224                       |                      39226                       |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|                           |                    TCP_MISS from                    |                    TCP_MISS from                    |
|          X-Cache          |       a23-50-54-14.deploy.akamaitechnologies.com        |       a2-21-242-215.deploy.akamaitechnologies.com       |
|                           |          (AkamaiGHost/10.1.2-30498069) (-)           |          (AkamaiGHost/10.1.2-30498069) (-)           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|                           | /L/16382/942749/1d/gsshappylearning.com/products.h  |             /L/16382/942749/1d/achuth-              |
|        X-Cache-Key        |              tml?%20&akamai-transform=9              |     autest.edgesuite.net/products.html?%20&akamai-      |
|                           |                                                         |                     transform=9                      |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|   X-Cache-Key-Extended-   | /L/16382/942749/1d/gsshappylearning.com/products.h  |             /L/16382/942749/1d/achuth-              |
|     Internal-Use-Only     |         tml?%20&akamai-transform=9 vcd=1456          |     autest.edgesuite.net/products.html?%20&akamai-      |
|                           |                                                         |                 transform=9 vcd=1456                 |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|  X-Akamai-Brotli-Status   |             client does not support brotli              |             client does not support brotli              |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|     X-True-Cache-Key      |      /L/gsshappylearning.com/products.html?%20      |  /L/achuth-autest.edgesuite.net/products.html?%20   |
|                           |                       vcd=1456                       |                       vcd=1456                       |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|      AKA_PM_BASEDIR       |                                                         |                                                         |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|  AKA_PM_CACHEABLE_OBJECT  |                          true                           |                          true                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|      AKA_PM_FWD_URL       |                   /products.html?%20                    |                   /products.html?%20                    |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|    AKA_PM_PREFETCH_ON     |                          true                           |                          true                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|   AKA_PM_PROPERTY_NAME    |                 achuth-akamaiuniversity                 |                 achuth-akamaiuniversity                 |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|  AKA_PM_PROPERTY_VERSION  |                        31                        |                        23                        |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|     AKA_PM_SR_ENABLED     |                          false                          |                          false                          |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|     AKA_PM_TD_ENABLED     |                          true                           |                          true                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|   AKA_PM_TD_MAP_PREFIX    |                           ch2                           |                           ch2                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|     ANS_PEARL_VERSION     |                         0.12.0                          |                         0.12.0                          |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
| FASTTCP_RENO_FALLBACK_DIS |                           on                            |                           on                            |
|        ABLE_OPTOUT        |                                                         |                                                         |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|   FOFR_PERF_CIP_BUCKET    |                          2283                           |                          2283                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|      FOFR_PERF_HASH       |                         228324                          |                         228324                          |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|   FOFR_PERF_TIME_BUCKET   |                           14                            |                           14                            |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
| G2C_RATE_LIMIT_HRS_MATCHE |                          FALSE                          |                          FALSE                          |
|             D             |                                                         |                                                         |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|      MPULSE_DEFAULT       |                          true                           |                          true                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
| OVERRIDE_HTTPS_IE_CACHE_B |                           all                           |                           all                           |
|            UST            |                                                         |                                                         |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|     PCH_SERIAL_PREFIX     |                            a                            |                            a                            |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|    PCH_SITE_SHIELD_MAP    |                     chws.akamai.net                     |                     chws.akamai.net                     |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|      TCP_OPT_APPLIED      |                           low                           |                           low                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|     Y_HATS_CIP_BUCKET     |                          9834                           |                          9834                           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|      Y_HATS_CIP_HASH      |                         983448                          |                         983448                          |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|    Y_HATS_TIME_BUCKET     |                           38                            |                           38                            |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|         X-Serial          |                          16382                          |                          16382                          |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|        Connection         |                       keep-alive                        |                       keep-alive                        |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|                           |                    TCP_MISS from                    |                    TCP_MISS from                    |
|      X-Cache-Remote       |       a23-50-58-47.deploy.akamaitechnologies.com        |      a23-11-206-150.deploy.akamaitechnologies.com       |
|                           |          (AkamaiGHost/10.1.2-30498069) (-)           |          (AkamaiGHost/10.1.2-30498069) (-)           |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
|       Server-Timing       |    cdn-cache; desc=MISS, edge; dur=226, origin;     |    cdn-cache; desc=MISS, edge; dur=109, origin;     |
|                           |                       dur=191                        |                       dur=192                        |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
| X-Akamai-Pragma-Client-IP |                80.67.65.11, 80.67.65.11                 |                80.67.65.11, 80.67.65.11                 |
+---------------------------+---------------------------------------------------------+---------------------------------------------------------+
--------------------------------------------------------------------------------------------------
Staging Headers for Logs:
X-Cache: TCP_MISS from a23-50-54-14.deploy.akamaitechnologies.com (AkamaiGHost/10.1.2-30498069) (-)
X-Akamai-Request-ID: 4399aa.dd4e4b
--------------------------------------------------------------------------------------------------
Production Headers for Logs:
X-Cache: TCP_MISS from a2-21-242-215.deploy.akamaitechnologies.com (AkamaiGHost/10.1.2-30498069) (-)
X-Akamai-Request-ID: 14d29e8f.1ee0026
--------------------------------------------------------------------------------------------------
```

# Utility 2: Hostname DNS Reviewer: Account wide mapping of Hostnames to its DNS Records.

As an account grows big, it also becomes very difficult to track the hostnames as well. It is very important to have a list of properties, hostnames, edge hostnames, and their corresponding CNAMEs to get a clear picture of hostnames and their status. This would be very useful if you are an aligned SA to know the health of the account. To get this data, I have developed a simple Python-based script that can be used to run it on any account.

## Usage
```
$python hostname-check.py
Enter Account Switch Key:<AccountID>
Fetching Hostname details and updating in file: <AccountID>.xlsx
................
Done
```


# Utility 3: Akamai Purge Validator
When we often purge a URL we know that the url is purged across Akamai Network. But often customers ask for validation.This script is aimed for that. This script reads a list of urls you want to purge from Akamai Staging or Production Network. For each of the url, the script requests the content by requesting more than once for the same content and ensures that it is cached in the Akamai Servers and then it purges the url and then re request the same edge server to see if the content is still cached.
You need to have permissions to purge the url. For that you need to create a CCU API client and give its credentials.

## Usage
```
$:python purge_validator.py delete staging urls.txt
http://www.dutchclothing.com.edgesuite-staging.net/images/img-sp.png
Retrying..
Retrying..
Cache-Status: TCP_HIT
Purging....
Cache-Status: TCP_MISS
Purged Successfully
-------------
http://www.dutchclothing.com.edgesuite-staging.net/images/5.jpg
Retrying..
Cache-Status: TCP_HIT
Purging....
Cache-Status: TCP_MISS
Purged Successfully
-------------
http://www.dutchclothing.com.edgesuite-staging.net/images/5.jpg
Cache-Status: TCP_HIT
Purging....
Cache-Status: TCP_MISS
Purged Successfully
-------------
