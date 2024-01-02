# Webdex
Webdex is a Python library and script to generate a website from text, PDF and JSON files. It converts text from files into a JSON intermediate format. This JSON intermediate contains a list of objects, each of which builds a webpage in the website. The object (source code) for each webpage contains a 'title' string and a 'body' list of strings. Each string in 'body' makes a paragraph in the webpage. Links are added to these strings that hyperlink to other pages in the dex.

Dependencies: PyPDF2

Run dev.py to create supporting directories and a sample dex. 

```bash
python dev.py
```

Running the above for the first time generates folders [backup, dex, raw, webdex] and files [config.json, data.json].

Folder 'dex' contains website files. Index.html is the entry point to this website. This website referred to as dex.

Folder 'backup' contains a backup of 'data.json' file. This backup is updated when 'data.json' is updated using files from the 'raw' folder.

Folder 'raw' is used to append data to the dex. Add PDF, text and JSON files here. The first time you add files here and run dev.py, text from these files will be added to 'dummy.json'. You can make changes to 'dummy.json' before committing it source 'data.json'. Once data is added to 'dummy.json' from the 'raw' folder, files in the 'raw' folder are moved to the 'clear' subfolder within the 'raw' folder.

Folder 'webdex' is to implement a library for dev.py's functionality.

File 'data.json' contains the source code for each webpage. 'Data.json' stores a list of objects in JSON format. Each object contains a 'title' string and a 'body' list of strings. 'Title' denotes title of the HTML page and name of the HTML file for that page for easier hyperlinking. Lowercase, space and special character (not number) removed title string forms the HTML filename. This file is meant to be edited in Visual Studio Code, using it as a word editor.

File 'config.json' stores the name of the dex. This serves as the source name that is used across the script as dexname. It also stores the name of the author.

# Next steps

Automatic search and hyperlink is yet to be implemented.

Neural network control for smarter website generation with images, tables etc.


