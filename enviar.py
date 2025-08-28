import numpy as np
import wave
import struct
import simpleaudio as sa
# ----------------------------
# Configurações globais
# ----------------------------
SAMPLE_RATE = 44100
DURACAO_BIT = 0.1
FREQ_0 = 1000
FREQ_1 = 2000
ARQUIVO_SAIDA = "mensagem_binario.wav"

def texto_para_binario(texto: str) -> str:
    """Converte string em sequência de bits (ASCII, 8 bits por caractere)."""
    return ''.join(format(ord(c), '08b') for c in texto)

def binario_para_audio(bits: str) -> np.ndarray:
    """Converte string de bits em onda de áudio normalizada [-1, 1]."""
    amostras = []
    for bit in bits:
        freq = FREQ_1 if bit == '1' else FREQ_0
        t = np.linspace(0, DURACAO_BIT, int(SAMPLE_RATE * DURACAO_BIT), endpoint=False)
        onda = np.sin(2 * np.pi * freq * t)
        amostras.extend(onda)
    audio = np.array(amostras)
    return audio / np.max(np.abs(audio))

def salvar_wav(audio: np.ndarray, filename: str = ARQUIVO_SAIDA):
    """Salva o áudio como arquivo WAV mono 16-bit."""
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        for amostra in audio:
            f.writeframes(struct.pack('<h', int(amostra * 32767)))

def tocar_audio(audio: np.ndarray):
    """Reproduz áudio gerado diretamente em PCM."""
    audio_pcm = (audio * 32767).astype(np.int16)
    play_obj = sa.play_buffer(audio_pcm, 1, 2, SAMPLE_RATE)
    play_obj.wait_done()

if __name__ == "__main__":
    texto = input("Digite sua mensagem: ")
    print("Gerando áudio criptografado...")
    bits = texto_para_binario(texto)
    audio = binario_para_audio(bits)
    salvar_wav(audio)
    print(f"Mensagem '{texto}' convertida em áudio ({ARQUIVO_SAIDA})")
    tocar_audio(audio)