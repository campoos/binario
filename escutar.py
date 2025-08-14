import numpy as np
import wave
import struct

# Parâmetros usados no transmissor
SAMPLE_RATE = 44100
DURACAO_BIT = 0.1
FREQ_0 = 1000
FREQ_1 = 2000

def ler_wav(path):
    with wave.open(path, 'rb') as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == SAMPLE_RATE
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)
        # Converte para array numpy [-1.0, 1.0]
        audio = np.array(struct.unpack('<' + 'h'*n_frames, frames), dtype=np.float32) / 32768.0
    return audio

def detectar_freq(chunk):
    # FFT para detectar frequência dominante
    fft = np.fft.rfft(chunk)
    freqs = np.fft.rfftfreq(len(chunk), 1/SAMPLE_RATE)
    idx = np.argmax(np.abs(fft))
    return freqs[idx]

def audio_para_bits(audio):
    samples_por_bit = int(SAMPLE_RATE * DURACAO_BIT)
    bits = ""
    for i in range(0, len(audio), samples_por_bit):
        chunk = audio[i:i+samples_por_bit]
        if len(chunk) < samples_por_bit:
            break
        freq = detectar_freq(chunk)
        # Decide se é 0 ou 1
        if abs(freq - FREQ_0) < abs(freq - FREQ_1):
            bits += "0"
        else:
            bits += "1"
    return bits

def bits_para_texto(bits):
    texto = ""
    # Quebra em grupos de 8 bits
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            continue
        texto += chr(int(byte, 2))
    return texto

# --------------------------
# Testando com o WAV gerado
# --------------------------
audio = ler_wav("mensagem_binario.wav")
bits = audio_para_bits(audio)
texto_decodificado = bits_para_texto(bits)

print("Bits recebidos:", bits)
print("Texto decodificado:", texto_decodificado)
