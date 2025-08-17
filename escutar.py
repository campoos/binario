import numpy as np
import wave
import struct
import sounddevice as sd

# Parâmetros usados no transmissor
SAMPLE_RATE = 44100
DURACAO_BIT = 0.1
FREQ_0 = 1000
FREQ_1 = 2000

samples_por_bit = int(SAMPLE_RATE * DURACAO_BIT)

def ler_wav(path):
    with wave.open(path, 'rb') as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == SAMPLE_RATE
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)
        audio = np.array(struct.unpack('<' + 'h'*n_frames, frames), dtype=np.float32) / 32768.0
    return audio

def detectar_freq(chunk):
    fft = np.fft.rfft(chunk)
    freqs = np.fft.rfftfreq(len(chunk), 1/SAMPLE_RATE)

    # pega os bins mais próximos das frequências esperadas
    idx0 = np.argmin(np.abs(freqs - FREQ_0))
    idx1 = np.argmin(np.abs(freqs - FREQ_1))

    power0 = np.abs(fft[idx0])
    power1 = np.abs(fft[idx1])

    return FREQ_0 if power0 > power1 else FREQ_1

def audio_para_bits(audio):
    bits = ""
    for i in range(0, len(audio), samples_por_bit):
        chunk = audio[i:i+samples_por_bit]
        if len(chunk) < samples_por_bit:
            break
        freq = detectar_freq(chunk)
        bits += "0" if freq == FREQ_0 else "1"
    return bits

def bits_para_texto(bits):
    texto = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            byte = byte.ljust(8, "0")  # completa com zeros
        texto += chr(int(byte, 2))
    return texto

# --------------------------
# Testando com o WAV gerado
# --------------------------
audio = ler_wav("mensagem_binario.wav")

# 🔊 Tocar o áudio antes de traduzir
print("Tocando o áudio recebido...")
sd.play(audio, SAMPLE_RATE)
sd.wait()  # espera terminar a reprodução

bits = audio_para_bits(audio)
texto_decodificado = bits_para_texto(bits)

print("Bits recebidos:", bits)
print("Texto decodificado:", texto_decodificado)
