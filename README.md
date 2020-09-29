# Crossref Data Extraction Tool

A simple tool to fetch citations using the Crossref REST API.

Refer to Crossref REST API documentation at https://github.com/CrossRef/rest-api-doc.

## Requirements
- python 3
- tqdm (optional; for neat progress bars in console/GUI)

## Contents
- Libary functions (in `crm_lib.py`)
- Usage examples (in `crm_examples.py`)
- Script to fetch all works from a journal (`fetch_all_journal_works.py`)

Edit parameters in `fetch_all_journal_works.py` to customize the script for a
specific search.

## Usage:
- **Before running any scripts, set the value of the POLITE_MAILTO constant in
`crm_lib.py` to your email address.**

- To use the library functions in a Python script (must be in the same directory as `crm_lib.py`)

```python
import crm_lib
```

- To run examples from console:

```sh
python crm_lib_examples.py
```

- To fetch all works from a journal after applying filters:

```sh
python fetch_all_journal_works.py
```
