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



import requests, json

url ="https://pp-api.education.gov.uk/statistics-preprod/v1/publications?pageSize=3"

r = requests.get(url)
print("STATUS:" , r.status_code)
data = r.json()
for pub in data.get("results",[]):
    print(f"Pub ID: {pub["id"]}  Title: {pub['title']}")
    ds_url = f"https://api.education.gov.uk/statistics/v1/publications/{pub['id']}/data-sets?pageSize=2"
    ds_r = requests.get(ds_url)
    if ds_r.status_code == 200:
         for ds in ds_r.json().get("results", []):
             print(f" Dataset ID: {ds['id']} Title: {ds['title']}")


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

