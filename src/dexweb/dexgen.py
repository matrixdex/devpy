import pypdf
import os, json, shutil, importlib_resources, mammoth
from bs4 import BeautifulSoup

class Dexgen:
    def __init__(self):
        self.dexname = None
        self.index_template=None
        self.page_template=None
        self.config_javascript=None
        self.index_list_type_para=False
        self.index_list_no_page_link_only = True
        root=os.getcwd()
        self.init_dex(root)
      
        self.site_folder_path = os.path.join(root, 'gen')
        self.json_file = os.path.join(root,'data.json')
        self.new_json_file = os.path.join(root, 'data2.json')
        self.assets_path = os.path.join(root, 'gen', 'assets')
        self.styles_path = os.path.join(root, 'styles.css')
        self.update_path = os.path.join(root,'to_add')
      
        updates=None
        files_to_add=False
        if os.path.exists(self.update_path) and len(os.listdir(self.update_path))!=0:
            for i in os.listdir(self.update_path):
                if i!='clear' and not i.startswith('.'):
                    files_to_add=True
            if files_to_add:
                updates = self.parse_updates(self.json_file, self.update_path)
            else:
                updates=None
            
        if 'dummy.json' in os.listdir(root):
            with open(os.path.join(root,'dummy.json'),'r') as f:
                k=json.loads(f.read())
            if updates == None:
                print('appending dummy.json to data.json')
                shutil.copy(os.path.join(root,'data.json'),os.path.join(root,'backup'))
                print('data.json backed up in backup folder')
                self.update_json_data(self.json_file,k)
                print('data.json updated with dummy.json')
                os.remove(os.path.join(root,'dummy.json'))  

            else:
                self.update_json_data(os.path.join(root,'dummy.json'),updates)
                print('dummy.json updated with text from files in /to_add folder')
                print("clearing files from /to_add folder and saving added files into '/to_add/clear' folder")
                if 'clear' not in os.listdir(self.update_path):
                    os.mkdir(os.path.join(self.update_path,'clear'))
                for i in os.listdir(self.update_path):
                    if i != 'clear' and not i.startswith('.'):
                        shutil.move(os.path.join(self.update_path,i),os.path.join(self.update_path,'clear'))
                print('edit dummy.json and run script again to add dummy.json to data.json')
        else:
            if updates != None:
                with open(os.path.join(root,'dummy.json'),'w+') as f:
                    f.write(json.dumps(updates, indent=4))
                print('dummy.json created from files in /to_add folder')
                print("clearing files from /to_add folder and saving added files into '/to_add/clear' folder")
                if 'clear' not in os.listdir(self.update_path):
                    os.mkdir(os.path.join(self.update_path,'clear'))
                for i in os.listdir(self.update_path):
                    if i != 'clear' and not i.startswith('.'):
                        shutil.move(os.path.join(self.update_path,i),os.path.join(self.update_path,'clear'))
                print('edit dummy.json and run script again to add dummy.json to data.json')

        
        if os.path.exists(self.json_file):
            pages=self.json_to_webpages(self.json_file)
            self.save_webpages(self.site_folder_path,self.assets_path,self.styles_path,pages)
            print("Webpages created successfully.")
        else:
            print("JSON file does not exist")

    def init_dex(self, root):

        p=['backup', 'data.json', 'dev.py', 'gen', 'readme.txt', 'styles.css', 'to_add']
        for i in p:
            if i not in os.listdir(root):
                if i=='assets' or i=='backup' or i=='gen' or i=='to_add':
                    os.mkdir(os.path.join(root, i))
                    if i=='gen':
                        os.mkdir(os.path.join(root,i,'assets'))
                        favicon = importlib_resources.read_binary('dexweb', 'favicon.ico')
                        with open(os.path.join(root,i,'assets','favicon.ico'), "wb+") as file:
                            file.write(favicon)
                if i=='backup':
                    if 'data.json' not in os.listdir(root):
                        print("No dex found. Input name of dex: ", end='')
                        dexname=input()
                        self.dexname=dexname.title()
                        self.create_first_json_file(root, self.dexname)
                        self.create_first_json_file(os.path.join(root,i), self.dexname)
                        if 'config.json' not in os.listdir(root):
                            self.save_dexname_in_config(root, self.dexname)
                    else:
                        shutil.copy(os.path.join(root,'data.json'),os.path.join(root,i))
                if i=='data.json':
                    print("No dex found. Input name of dex: ", end='')
                    dexname=input()
                    self.dexname=dexname.title()
                    self.create_first_json_file(root, self.dexname)
                    self.save_dexname_in_config(root, self.dexname)
                if i=='styles.css':
                    styles_text = importlib_resources.files("dexweb").joinpath("styles.css").read_text()
                    with open(os.path.join(root,"styles.css"), "w+") as file:
                        file.write(styles_text)

        if 'config.json' in os.listdir(root):
            t=self.get_config()
            self.dexname=t['dexname']
            self.index_template=t['index_template']
            self.page_template=t['page_template']
            self.index_list_type_para=t['index_list_type_para']
            self.index_list_no_page_link_only = t['index_list_no_page_link_only']
            if "index_javascript" in t.keys() and len(t["index_javascript"])>2:
                if self.config_javascript == None:
                    self.config_javascript={"index_javascript": t["index_javascript"]}
                else:
                    self.config_javascript["index_javascript"]=t["index_javascript"]
            if "page_javascript" in t.keys() and len(t["page_javascript"])>2:
                if self.config_javascript == None:
                    self.config_javascript={"page_javascript": t["page_javascript"]}
                else:
                    self.config_javascript["page_javascript"]=t["page_javascript"]

        elif 'index.html' in os.listdir(os.path.join(root,'gen')):
            with open(os.path.join(root,'gen','index.html'),'r') as file:
                self.dexname=self.get_dexname_from_index_html(file.read())
            self.save_dexname_in_config(root, self.dexname)

        else:
            if 'data.json' in os.listdir(root):
                print('dex root data.json found. dex name not found. input dex name: ', end='')
                dexname = input()
                self.dexname=dexname.title()
            else:
                self.dexname='Sample'
            self.save_dexname_in_config(root, self.dexname)

    def create_indexpage(self,pages):
        k=''
        if self.index_list_type_para == False:
            for i in range(len(pages)):
                if self.index_list_no_page_link_only == True:
                    if len(pages[i]['full_body']) == 1 and pages[i]['full_body'][0][0:2]=='<a' and pages[i]['full_body'][0][-4:] == "</a>":
                        q=pages[i]['full_body'][0]
                        k+="<div class='indexlink'><a href='"+q[q.index('=')+2:q.index('>')-1]+"'>"+pages[i]['title']+'</a><br></div>'
                    else:
                        k+="<div class='indexlink'><a href="+pages[i]['html_title']+".html>"+pages[i]['title']+'</a><br></div>'
                else:
                    k+="<div class='indexlink'><a href="+pages[i]['html_title']+".html>"+pages[i]['title']+'</a><br></div>'
        else:
            for i in range(len(pages)):
                b=pages[i]['body']
                c=pages[i]['full_body']
                if self.index_list_no_page_link_only == True:
                    if len(c) == 1 and c[0][0:2]=='<a' and c[0][-4:] == "</a>":
                        q=c[0]
                        k+="<div class='indexlink'><p><a href='"+q[q.index('=')+2:q.index('>')-1]+"'>"+pages[i]['title']+'</a> ('+q[q.index('>')+1:q.index('</a>')]+')</p></div>'
                    else:
                         k+="<div class='indexlink'><p><a href="+pages[i]['html_title']+".html>"+pages[i]['title']+'</a>'+' ('+b+')'+'</p></div>'
                else:
                    k+="<div class='indexlink'><p><a href="+pages[i]['html_title']+".html>"+pages[i]['title']+'</a>'+' ('+b+')'+'</p></div>'
        if self.index_template == None:
            self.index_template=self.get_config("index_template")
        template = self.index_template.format(self.dexname,self.dexname.upper(),k,self.dexname.upper())
        if self.config_javascript != None and "index_javascript" in self.config_javascript.keys() and len(self.config_javascript["index_javascript"])>2:
            p = str(template.split('</head>')[0]) + str(self.config_javascript['index_javascript']) + '</head>' + str(template.split('</head>')[1])
            template = p
        return template

    def create_webpage(self, title, body):
        k=''
        for i in body:
            k+='<p>'+i+'</p>'
        if self.page_template == None:
            self.page_template=self.get_config("page_template")
        template = self.page_template.format(title,self.dexname,title.upper(),k,self.dexname.upper())
        
        return template

    def save_webpages(self,site_folder_path,assets_path,styles_path,pages):
        if 'assets' not in os.listdir(site_folder_path):
            os.mkdir(os.path.join(site_folder_path,'assets'))
        # for i in os.listdir(assets_path):
        #     shutil.copy(os.path.join(assets_path,i),os.path.join(site_folder_path,"assets"))
        shutil.copy(styles_path,site_folder_path)
        for i in pages:
            with open(os.path.join(site_folder_path,i['html_title']+'.html'), "w+", encoding="utf-8") as file:
                file.write(i['page'])

    def json_to_webpages(self,json_file):
        with open(json_file, 'r') as f:
            z=f.read()
        p=json.loads(z)
        titles=[]
        pages=[]
        for i in range(len(p)):
            t2="".join(x for x in p[i]['title'] if x.isalnum())
            t2=t2.lower()
            page=self.create_webpage(p[i]['title'], p[i]['body'])
            if len(p[i]['body'])>0:
                pages.append({'title':p[i]['title'], 'page':page, 'html_title': t2, 'body':p[i]['body'][0], 'full_body': p[i]['body']})

        pages = sorted(pages, key=lambda x: x['title'])
        pages.append({'title':f'{self.dexname} Dex', 'page':self.create_indexpage(pages) , 'html_title': 'index'})
        return pages

    # deprecated
    def pdf_to_json_by_page(self,pdf_file):
        pdf_reader = pypdf.PdfReader(pdf_file)
        data=[] # list of pages if this was new dex
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            text = page.extract_text()
            lines = text.split("\n")
            body = lines[1:]  # Rest of the lines form the body
            title=lines[0]
            data.append({'title':title, 'body':body})
        return data

    def pdf_to_json(self,pdf_file):
        pdf_reader = pypdf.PdfReader(pdf_file)
        data={} # list of pages if this was new dex
        if pdf_reader.metadata.title != None:
            title_flag=True
            data['title']=pdf_reader.metadata.title
        else:
            title_flag=False
        body=[]
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            text = page.extract_text()
            lines = text.split("\n")
            body[len(body):len(body)]=lines
        data['body']=body
        if not title_flag:
            data['title']=body[0]
        return data

    def txt_to_json(self,txt_path):
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

    def get_html_filenames(self,folder_path):
        filenames=os.listdir(folder_path)
        f=[]
        for i in filenames:
            if len(i)>=5 and i[-5]=='.' and i[-4]=='h' and i[-3]=='t' and i[-2]=='m' and i[-1]=='l':
                f.append(i)
        filenames=f
        return filenames

    def html_to_json(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        page={}
        if soup.title == None:
            for i in soup.children:
                if i.name =='p' and len(i.text)>2 and 'date' not in str(i.text).lower():
                    page['title']=i.text
                    break
        else:
            page["title"]=soup.title
        body=[]
        for i in soup.children:
            if i.name =='p':
                body.append(str(i.text))
            if i.name == 'ul':
                li=i.find_all('li')
                b=''
                for j in li:
                    if j!=None and len(j.text)>2:
                        b+=str(j.text)+'<br>'
                b=b[:-4]
                body.append(b)
            if i.name == 'ol':
                body.append(str(i))
            if i.name == 'table':
                body.append(str(i))  
        page["body"]=body
        page=json.dumps(page)
        return page

    #deprecated
    def html_files_to_json(self,site_folder_path):
        data=[]
        raw_html_files=[]
        html_files=self.get_html_filenames(site_folder_path)
        for file in html_files:
            with open(os.path.join(site_folder_path,file), 'r', encoding="utf8") as f:
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

    def docx_to_json(self, docpath):
        with open(docpath, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
            messages = result.messages
        p=json.loads(self.html_to_json(html))
        return p

    def consolidate_json(self,json_data):
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

    def parse_updates(self,old_path,update_path):
        update_files = os.listdir(update_path)
        update_files = [f for f in update_files if os.path.isfile(os.path.join(update_path,f))]
        p=[]
        for i in update_files:
            p.append({'format': str(i[i.find('.')+1:]), 'file_path': str(os.path.join(update_path,i))})
        
        updates = p
        updates_json = []
        for i in updates:
            if i['format']=='pdf':
                pdf_obj=self.pdf_to_json(i['file_path'])
                updates_json.append(pdf_obj)
            elif i['format']=='txt':
                updates_json.append(self.txt_to_json(i['file_path']))
            elif i['format']=='docx':
                updates_json.append(self.docx_to_json(i['file_path']))
            elif i['format']=='json':
                with open(i['file_path'], 'r') as f:
                    z=f.read()
                p=json.loads(z)
                for j in p:
                    updates_json.append(j)
        updates_json=self.consolidate_json(updates_json)

        with open(old_path, 'r') as f:
            z=f.read()
        old=json.loads(z)
        for i in updates_json:
            old.append(i)
        old=self.consolidate_json(old)
        return old

    def create_first_json_file(self, path, dexname):
        indexlink='''<a href="index.html">'''+dexname+'''</a>'''
        z=[
        {
            "title": "Sample Page 1",
            "body": [
                "This is a sample page. This page is named 'samplepage1.html' in the "+indexlink+" Dex and found in /gen folder. Pages like <a href='samplepage2.html'>Sample Page 2</a> are hyperlinked using human intervention. Automatic search and hyperlink using simple document search will be embedded later.",
                "Each string in 'body' object of 'data.json', also called <a href='jsonintermediate.html'>JSON intermediate</a>, is a paragraph. JSON intermediate is further explained in the link above.",
                "Link colors and limited stylistic features of this website can be edited in'styles.css' file in the codebase.",
                "'Favicon.ico' file in /assets folder in codebase is the icon for this website."
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
                "JSON intermediate file named 'data.json' is created in the dex codebase. 'Data.json' is constructed with raw text, PDF and PPTX files added to '/raw' folder in the dex codebase. Make document edits in this JSON intermediate. This raw data file is used as input to generate HTML pages for each item in this list, along with an index page that links to all generated pages."
            ]
        },
        {
            "title": "Contact",
            "body": [
                "Contact <a href='manonthemoon13131@gmail.com'>manonthemoon13131@gmail.com</a> to manage your dex website.",
                "The Matrix codebase is listed on GitHub <a href='https://github.com/orgs/matrixdex/repositories'>here</a>."
            ]
        },
        {
            "title": "Hosting",
            "body": ["GitHub allows free hosting through GitHub pages. Simply create a repository in your account and add all files in the dex folder to that repository. Deploy a website using GitHub pages using 'index.html' in the 'dex' folder as entry point."]
        }
        ]
        with open(os.path.join(path,'data.json'),'w+') as file:
            file.write(json.dumps(z, indent=4))

    def update_json_data(self,old_path,updates):
        with open(old_path, 'r') as f:
            z=f.read()
        old=json.loads(z)
        for i in updates:
            old.append(i)
        old=self.consolidate_json(old)
        with open(old_path, 'w+') as f:
            f.write(json.dumps(old, indent=4))

    def get_dexname_from_index_html(self,html):
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

    def save_dexname_in_config(self, path, dexname):
        config_json = {
                "dexname": self.dexname,
                "author": "Dexgen",
                "index_template": """<html lang='en'>
                        <head>
                            <meta charset='UTF-8'>
                            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                            <link rel='shortcut icon' type='image/x-icon' href='assets/favicon.ico'>
                            <link rel='stylesheet' href='styles.css'>
                            <title>{} Dex</title>
                        </head>
                        <body>
                            <br><h1>{} DEX</h1><br>
                            {}
                            <br><br><br><br><br><br><br>
                            <h3><a href='index.html'>{} DEX</a></h3>
                        </body>
                        </html>""",
                "page_template": """<html lang='en'>
                        <head>
                            <meta charset='UTF-8'>
                            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                            <link rel='shortcut icon' type='image/x-icon' href='assets/favicon.ico'>
                            <link rel='stylesheet' href='styles.css'>
                            <title>{} - {} Dex</title>
                        </head>
                        <body>
                        <br>
                        <h1>{}</h1>
                        <br>
                        {}
                        <br><br><br><br><br><br><br>
                        <h3><a href='index.html'>{} DEX</a></h3>
                    </body>
                    </html>""",
                    "page_javascript": "",
                    "index_javascript": "",
                    "index_list_type_para": False,
                    "index_list_no_page_link_only": True
            }
        with open(os.path.join(path,'config.json'), 'w+') as file:
            file.write(json.dumps(config_json, indent=4))

    def get_config(self, var=None):
        with open(os.path.join(os.getcwd(),'config.json'),'r') as file:
            t=json.loads(file.read())
        if var==None:
            return t
        else:
            return t[var]
    # TODO
    def upload(self, site_folder_path): # add github manager bot
        pass
