import requests
from flask import Flask, render_template,request,redirect,url_for
from googletrans import Translator
from bs4 import BeautifulSoup
app = Flask(__name__)

class Lines:
    def __init__(self,url,text):
        self.url = url
        self.text = text

@app.route('/')
def redirect():
    return redirect(url_for('main'))

@app.route('/main', methods=['get','post'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        translator = Translator()
        translator = Translator(service_urls=['translate.googleapis.com'])
        url = request.form['url']
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        links = []
        other = []
        for link in soup.find_all('a'):
            cur = str(link.get('href'))
            transtaded_text = translator.translate(link.getText(),dest='hi')
            if cur.startswith('http'):
                other.append( Lines(cur[cur.find('://')+3:],transtaded_text.text))
            else:
                links.append(Lines(cur,transtaded_text.text))
        return render_template('links.html',other=other,links=links,current = url[0:len(url)-1])


if __name__ == '__main__':
    app.run(debug=True)