# ROADtools 
*(**R**ogue **O**ffice 365 and **A**zure (active) **D**irectory tools)*


ROADtools is a framework to interact with Azure AD. It consists of a library (roadlib) with common components, the ROADrecon Azure AD exploration tool and the ROADtools Token eXchange (roadtx) tool.

## ROADlib

ROADlib is a library that can be used to authenticate with Azure AD or to build tools that integrate with a database containing ROADrecon data. The database model in ROADlib is automatically generated based on the metadata definition of the Azure AD internal API. ROADlib lives in the ROADtools namespace, so to import it in your scripts use `from roadtools.roadlib import X`

## ROADrecon
ROADrecon is a tool for exploring information in Azure AD from both a Red Team and Blue Team perspective. In short, this is what it does:
* Uses an automatically generated metadata model to create an SQLAlchemy backed database on disk.
* Use asynchronous HTTP calls in Python to dump all available information in the Azure AD graph to this database.
* Provide plugins to query this database and output it to a useful format.
* Provide an extensive interface built in Angular that queries the offline database directly for its analysis.

ROADrecon uses `async` Python features and is only compatible with Python 3.7 and newer (development is done with Python 3.8, tests are run with versions up to Python 3.11). 
