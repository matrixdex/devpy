# Webdex
Webdex generates a website from text, PDF and JSON files using a Python script ```dev.py```. It helps freely host and rapidly update [The Matrix Dex](https://alinoorul.github.io). Webdex is built in [Research Engine](https://alinoorul.github.io/researchengine.html) so scientists host their own journals. 

Get a webdex to put your research papers on the Internet for free. Read TL;DR to get your research online fast. 

Webdex converts text from files into a JSON intermediate format. This JSON intermediate contains a list of objects, each of which builds a webpage in the website. The object (source code) for each webpage contains a 'title' string and a 'body' list of strings. Each string in 'body' makes a paragraph in the webpage. Links are added to these strings that hyperlink to other pages in the dex.

### Installation

```bash
pip install PyPDF2
```

### Initial setup

```bash
python dev.py
```

Run dev.py to create supporting directories and a sample dex. Current working directory (where Python command is run) must be where 'dev.py' file, 'assets' folder and ```styles.css``` file are present. Running dev.py for the first time generates folders ```/backup```, ```/dex```, ```/raw```, ```/webdex``` and files ```config.json``` and ```data.json```.

### Add PDFs

Add PDFs to ```/raw``` folder.

```bash python dev.py```. This generates editable ```dummy.json``` in root directory.

Run ```bash python dev.py``` again to generate webdex in ```/dex``` folder.

Editable ```dummy.json``` for hyperlinks and formatting.

### Viewing website

Open ```index.html``` in ```/dex``` folder.

### Adding data manually

Manually edit ```data.json```. 

```bash python dev.py``` to re-generate website with new data (backup functionality not added here).

### Adding data from PDF, TXT and JSON files

Add PDF, text and JSON files to ```/raw``` folder. Run ```bash python dev.py``` to generate ```dummy.json```. Run ```bash python dev.py``` again to generate webdex in ```/dex``` folder.

```bash
python dev.py
```

Text from files in 'raw' folder are extracted and added 'dummy.json'. You can edit 'dummy.json' at this step (more on that below). Once done editing, run 'dev.py' again.

### Editing 'data.json' and 'dummy.json' files

These files are structured like this:

```bash
[
  {"title": "Page 1"
  "body": ["Page 1", "<a href='page2.html'>Page 2</a>"]},
  {"title": "Page 2"
  "body": ["Page 2", "<a href='page1.html'>Page 1</a>"]}
]
```
The alphanumberic title for each page without spaces and in lowercase forms the title of the HTML file. This allows you to add links by adding the <a> tag in strings in the body object for each webpage object. Strings in 'body' form paragraphs of the webpage. This is how 'data.json' and 'dummy.json' are composed of a list of JSON objects, each representing a webpage. The title of each page is unique. In case the same title is detected for 2 objects inside the 'data.json' file or between 'data.json' and 'dummy.json' files, the objects are combined into 1 webpage with the same title and body strings combined. This can be used to edit 'dummy.json'. You can use existing titles in 'data.json' in 'dummy.json' objects to add data to a specific webpage instead of creating a new one. When 'data.json' is updated with data from 'dummy.json' (i.e. 'raw' folder) when 'dev.py' is run a second time after adding files to the 'raw' folder, a backup is made. This backup is stored in 'backup' folder as 'data.json'. This is done in case 'data.json' was updated wrongly and you'd like to go back to the original 'data.json' file without content from the 'raw' folder. Replace the 'data.json' file in the root directory with the one from the 'backup' folder and run 'dev.py' to generate the original dex (without added data). 


### Root directory structure

Folder 'dex': Website root folder with HTML files, styles.css and 'assets' folder. This folder Index.html is the entry point to this website. This website referred to as dex.

Folder 'backup': Contains backup of 'data.json' file. This backup is updated when 'data.json' is updated using files from the 'raw' folder.

Folder 'raw': Used to append data to the dex. Add PDF, text and JSON files here. The first time you add files here and run dev.py, text from these files will be added to 'dummy.json'. You can make changes to 'dummy.json' before committing it source 'data.json'. Once data is added to 'dummy.json' from the 'raw' folder, files in the 'raw' folder are moved to the 'clear' subfolder within the 'raw' folder.

Folder 'webdex': TODO implement a library for dev.py's functionality.

File 'data.json': Contains the source code for each webpage. 'Data.json' stores a list of objects in JSON format. Each object contains a 'title' string and a 'body' list of strings. 'Title' denotes title of the HTML page and name of the HTML file for that page for easier hyperlinking. Lowercase, space and special character (not number) removed title string forms the HTML filename. This file is meant to be edited in Visual Studio Code, using it as a word editor.

File 'config.json': Stores the name of the dex. This serves as the source name that is used across the script as dexname. It also stores the name of the author.

### Working example

[The Matrix Dex](https://alinoorul.github.io) is a webdex. Current webdex workflow of this website's maintainer comprises of editing ```data.json```, running ```dev.py``` to get updated website and adding updated HTML files to the project hosted [here](https://github.com/alinoorul/alinoorul.github.io) on GitHub Pages. [https://alinoorul.github.io](https://alinoorul.github.io) is the free URL thanks to GitHub.  

## TL; DR
Run dev.py once. Put PDFs in raw folder. Run dev.py twice. index.html in the dex folder is your website. 

### Next steps

Automatic search and hyperlink.

Neural network control for smarter website generation with images, tables etc.

## Need help?

Ask the human behind devpy at manonthemoon13131@gmail.com.




