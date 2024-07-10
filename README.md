# Webdex
Webdex generates a website from text, PDF and JSON files using a Python script ```dev.py```. It helps freely host and rapidly update [The Matrix Dex](https://alinoorul.github.io). Webdex is built in [Research Engine](https://alinoorul.github.io/researchengine.html) so scientists host their own journals. 

Get a webdex to put your research papers on the Internet for free. Read TL;DR to get your research online fast. 

Webdex converts text from files into a JSON intermediate file ```data.json```. This JSON intermediate contains a list of objects, each of which builds a webpage in the website. The object (source code) for each webpage has a string ```title``` and a list of strings ```body = [paragraph1, paragraph2]```. Each string in ```body``` makes a paragraph in the webpage. Hyperlinks can be added like HTML.

### Installation

```bash
pip install PyPDF2
```

### Initial setup

```bash
python dev.py
```

Creates supporting directories and a sample dex. Root directory where Python command is run must have ```dev.py```, ```/assets``` folder and ```styles.css```. Running ```dev.py``` for the first time generates folders ```/backup```, ```/dex```, ```/raw``` and ```/webdex```, and files ```config.json``` and ```data.json```.

### Add PDFs

Add PDFs to ```/raw``` folder.

```bash 
python dev.py
```
This generates editable ```dummy.json``` in root directory.

Run ```python dev.py``` again to generate webdex in ```/dex``` folder.

Editable ```dummy.json``` for hyperlinks and formatting.

### Viewing website

Open ```index.html``` in ```/dex``` folder.

### Adding data manually

Manually edit ```data.json```. 

```bash
python dev.py
```
Re-generate website with new data (backup functionality not added here).

### Adding data from PDF, TXT and JSON files

Add PDF, text and JSON files to ```/raw``` folder. Run ```bash python dev.py``` to generate ```dummy.json```. Run ```bash python dev.py``` again to generate webdex in ```/dex``` folder.

```bash
python dev.py
```

Text from files in ```/raw``` folder are extracted and added ```dummy.json```. Edit ```dummy.json``` at this step (more on that below). Once done editing, run ```python dev.py``` again.

### Editing ```data.json``` and ```dummy.json``` files

File structure:
```bash
[
  {"title": "Page 1"
  "body": ["Page 1", "<a href='page2.html'>Page 2</a>"]},
  {"title": "Page 2"
  "body": ["Page 2", "<a href='page1.html'>Page 1</a>"]}
]
```
Alphanumberic title for each page without spaces and in lowercase forms the title of the HTML file. Add links by adding the ```<a>``` tag in strings in the body object for each webpage object.

Strings in ```body``` form paragraphs of the webpage. ```data.json``` and ```dummy.json``` are lists of JSON objects. Each object in the list represents a webpage. The title of each page is unique. In case the same title is detected for 2 objects inside the ```data.json``` file or between ```data.json``` and ```dummy.json``` files, the objects are combined into 1 webpage with the same title and body strings combined. This can be used to edit ```dummy.json```.

To add to an existing page in ```data.json```, use a webpage object ```dummy.json``` objects with the same title as existing webpage object in ```data.json```. to add data to a specific webpage instead of creating a new one. 



### JSON webpage strcuture

Each webpage object in ```data.json``` and ```dummy.json``` is a JSON object.

```bash
{"title": "", "body": []},
```

### Root directory structure

```/dex``` folder: Website root folder with HTML files, ```styles.css``` and ```/assets``` folder. ```/dex/index.html``` is the entry point to this website, also referred to as dex and webdex.

```backup``` folder: Contains backup of ```data.json```. This backup is updated when ```data.json``` is updated using files from the ```/raw``` folder.

```raw``` folder: Appends data to the dex. Add PDF, text and JSON files here. The first time you add files here and run ```python dev.py```, text from these files will be added to ```dummy.json```. You can edit ```dummy.json``` before committing it to source ```data.json```. Once data is added to ```dummy.json``` from the ```/raw``` folder, files in the ```/raw``` folder are moved to the ```/raw/clear``` subfolder within the ```/raw``` folder.

```/webdex``` directory: TODO implement a library for ```dev.py```.

```data.json```: Contains the source code for each webpage. ```data.json``` stores a list of objects in JSON format. Each object contains a ```title``` string and a ```body``` list of strings. 'Title' denotes title of the HTML page and name of the HTML file for that page for easier hyperlinking. Lowercase, space and special character (not number) removed title string forms the HTML filename. This file is meant to be edited in Visual Studio Code, using it as a word editor.

```config.json```: Stores the name of the dex. This serves as the source name that is used across the script as dexname. It also stores the name of the author.

### Backup functionality

When ```data.json``` is updated with data from ```dummy.json``` (from ```/raw``` folder) when ```dev.py``` is run a second time, a backup is made. This backup is stored in ```/backup``` folder as ```data.json```. If ```data.json``` was updated wrongly and you'd like to go back to the original ```data.json``` file without added content from the ```/raw``` folder, replace ```/data.json``` with ```/backup/data.json``` and run ```python dev.py``` to generate the original dex (without added data). 

### Working example

[The Matrix Dex](https://alinoorul.github.io) is a webdex. Current webdex workflow of this website's maintainer comprises of editing ```data.json```, running ```dev.py``` to get updated website and adding updated HTML files to the project hosted [here](https://github.com/alinoorul/alinoorul.github.io) on GitHub Pages. [https://alinoorul.github.io](https://alinoorul.github.io) is the free URL thanks to GitHub.  

## TL; DR
Run ```python dev.py``` once. Put PDFs in ```/raw``` folder. Run ```python dev.py``` twice. ```/dex/index.html``` (in the ```/dex``` folder) is your website. 

### Next steps

Automatic search and hyperlink.

Neural network control for smarter website generation with images, tables etc.

## Need help?

Ask the human behind devpy at manonthemoon13131@gmail.com.




