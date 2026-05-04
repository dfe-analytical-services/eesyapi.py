# import requests, json 

# url = "https://api.education.gov.uk/statistics/v1/publications?pageSize=5"

# r = requests.get(url)
# print("STATUS:" , r.status_code)
# data = r.json()
# for pub in data.get("results",[]):
#     print(f"Pub ID: {pub["id"]}  Title: {pub['title']}")
#     ds_url = f"https://api.education.gov.uk/statistics/v1/publications/{pub['id']}/data-sets?pageSize=3"
#     ds_r = requests.get(ds_url)
#     if ds_r.status_code == 200:
#         for ds in ds_r.json().get("results", []):
#             print(f" Dataset ID: {ds['id']} Title: {ds['title']}")



# import requests, json

# url ="https://pp-api.education.gov.uk/statistics-preprod/v1/publications?pageSize=3"

# r = requests.get(url)
# print("STATUS:" , r.status_code)
# data = r.json()
# for pub in data.get("results",[]):
#     print(f"Pub ID: {pub["id"]}  Title: {pub['title']}")
#     ds_url = f"https://api.education.gov.uk/statistics/v1/publications/{pub['id']}/data-sets?pageSize=2"
#     ds_r = requests.get(ds_url)
#     if ds_r.status_code == 200:
#          for ds in ds_r.json().get("results", []):
#              print(f" Dataset ID: {ds['id']} Title: {ds['title']}")


# import requests, json 

# base = "https://pp-api.education.gov.uk/statistics-preprod/v1"

# pubs = requests.get(f"{base}/publications?pageSize=3").json()

# for pub in pubs.get("results",[]):
#     print(f"Pub: {pub["id"]} - {pub['title']}")
#     ds = requests.get(f"{base}/publications/{pub['id']}/data-sets?pageSize=2").json()
#     for d in ds.get("results", []):
#         print(f" Dataset: {d['id']} - {d['title']}")

# from get_publications import warning_max_pages
# result = warning_max_pages({"paging": {"totalPages": 3, "page": 3}})
# print(repr(result))


# import requests, json 

# url = "https://api.education.gov.uk/statistics/v1/publications?pageSize=10"
# r = requests.get(url)
# data = r.json()
# for pub in data.get("results", []):
#     print(f"ID: {pub['id']} Title: {pub['title']}")

# import requests 

# r = requests.get("https://api.education.gov.uk/statistics/v1/publications?pageSize=10")
# for pub in r.json().get("results", []):
#     print(pub['id'], '-', pub['title'])

# import requests
# pub_ids = {
#     "EARLY_YEARS_PUB_ID":"fcda2962-82a6-4052-afa2-ea398c53c85f",
#     "APPRENTICESHIPS_PUB_ID" : "412d8090-ab45-455a-c176-08dbf5ab522b",
#     "PHONICS_PUB_ID" : "5becb18e-852b-4cdf-e2e8-08dcc3489646",
#     "PUPIL_ABSENCE_PUB_ID": "cbbd299f-8297-44bc-92ac-558bcf51f8ad",
#     "OUTCOMES_PUB_ID" : "f51895df-c682-45e6-b23a-3138ddbfdaeb",
#     "CHILDREN_NEEDS_PUB_ID": "89869bba-0c00-40f7-b7d6-e28cb904ad37",
#     "ALEVEL_PUB_ID" : "3f3a66ec-5777-42ee-b427-8102a14ce0c",
#     "KS4_PUB_ID" : "c8756008-ed50-4632-9b96-01b5ca002a43",
#     "KS2_PUB_ID": "8b7474f9-5878-4acc-7357-08da5f64dcf1"

# }

# base  = "https://api.education.gov.uk/statistics/v1"
# for name, pub_id in pub_ids.items():
#     r = requests.get(f"{base}/publications/{pub_id}/data-sets?pageSize=1")
#     count = len(r.json().get("results",[])) if r.status_code == 200 else 0
#     print(f"{r.status_code} | {count} datasets | {name}")

