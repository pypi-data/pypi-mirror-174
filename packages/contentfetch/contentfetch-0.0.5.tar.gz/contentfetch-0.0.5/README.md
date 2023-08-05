# content-fetch


This package helps you parse the text from the webpage. The input to the function can be a path to an HTML file on your disk or a URL to a web page. 

You can install the package by running the following command

```
pip install contentfetch
```


Please refer to the code snippet for parsing the text from the HTML file

```
import contentfetch

results_json = contentfetch.extract_content(html=<html_file>)

results_json

### OR

from contentfetch import extract_content

results_json = extract_content(html=<html_file>)

results_json
```

Please refer to the code snippet for parsing the text from the webpage through URL

```
import contentfetch

results_json = contentfetch.extract_content(url=<webpage_url>)

results_json

### OR

from contentfetch import extract_content

results_json = extract_content(url=<webpage_url>)

results_json
```

