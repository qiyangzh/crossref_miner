"""
Fetches all works from a journal in given date range, saves data to CSV and DOIs
to text file.
"""
import crm_lib as lib
import csv

display_progress_bar = True
try:
    from tqdm import tqdm
except ImportError:
    display_progress_bar = False

"""Parameters to set"""
ISSN = "XXXX-XXXX"  # ISSN of journal
START_DATE = "2000-01-01"  # Date to begin fetching data from (inclusive)
END_DATE = "2001-01-01"  # Date to stop fetching data at (inclusive)
output_csv_file = "XXXX_from_2001.csv"  # CSV file to write data to
output_doi_file = "XXXX_from_2001_doi.txt"  # Text file to write DOIs to
ROWS = 100  # Number of works to fetch each query (maximum 1000)

# Facets (see Crossref API doc)
facets = {
    'type-name': 'journal-article'
}

# Filters (see Crossref API doc)
filters = {
    'from-pub-date': START_DATE,
    'until-pub-date': END_DATE,
    'is-update': 'false'
}

# Fields to fetch (See Crossref API doc esp. Crossref API format)
# Can change the date field from `issued` to `accepted` or `published-print` or `published-online`
# (with caution, as these fields are not required fields in the Crossref database)
fields = ['DOI', 'URL', 'title', 'author', 'issued']
# Functions to process field data
field_parsers = [lib.parse_DOI, lib.parse_URL, lib.parse_title, lib.parse_authors,
                 lib.parse_date]


"""Begin extraction"""
total_items = lib.fetch_count(ISSN, facet=facets, filter=filters)

print("Fetching {} works".format(total_items))

offsets = range(total_items)[::ROWS]

if(display_progress_bar):
    offsets = tqdm(offsets)  # Add progress bar
else:
    print("Fetching data...")

all_works = []

for offset in offsets:
    batch = lib.fetch_batch(ISSN, n=ROWS, offset=offset, fields=fields, field_parsers=field_parsers,
                            facet=facets, filter=filters)
    all_works += batch

# Check
assert(len(all_works) == total_items)

"""Output"""
# Print list of DOIs
with open(output_doi_file, 'w') as of:
    for work in all_works:
        of.write(work[0] + "\n")  # DOI is at index 0

# Write data to CSV
all_works.insert(0, fields)  # CSV header
with open(output_csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_works)
