"""
Examples demonstrating mining Crossref using library functions.

Requires Python 3.
"""
import crm_lib as lib

"""Example 1"""

ISSN = "1935-1011"

# Facets (see Crossref API doc)
facets = {
    'type-name': 'journal-article'
}

# Filters (see Crossref API doc)
filters = {
    'from-pub-date': '2010-01-01',
    'is-update': 'false'
}

# Fields to fetch (See Crossref API doc esp. Crossref API format)
fields = ['DOI', 'URL', 'title', 'author', 'issued']
# Functions to process field data
field_parsers = [lib.parse_DOI, lib.parse_URL, lib.parse_title, lib.parse_authors,
                 lib.parse_date]

# Check that ISSN exists
print(lib.check_issn_exists(ISSN))

# Fetch count
print(lib.fetch_count(ISSN, facet=facets, filter=filters))

# Fetch batch of works
batch = lib.fetch_batch(ISSN, n=2, fields=fields, field_parsers=field_parsers,
                        facet=facets, filter=filters)
print(batch)

"""Example 2"""
ISSN = "1520-5126"

# Search query (see CrossRef API doc)
query = "hydration"

# Facets (see Crossref API doc)
facets = {
    'type-name': 'journal-article'
}

# Filters (see Crossref API doc)
filters = {
    'from-pub-date': '2018-01-01',
    'until-pub-date': '2020-09-28'
}

# Fields to fetch (See Crossref API doc esp. Crossref API format)
fields = ['DOI', 'URL', 'title', 'author', 'issued']
# Functions to process field data
field_parsers = [lib.parse_DOI, lib.parse_URL, lib.parse_title, lib.parse_authors,
                 lib.parse_date]

# Check that ISSN exists
print(lib.check_issn_exists(ISSN))

# Fetch count
print(lib.fetch_count(ISSN, query=query, facet=facets, filter=filters))

# Fetch two random samples
batch = lib.fetch_batch(ISSN, n=50, fields=fields, query=query, field_parsers=field_parsers,
                        facet=facets, filter=filters)
print(batch)
