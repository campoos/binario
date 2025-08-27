import numpy as np
import wave
import struct

# -----------------------
# Parâmetros do transmissor
# -----------------------
SAMPLE_RATE = 44100
DURACAO_BIT = 0.1
FREQ_0 = 1000
FREQ_1 = 2000

samples_por_bit = int(SAMPLE_RATE * DURACAO_BIT)

# Marcadores
MARCADOR_INICIO = "11111111"
MARCADOR_FIM = "00000000"

# -----------------------
# Funções
# -----------------------
def ler_wav(path):
    """Lê um arquivo WAV mono e retorna os samples normalizados."""
    with wave.open(path, 'rb') as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == SAMPLE_RATE
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)
        audio = np.array(struct.unpack('<' + 'h'*n_frames, frames), dtype=np.float32) / 32768.0
    return audio

def detectar_freq(chunk):
    """Detecta se o chunk de áudio corresponde a FREQ_0 ou FREQ_1."""
    fft = np.fft.rfft(chunk)
    freqs = np.fft.rfftfreq(len(chunk), 1/SAMPLE_RATE)

    idx0 = np.argmin(np.abs(freqs - FREQ_0))
    idx1 = np.argmin(np.abs(freqs - FREQ_1))

    power0 = np.abs(fft[idx0])
    power1 = np.abs(fft[idx1])

    return FREQ_0 if power0 > power1 else FREQ_1

def audio_para_bits(audio):
    """Converte o áudio em uma sequência de bits."""
    bits = ""
    for i in range(0, len(audio), samples_por_bit):
        chunk = audio[i:i+samples_por_bit]
        if len(chunk) < samples_por_bit:
            break
        freq = detectar_freq(chunk)
        bits += "0" if freq == FREQ_0 else "1"
    return bits

def extrair_bits_validos(bits):
    """Extrai apenas os bits entre os marcadores de início e fim."""
    start = bits.find(MARCADOR_INICIO)
    end = bits.find(MARCADOR_FIM, start + len(MARCADOR_INICIO))
    if start != -1 and end != -1:
        return bits[start + len(MARCADOR_INICIO):end]
    else:
        return bits  # se não achar marcadores, retorna tudo

def bits_para_texto(bits):
    """Converte uma string de bits em texto ASCII."""
    texto = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            byte = byte.ljust(8, "0")
        texto += chr(int(byte, 2))
    return texto

# -----------------------
# Função principal
# -----------------------
def main():
    audio = ler_wav("mensagem_binario.wav")
    bits = audio_para_bits(audio)
    bits_validos = extrair_bits_validos(bits)
    texto_decodificado = bits_para_texto(bits_validos)

    print("Bits recebidos:", bits)
    print("Bits válidos:", bits_validos)
    print("Texto decodificado:", texto_decodificado)

# -----------------------
# Executa o programa
# -----------------------
if __name__ == "__main__":
    main()
