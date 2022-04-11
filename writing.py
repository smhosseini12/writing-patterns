from flask import Flask , render_template,request
from Myutility import findinalltext,Text2WordList,pdf2txt,remove_nonsense_line,find
import webbrowser
import os, sys
from pathlib import Path
import json


if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(sys.executable)
else:
    current_path = os.path.dirname(__file__)
current_path = (current_path.replace("\\", "/")+"/").replace('//','/')

Dir=f'{current_path}DB'


if Path(current_path+'Config.json').is_file():
    with open(current_path+'Config.json') as json_file:
        config = json.load(json_file)
        
else:
    config={
            "pdf_path": "",
    }
    with open(current_path+'Config.json', 'w') as f:
        json.dump(config, f)

pdf_path=(config['pdf_path']+'/').replace('\\','/').replace('//','/')


app = Flask(__name__,
        static_folder=os.path.join(current_path, 'static'),
        template_folder=os.path.join(current_path, 'templates'))

@app.route("/")
def init():

    ListDict={}
    return render_template('index.html', ListDict=ListDict)

@app.route("/",methods=['POST'])
def Main():
    text = request.form['fname']
    if not text.startswith('@ref:'):
        WordList=Text2WordList(text)
        ListDict=findinalltext(WordList,Dir)
        return render_template('index.html', text=text ,ListDict=ListDict)
    else:
        filename=text.replace('@ref:','')
        file_path=find(filename,pdf_path)
        path = f'{file_path}.pdf'
        webbrowser.open_new_tab(path)
        return ('', 204)

if len(sys.argv)==2:
    if sys.argv[1]=='pdf2text':
        pdf_path=pdf_path
        try:
            pdf2txt(pdf_path,Dir)
            remove_nonsense_line(Dir)
        except Exception as e:
            print(e)


if __name__ == "__main__" and len(sys.argv)==1:
    app.run(debug=False)
