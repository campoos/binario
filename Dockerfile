# Usa uma imagem base do Python
FROM python:3.9-slim

# Instala a dependência do sistema: PortAudio
RUN apt-get update && apt-get install -y libportaudio2

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do seu projeto para o container
COPY . .

# Instala as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando para iniciar o servidor
CMD ["/usr/local/bin/gunicorn", "app:app"]