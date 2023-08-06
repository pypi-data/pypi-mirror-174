# basylic-python-client

Module to access [Basylic](https://www.basylic.fr/) API.

# Summary

Developed by ETAONIS, Basylic is a SaaS solution performing document
fraud detection with "state-of-the-art" performances. The solution is
also used as a powerful tool to extract information from
documents. This module provides a Python interface for accessing
Basylic.

# Installation

This module is available on PyPI. You can install it with `pip` command:

```
pip install basylic
```

Alternatively, you can access the module source code on GitHub:

* https://github.com/basylic-team/basylic-python-client

# Basic usage

To access the API, refresh and access tokens should be provided. You
can access your Refresh token via the Portal interface. Then, we
recommend you store its value in the environment variable
`BASYLIC_REFRESH_TOKEN`.

```python
from basylic import Basylic
basylic = Basylic()
```

Alternatively, if your refresh token is stored in a non-standard
location, you can specify its value with argument `refresh_token` 
during class instantiation:

```python
from basylic import Basylic
basylic = Basylic(refresh_token=...)
```

2. At least two arguments should be set: one of `file_path`,
   `file_obj` or `ftp_file`, and `document_type`:

```python
basylic.send_document(file_path="corinne-berthier-recto-verso.pdf", document_type="french_ids")
```

* The `file_path` argument is a string with the document path (e.g.: "~/FILE.pdf")
* `document_type` is a string specifying which Basylic API to call (e.g.: "french_ids")

Possible values for `document_type` are: `'french_ids'`, `'rib'`, `'ri'`, `'avis-imposition'`...

With those arguments specified, `send_document` returns a comprehensive JSON document.

3. Data about applicants can also be joined to the API call:

```python
applicants_information = {"applicant_0": {"identity": "BERTHIER CORINNE"}}
basylic_result = basylic.send_document(
    file_path="corinne-berthier-recto-verso.pdf",
    document_type="french_ids", applicants_information=applicants_information)
print(basylic_result)
```

4. And various arguments could be passed as kwargs. For example:

* a. `save_report=True` will save the result of your request in your
  user space on Basylic Portal;
* b. `with_image=True` will return a base64 image for each recognised document;

For example, this code:

```python
applicants_information = {"applicant_0": {"identity": "BERTHIER CORINNE"}}
basylic_result = basylic.send_document(
    file_path="corinne-berthier-recto-verso.pdf",
    document_type="french_ids", applicants_information=applicants_information,
    with_image=True, save_report=True)
print(basylic_result)
```

will act in the following way:

1. Uploads of document whose path is `file_path` to Basylic service `french_ids`;
2. Produces of a JSON document `basylic_result` with all relevant information;
3. Compares `identity` provided and identity extracted by Basylic OCR;
5. A base64 encoded image will be returned in the approriate key of `basylic_result`.
