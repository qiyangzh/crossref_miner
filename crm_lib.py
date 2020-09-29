"""
Library functions for mining Crossref.
"""
import urllib.request
import json

CR_URL = "https://api.crossref.org/"

# Send email address along with query, to place query in polite pool of servers.
# Crossref can contact you for problems with the query.
# This is the 'polite' thing to do, as per the Crossref API doc!
POLITE_MAILTO = "XXXX@XXXX.XXX"


def check_issn_exists(issn):
    """Checks if ISSN exists in Crossref.

    Args:
        issn: string

    Returns:
        bool
    """
    request_str = CR_URL + "journals/{}?mailto={}&".format(issn, POLITE_MAILTO)
    with urllib.request.urlopen(request_str) as response:
        status = response.getcode()
        return status == 200


def fetch_count(issn, facet=None, filter=None, query=None):
    """Fetches total number of works which meet facet, filter and query criteria in
    a journal given its ISSN.

    Args:
        issn: string
        facet: dict
        filter: dict
        query: string

    Returns:
        int
    """
    if check_issn_exists(issn):
        request_str = CR_URL + "journals/{}/works?mailto={}&rows=0&".format(issn, POLITE_MAILTO)

        if facet is not None:
            facet_list = []
            for key in facet.keys():
                facet_list.append("{}:{}".format(key, facet[key]))
            request_str += "facet=" + ",".join(facet_list) + "&"

        if filter is not None:
            filter_list = []
            for key in filter.keys():
                filter_list.append("{}:{}".format(key, filter[key]))
            request_str += "filter=" + ",".join(filter_list) + "&"

        if query is not None:
            query = "+".join(list(query.strip().split()))
            request_str += "query=" + query + "&"

        # Debugging:
        # print(request_str)
        with urllib.request.urlopen(request_str) as response:
            data = json.loads(response.read().decode())
            total_items = data['message']['total-results']
            return total_items
    else:
        raise ValueError("ISSN not indexed in Crossref?")


def fetch_batch(issn, n=1, offset=0, fields=None, field_parsers=None, facet=None, filter=None, query=None):
    """Fetches a batch of works (sorted in descending order by date published) which meet facet,
    filter, and query criteria in a journal given its ISSN.

    Works fetched in JSON format (https://github.com/Crossref/rest-api-doc/blob/master/api_format.md).

    Args:
        issn: string
        n: Size (int, default = 100) of batch
        offset: Offset (int, default = 0) to fetch results from
        fields: list of strings
        facet: dict of string:string key,value pairs
        filter: dict of string:string key,value pairs
        query: string

    Returns:
        list of samples
    """
    if check_issn_exists(issn):
        output_list = []

        request_str = CR_URL + "journals/{}/works?mailto={}&rows={}&offset={}&sort=published&order=desc&".format(issn, POLITE_MAILTO, n, offset)

        if fields is not None:
            request_str += "select={}".format(",".join(fields)) + "&"

        if facet is not None:
            facet_list = []
            for key in facet.keys():
                facet_list.append("{}:{}".format(key, facet[key]))
            request_str += "facet=" + ",".join(facet_list) + "&"

        if filter is not None:
            filter_list = []
            for key in filter.keys():
                filter_list.append("{}:{}".format(key, filter[key]))
            request_str += "filter=" + ",".join(filter_list) + "&"

        if query is not None:
            query = "+".join(list(query.strip().split()))
            request_str += "query=" + query + "&"

        # Debugging:
        # print(request_str)
        with urllib.request.urlopen(request_str) as response:
            data = json.loads(response.read().decode())
            for item in data['message']['items']:
                output_item = []
                for fidx in range(len(fields)):
                    field = fields[fidx]
                    field_parser = field_parsers[fidx]
                    try:
                        extracted_field = item[field]
                        output_item.append(field_parser(extracted_field))
                    except KeyError:
                        output_item.append("")
                output_list.append(output_item)
        return output_list
    else:
        raise ValueError("ISSN not indexed in Crossref?")


"""Functions to convert fields returned from query into human-readable strings"""


def parse_date(date):
    return "-".join([str(num) for num in date['date-parts'][0]])


def parse_authors(author_array):
    try:
        authors = ", ".join(d['family'] for d in author_array)
    except (KeyError, TypeError):
        authors = ""
    return authors


def parse_title(title):
    return " ".join(title[0].split())


def parse_URL(url):
    return url


def parse_DOI(doi):
    return doi
