"""
Dataset Documentation

This module provides information about datasets available through the Explore Education Statistics (EES) API

Overview 

Datasets are part of publications and contain statistical data. Each dataset can have multiple versions and associated metadata. 

Workflow 

Typical steps to use datasets:

1. Get publications 
2. Get data catalogue 
3. Get dataset metadata
4. Query dataset for results 

Dataset Components 

* Dataset ID: Unique identifier 
* Version: Specific release of dataset
* Filters: Used to subset data (e.g., gender, age)
* Indicators: Metrics or values to retrieve 
* Time Periods: Available time ranges 
* Geography: Regional breakdown 


Notes

* Metadata must be checked before querying datasets 
* Filters and indicators must match dataset structure 

"""