import PyPDF2
import os
import json
import shutil

def create_indexpage(pages):
    k=''
    for i in range(len(pages)):
        k+='<a href='+pages[i]['html_title']+".html style='font-family:consolas;'>"+pages[i]['title']+'</a><br>'
    template = f"""<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="shortcut icon" type="image/x-icon" href="assets/favicon.ico">
        <link rel="stylesheet" href="styles.css">
        <title>{dexname} Dex</title>
    </head>
    <body>
        <br><h1>{dexname.upper()} DEX</h1><br>
        {k}
        <br><br><br><br><br><br><br>
        <h3><a href="index.html">{dexname.upper()}</a></h3>
    </body>
    </html>
    """
    return template

def create_webpage(title, body):
    k=''
    for i in body:
        k+='<p>'+i+'</p>'
    template = f"""<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="shortcut icon" type="image/x-icon" href="assets/favicon.ico">
        <link rel="stylesheet" href="styles.css">
        <title>{title} - {dexname} Dex</title>
    </head>
    <body>
    <br>
    <h1>{title.upper()}</h1>
    <br>
    {k}
    <br><br><br><br><br><br><br>
    <h3><a href="index.html">{dexname.upper()}</a></h3>
</body>
</html>"""
    return template

def save_webpages(site_folder_path,assets_path,styles_path,pages):
    if 'assets' not in os.listdir(site_folder_path):
        os.mkdir(site_folder_path+'assets//')
    assets=[]
    for i in os.listdir(assets_path):
        shutil.copy(assets_path+"\\"+i,site_folder_path+"\\assets\\")
    shutil.copy(styles_path,site_folder_path)
    for i in pages:
        with open(site_folder_path+i['html_title']+'.html', "w+", encoding="utf-8") as file:
            file.write(i['page'])

def json_to_webpages(json_file):
    with open(json_file, 'r') as f:
        z=f.read()
    p=json.loads(z)
    titles=[]
    pages=[]
    for i in range(len(p)):
        t2="".join(x for x in p[i]['title'] if x.isalnum())
        t2=t2.lower()
        page=create_webpage(p[i]['title'], p[i]['body'])
        if len(p[i]['body'])>0:
            pages.append({'title':p[i]['title'], 'page':page, 'html_title': t2})

    pages = sorted(pages, key=lambda x: x['title'])
    pages.append({'title':f'{dexname} Dex', 'page':create_indexpage(pages) , 'html_title': 'index'})
    return pages

def pdf_to_json(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    data=[] # list of pages if this was new dex
    for i in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[i]
        text = page.extract_text()
        lines = text.split("\n")
        body = lines[1:]  # Rest of the lines form the body
        title=lines[0]
        data.append({'title':title, 'body':body})
    return data

def txt_to_json(txt_path):
    with open(txt_path, 'r') as f:
        z=f.read()
        z=z.split('\n')
    title=os.path.basename(txt_path)
    title=title[:title.find('.')]
    p=[]
    for i in z:
        if len(i)!=0:
            p.append(i)
    return {'title':title, 'body': p}

def get_html_filenames(folder_path):
    filenames=os.listdir(folder_path)
    f=[]
    for i in filenames:
        if len(i)>=5 and i[-5]=='.' and i[-4]=='h' and i[-3]=='t' and i[-2]=='m' and i[-1]=='l':
            f.append(i)
    filenames=f
    return filenames

def html_to_json(site_folder_path):
    data=[]
    raw_html_files=[]
    html_files=get_html_filenames(site_folder_path)
    for file in html_files:
        datum={'title':'', 'body':[]}
        with open(site_folder_path+file, 'r', encoding="utf8") as f:
            z=f.read()
            raw_html_files.append(z)
    for i in raw_html_files:
        datum={'title':'', 'body':[]}
        t=i.split('<title>')
        k=t[1].split('</title>')[0]
        title=k[0:(k.find('-')-1)]
        datum['title']=title
        op=False
        pl=''
        for j in range(len(i)-2):
            if i[j]=='<':
                if i[j+1] == 'p':
                    op=True
                elif i[j+1] == '/':
                    if i[j+2] == 'p':
                        op=False
                        datum['body'].append(pl)
                        pl=''
            if op:
                pl+=i[j]
        k=[]
        for i in datum['body']:
            if len(i.split('<p>'))==2:
                k.append(i.split('<p>')[1])
            else:
                k.append(i)
        datum['body']=k
        data.append(datum)
    return data

def consolidate_json(json_data):
    complete={}
    for i in json_data:
        if i['title'] in complete.keys():
            for k in i['body']:
                    complete[i['title']].append(k)
        else:
            complete[i['title']]=i['body']
    p=[]
    for i in complete:
        p.append({'title':i, 'body':complete[i]})
    return p

def parse_updates(update_path):
    update_files = os.listdir(update_path)
    update_files = [f for f in update_files if os.path.isfile(update_path+'/'+f)]
    p=[]
    for i in update_files:
        p.append({'format': str(i[i.find('.')+1:]), 'file_path': str(update_path + i)})
    updates = p
    updates_json = []
    for i in updates:
        if i['format']=='pdf':
            pdf_pages=pdf_to_json(i['file_path'])
            for i in pdf_pages:
                updates_json.append(i)

        elif i['format']=='txt':
            
            updates_json.append(txt_to_json(i['file_path']))
        elif i['format']=='json':
            
            with open(i['file_path'], 'r') as f:
                z=f.read()
            p=json.loads(z)
            for j in p:
                updates_json.append(j)
    
    updates_json=consolidate_json(updates_json)
    return updates_json

def create_first_json_file(path, dexname):
    indexlink='''<a href="index.html">'''+dexname+'''</a>'''
    z=[
    {
        "title": "Sample Page 1",
        "body": [
            "This is a sample page. The title of this page in the "+indexlink+" dex codebase is 'samplepage1.html'. Pages like <a href='samplepage2.html'>Sample Page 2</a> are currently hyperlinked using human intervention. Automatic search and hyperlink using simple document search will be embedded later.",
            "Strings in the 'body' list of strings in the <a href='jsonintermediate.html'>JSON intermediate</a> document named 'data.json' encode different paragraphs of this page. The JSON intermediate is further explained in the green link above.",
            "Link colors and limited stylistic features of this website may be edited using CSS in the 'styles.css' file in the codebase.",
            "'Favicon.ico' file in the assets folder in this dex codebase is the icon for this website."
        ]
    },
    {
        "title": "Sample Page 2",
        "body": [
            "This is sample page 2 in the dex."
        ]
    },
    {
        "title": "JSON intermediate",
        "body": [
            "A JSON intermediate file named 'data.json' is created in the dex codebase. 'Data.json' is made from raw text, PDF and PPTX files you add to 'raw' folder in the dex codebase. Make document edits in this JSON intermediate. It is the raw data file used as input to generate HTML pages for each item in this list, along with an index page that links to all generated pages."
        ]
    },{
        "title": "Contact",
        "body": [
            "Contact <a href='manonthemoon13131@gmail.com'>manonthemoon13131@gmail.com</a> to manage your dex website.",
            "The Matrix codebase is listed on GitHub <a href='https://github.com/orgs/matrixdex/repositories'>here</a>."
        ]
    },{
        "title": "Hosting",
        "body": ["GitHub allows free hosting through GitHub pages. Simply create a repository in your account and add all files in the dex folder to that repository. Deploy a website using GitHub pages using 'index.html' in the 'dex' folder as entry point."]
    }
    ]
    with open(path+'\\data.json','w+') as file:
        file.write(json.dumps(z, indent=4))

def update_json_data(old_path,updates):
    with open(old_path, 'r') as f:
        z=f.read()
    old=json.loads(z)
    for i in updates:
        old.append(i)
    old=consolidate_json(old)
    with open(old_path, 'w+') as f:
        f.write(json.dumps(old, indent=4))

def get_dexname_from_index_html(html):
    dexname=None
    link=False
    links=[]
    for i in range(len(html)):
        if html[i]=='<':
            if html[i+1]=='a':
                link=True
                links.append('')
            if html[i+1]=='/' and html[i+2]=='a':
                links[-1]+='</a>'
                i=i+3
                link=False
        if link:
            links[-1]+=html[i]
    dexname = links[-1][links[-1].find('>'):links[-1].find('/a')][1:-1]

    return dexname.title()

def save_dexname_in_config(path, dexname):
    config_json = {
        "dexname": dexname,
        "author": "Devpy Bot"
    }
    with open(path+'config.json', 'w+') as file:
        file.write(json.dumps(config_json, indent=4))
def upload(site_folder_path): # add github manager bot
    pass

## CONTROLS

if __name__ == "__main__":
    dexname = None
    root=os.getcwd()+'\\'
    p=['assets', 'backup', 'data.json', 'dev.py', 'dex', 'raw', 'readme.txt', 'styles.css', 'webdex']
    tc=[]
    for i in p:
        if i not in os.listdir(root):
            if i=='assets' or i=='backup' or i=='dex' or i=='raw' or i=='webdex':
                os.mkdir(root+i)
            if i=='assets':
                pass    # assuming website icon exists, can embed into dev.py
            if i=='backup':
                if 'data.json' not in os.listdir(root):
                    print("No dex found. Input name of dex: ", end='')
                    dexname=input()
                    dexname=dexname.title()
                    create_first_json_file(root, dexname)
                    create_first_json_file(root+i, dexname)
                    save_dexname_in_config(root, dexname)
                else:
                    shutil.copy(root+'data.json',root+i)
            if i=='data.json':
                print("No dex found. Input name of dex: ", end='')
                dexname=input()
                dexname=dexname.title()
                create_first_json_file(root, dexname)
                save_dexname_in_config(root, dexname)

    if 'config.json' in os.listdir(root):
        with open(root+'config.json','r') as file:
            t=json.loads(file.read())
        dexname=t['dexname']

    elif 'index.html' in os.listdir(root+'dex\\'):
        with open(root+'dex\\'+'index.html','r') as file:
            dexname=get_dexname_from_index_html(file.read())
        save_dexname_in_config(root, dexname)

    else:
        if 'data.json' in os.listdir(root):
            print('dex root data.json found. dex name not found. input dex name: ', end='')
            dexname = input()
            dexname=dexname.title()
        else:
            dexname='Sample'
        save_dexname_in_config(root, dexname)
    
        
    

    site_folder_path = root+"dex\\"
    json_file = root+'data.json'
    assets_path = root+'assets'
    styles_path = root+'styles.css'
    update_path = root + 'raw\\'

    updates=None
    if len(os.listdir(update_path))!=0:
        if len(os.listdir(update_path))!=1 or os.listdir(update_path)[0]!='clear':
            updates = parse_updates(update_path)
        else:
            updates=None
        
    if 'dummy.json' in os.listdir(root):
        with open(root+'dummy.json','r') as f:
            k=json.loads(f.read())
        if updates == None:
            print('appending dummy.json to data.json')
            shutil.copy(root+'data.json',root+'backup\\')
            print('data.json backed up in backup folder')
            update_json_data(json_file,k)
            print('data.json updated with dummy.json')
            os.remove(root+'dummy.json')  

        else:
            update_json_data(root+'dummy.json',updates)
            print('dummy.json updated with raw text from files in raw folder')
            print("clearing files from raw folder and saving added files into '//raw//clear' folder")
            if 'clear' not in os.listdir(update_path):
                os.mkdir(update_path+'clear')
            for i in os.listdir(update_path):
                if i != 'clear':
                    shutil.move(update_path+i,update_path+'clear')
            print('edit dummy.json and run script again to add dummy.json to data.json')
    else:
        if updates != None:
            with open(root+'dummy.json','w+') as f:
                f.write(json.dumps(updates, indent=4))
            print('dummy.json created from raw text files in raw folder')
            print("clearing files from raw folder and saving added files into '//raw//clear' folder")
            if 'clear' not in os.listdir(update_path):
                os.mkdir(update_path+'clear')
            for i in os.listdir(update_path):
                if i != 'clear':
                    shutil.move(update_path+i,update_path+'clear')
            print('edit dummy.json and run script again to add dummy.json to data.json')

    
    if os.path.exists(json_file):
        pages=json_to_webpages(json_file)
        save_webpages(site_folder_path,assets_path,styles_path,pages)
        print("Webpages created successfully.")
    else:
        print("JSON file does not exist")