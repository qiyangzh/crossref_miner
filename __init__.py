"""
Queries CrossRef using CrossRef REST API and fetches
- Published date
- Author
- Title
- DOI
- URL
for each journal article (which isn't an update) published in a journal from a given date.

Requires Python 3 and (optional) tqdm
"""
import urllib.request
import json
import csv

display_progress_bar = True
try:
    from tqdm import tqdm
except ImportError:
    display_progress_bar = False

"""User-defined parameters"""
issn = "1935-1011"  # ISSN of journal
date = "2001-01-01"  # Date to begin fetching data from
output_csv_file = "AERJ_from_2001.csv"  # CSV file to write data to
output_doi_file = "AERJ_from_2001_doi.txt"  # Text file to write DOIs to

"""Control data fetching interval (optional)"""
rows = 100  # Number of papers to fetch each query (maximum 1000)

"""Begin fetch"""
query_string = "https://api.crossref.org/journals/{}/works?facet=type-name:journal-article&filter=is-update:false,from-pub-date:{}".format(issn, date)

# Sort by publication date, in reverse
query_string = query_string + "&sort=published&order=desc"

# Fields to return
fields = ['published-online', 'author', 'title', 'DOI', 'URL']

query_string = query_string + "&select={}".format(",".join(fields))

# Fetch headers
header_query_string = query_string + "&rows=0"

with urllib.request.urlopen(header_query_string) as url:
    data = json.loads(url.read().decode())
    total_items = data['message']['total-results']

print("Fetching {} papers".format(total_items))

# Data structure to store all data
all_papers = []

query_string = query_string + "&rows={}".format(rows)

offsets = range(total_items)[::rows]

if(display_progress_bar):
    offsets = tqdm(offsets)
else:
    print("Fetching data...")

for offset in offsets:
    current_query_string = query_string + "&offset={}".format(offset)

    with urllib.request.urlopen(current_query_string) as url:
        data = json.loads(url.read().decode())

        for i in data['message']['items']:
            # Date
            date = "-".join([str(num) for num in i['published-online']['date-parts'][0]])
            # Author
            try:
                author = ", ".join(d['family'] for d in i.get('author'))
            except (KeyError, TypeError):
                author = ""
            # Title
            title = " ".join(i['title'][0].split())
            # DOI
            doi = i['DOI']
            # URL
            url = i['URL']
            all_papers.append([date, author, title, doi, url])

# Check that all data has arrived
assert(len(all_papers) == total_items)

# Print list of DOIs
with open(output_doi_file, 'w') as of:
    for paper in all_papers:
        of.write(paper[3] + "\n")

# Write data to CSV
all_papers.insert(0, ['Published date', 'Author', 'Title', 'DOI', 'URL'])
with open(output_csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_papers)
