from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>Proxy Navegador</h2>
    <form action="/go" method="get">
        <input type="text" name="url" placeholder="https://ejemplo.com" size="40">
        <button type="submit">Ir</button>
    </form>
    '''

@app.route('/go')
def go():
    url = request.args.get('url')
    if not url:
        return 'No se proporcionó URL'
    if not url.startswith('http'):
        url = 'http://' + url
    return f'<iframe src="/proxy/{url.replace("://", "/")}" width="100%" height="800"></iframe>'

@app.route('/proxy/<path:url>')
def proxy(url):
    # Reconstruir la URL original
    real_url = url.replace('/', '://', 1)
    try:
        resp = requests.get(real_url)
        return Response(resp.content, content_type=resp.headers.get('Content-Type', 'text/html'))
    except Exception as e:
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True)