# Webdex
Webdex is a Python library and script to generate a website from text, PDF, PPTX and JSON files. It converts text from files into a JSON intermediate format. This JSON intermediate contains a list of objects, each of which builds a webpage in the website. The object (source code) for each webpage contains a 'title' string and a 'body' list of strings. Each string in 'body' makes a paragraph in the webpage. Links are added to these strings that hyperlink to other pages in the dex. Automatic search and hyperlink is yet to be implemented.

```bash
python webdex.py
```
