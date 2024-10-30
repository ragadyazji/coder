from flask import Flask, render_template, request, redirect, url_for
import random
import string
import json
import base64

app = Flask(__name__)

def create_hashtable():
    letters = string.ascii_lowercase
    shuffled = list(letters)
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def encrypt(text, hashtable):
    return ''.join(hashtable.get(char, char) for char in text.lower())

def decrypt(encrypted_text, hashtable):
    reverse_hashtable = {shuffled: letters for letters, shuffled in hashtable.items()}
    return ''.join(reverse_hashtable.get(char, char) for char in encrypted_text)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        hashtable = create_hashtable()
        encrypted_text = encrypt(text, hashtable)
        hashtable_json = json.dumps(hashtable)
        encoded_hashtable = base64.b64encode(hashtable_json.encode()).decode()
        encoded_encrypted_text = base64.b64encode(encrypted_text.encode()).decode()
        link = url_for('decrypt_message', encrypted_text=encoded_encrypted_text, hashtable=encoded_hashtable, _external=True)
        return render_template('index.html', link=link, encrypted_text=encrypted_text)
    return render_template('index.html')

@app.route('/decrypt')
def decrypt_message():
    encrypted_text = request.args.get('encrypted_text')
    hashtable_json = request.args.get('hashtable')
    return render_template('decrypt.html', encrypted_text=base64.b64decode(encrypted_text).decode(), hashtable=hashtable_json)

@app.route('/manual_decrypt', methods=['POST'])
def manual_decrypt():
    encrypted_text = request.form['reenter_encrypted']
    hashtable_json = request.form['hashtable']
    hashtable = json.loads(base64.b64decode(hashtable_json).decode())
    decrypted_text = decrypt(encrypted_text, hashtable)
    return render_template('decrypt.html', encrypted_text=encrypted_text, hashtable=hashtable_json, decrypted_text=decrypted_text)

if __name__ == '__main__':
    app.run(debug=True)

