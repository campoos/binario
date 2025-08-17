import numpy as np
import wave
import struct
import simpleaudio as sa

# -----------------------
# 1. Texto para binário
# -----------------------

textoDigitado = input("digite sua mensagem: ")
texto = textoDigitado
binario = ' '.join(format(ord(c), '08b') for c in texto)
print("Texto original:", texto)
print("Em binário:", binario)
print("Processando áudio...")

# -----------------------
# 2. Binário para áudio
# -----------------------
SAMPLE_RATE = 44100  # Hz
DURACAO_BIT = 0.1    # segundos por bit (0.1s => 10 bits/segundo)
FREQ_0 = 1000        # Hz para o bit 0
FREQ_1 = 2000        # Hz para o bit 1

# Remove os espaços da string binária
bits_puros = binario.replace(" ", "")

# Lista para armazenar as amostras
amostras = []

for bit in bits_puros:
    freq = FREQ_1 if bit == '1' else FREQ_0
    t = np.linspace(0, DURACAO_BIT, int(SAMPLE_RATE * DURACAO_BIT), endpoint=False)
    onda = np.sin(2 * np.pi * freq * t)
    amostras.extend(onda)

# Converte para numpy array e normaliza
audio = np.array(amostras)
audio = audio / np.max(np.abs(audio))  # normaliza para [-1, 1]

# -----------------------
# 3. Salva em WAV
# -----------------------
with wave.open("mensagem_binario.wav", 'w') as f:
    f.setnchannels(1)  # mono
    f.setsampwidth(2)  # 16 bits
    f.setframerate(SAMPLE_RATE)
    for amostra in audio:
        f.writeframes(struct.pack('<h', int(amostra * 32767)))

print("Áudio gerado: mensagem_binario.wav")

# -----------------------
# 4. Toca o áudio
# -----------------------
# Converte para 16-bit PCM
audio_pcm = (audio * 32767).astype(np.int16)
# Reproduz com simpleaudio
play_obj = sa.play_buffer(audio_pcm, 1, 2, SAMPLE_RATE)
play_obj.wait_done()  # espera o áudio terminar