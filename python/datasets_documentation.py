"""
Dataset Documentation.py

This module provides reference information about datasets available through the Explore Education Statistics (EES) API
including how they are structured, how to find them and how to query them effectively.

Overview 

Datasets are part of publications and contain statistical data. Each dataset contains statistical data that can be required 
via the EES API. Datasets can have multiple versions and each version has associated metadata describing the availble filters,
indicators, time periods and geographic levels. 

Only datasets that meet minimum data quality standards are available via the API. You can browse available API datasets at:
https://explore-education-statistics.service.gov.uk/data-catalogue

Workflow 

Typical steps to retrieve data from the EES API:

step 1: Find a publication 

    Use get_publications() to browse or search all available publications.
    Each publication has a unique publication_id.

    Example:
        from get_publications import get_publications
        pubs = get_publications(search="attendance", ees_environment="prod")

step 2: Find a dataset within a publications
    Use get_data_catalogue() with a publication_id to list all datasets available
    within the publication. Each dataset has a unique dataset_id.

    Example:
        from get_data_catalogue import get_data_catalogue
        catalogue = get_data_catalogue(
            publication_id="cbbd299f-8297-44bc-92ac-558bcf51f8ad",
            ees_environment="prod")

step 3: Get dataset metadata
    Use get_meta() with a dataset_id to retrieve metadata including:
    - filter_columns: available filter columns names and IDs
    - filter_items: available filter item labels and sqids 
    - indicators: available time period codes and labels 
    - time_periods: available time period codes and labels 
    - locations: available geographic locations and sqids 

    Example:
        from get_meta import get_meta
        meta = get_meta(
            dataset_id="63629501-d3ca-c471-9780-ec4cb6fdf172",
            ees_environment="prod")

step 4: Query the dataset
    Use query_dataset() or post_dataset() with the sqids from metadata
    to retrieve specific row of data.

    Example:
        from query_dataset import query_dataset
        result = query_dataset(
            dataset_id="63629501-d3ca-c471-9780-ec4cb6fdf172",
            json_query={
                "criteria": {"geographicLevels": {"in": ["NAT"]}},
                "indicators": [],
                "page": 1,
                "pageSize": 10
                
            },
            ees_environment="prod")

DATASET COMPONENTS

Dataset ID 
    A unique identifier (UUID) for a dataset e.g..,
    "63629501-d3ca-c471-9780-ec4cb6fdf172"
    Used in all dataset-level API calls.

Dataset Version
    A specific release of a dataset in "major.minor.patch" format
    e.g. "2.1.0". Wildcards are supported e.g. "2.*", "*".
    If not specified, the latest version is returned.

Filters
    Categorical columns used to subset data e.g. school_type, gender.
    Each filter has a col_id (sqid) and a set of filter items.
    each with their own item_id (sqid).
    use sqids -  not labels - when constructinf queries.

Indicators 
    Numeric metric columns to retrieve e.g. session_count, percentage.
    Each indicator has a col_id(sqid).
    At least one indicator must be specified in most query types.

Time Periods
    Available time ranges in the dataset e.g. "2024|AY", "2025|W4".
    Format is "period|code" where code identifies the period type:
    - AY = Academic year
    - FY = Financial year
    - CY = Calendar year
    - W{n} = Week number

Geographic Levels
    Regional breakdowns avaialble in the dataset.
    Uses short codes: NAT (National), REG (Regional), LA (Local Authority),
    SCH (School), etc.
    See geog_level_lookup.py for the full list of codes 

Locations
    Specific geographic areas within a level e.g. a particular LA or school.
    Each location has an item_id (sqid) from the metadata.


ENVIRONMENTS

prod - https://api.education.gov.uk/statistics/v1    (Public)
dev - https://pp-api.education.gov.uk/statistics-dev  (DFE VPN)
test - https://pp-api.education.gov.uk/statistics-test (DFE VPN)
preprod - https://pp-api.education.gov.uk/statistics-preprod (DFE VPN)


Notes 

* Always check metadata before querying - filters and indicators 
  must match the dataset structure exactly.

* Use sqids (not labels) for filters, indicators and locations in queries.
  Labels may change between dataset versions; sqids do not.

* For large datasets, use page_size and max_page to avaoid downloading
  too much data at once.Consider preview_dataset() for exploration.

* The API uses POST requests for data queries. GET is supported but 
  offers limited functionally - POST is recommended.


"""
