"""
geog_level_lookup.py 
Geographic Level lookup table - maps API shorthand codes to human-friendly names,
Converted from R: data-raw/geog_level_lookup.R
"""


GEOG_LEVEL_LOOKUP = {
    "EDA":  "English  devolved area",
    "INST":  "Institution",
    "LA":    "Local authority",
    "LAD":   "Local authority district",
    "LEP":   "Local enterprise partnership",
    "LSIP":  "Local skills improvement plan area",
    "MAT":   "Multi-academy trust",
    "MCA":   "MCA",
    "NAT":   "National",
    "OA":    "Opportunity area",
    "PA":    "Planning area",
    "PCON":  "Parliamentary constituency",
    "PROV":  "Provider",
    "REG":   "Regional",
    "RSC":   "Regional school comissioner region",
    "SCH":   "School",
    "SPON":  "Sponsor",
    "WARD":  "Ward",
}

GEOG_LEVEL_LOOKUP_REVERSE = {v: k for k, v in GEOG_LEVEL_LOOKUP.items()}

import pandas as pd 

geog_level_lookup = pd.DataFrame({
    "api_friendly":  list(GEOG_LEVEL_LOOKUP.keys()),
    "human_friendly": list(GEOG_LEVEL_LOOKUP.values())
})