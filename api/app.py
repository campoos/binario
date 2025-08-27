from flask import Flask, request, send_file, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename

# importa funções de envio
from enviar import texto_para_binario, binario_para_audio, salvar_wav
# importa funções de escuta
from escutar import ler_wav, audio_para_bits, extrair_bits_validos, bits_para_texto

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/enviar", methods=["POST"])
def enviar():
    mensagem = request.form["mensagem"]
    bits = texto_para_binario(mensagem)
    audio = binario_para_audio(bits)
    filename = os.path.join(UPLOAD_FOLDER, "mensagem.wav")
    salvar_wav(audio, filename)
    
    # Retorna um JSON com a URL do áudio e os bits
    return {
        "audio_url": url_for('get_audio', filename="mensagem.wav"),
        "bits": bits
    }

@app.route("/audio/<filename>")
def get_audio(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/receber", methods=["POST"])
def receber():
    arquivo = request.files["arquivo"]
    path = os.path.join(UPLOAD_FOLDER, secure_filename(arquivo.filename))
    arquivo.save(path)

    audio = ler_wav(path)
    bits = audio_para_bits(audio)
    bits_validos = extrair_bits_validos(bits)
    texto = bits_para_texto(bits_validos)

    # Retorna um JSON com o texto e os bits
    return {"texto": texto, "bits": bits}

if __name__ == "__main__":
    app.run(debug=True, port=5500)