# Usa uma imagem base do Python, que já vem com as ferramentas necessárias
FROM python:3.9-slim

# Instala a dependência do sistema (PortAudio), que o sounddevice precisa
RUN apt-get update && apt-get install -y libportaudio2

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os seus arquivos do projeto para o container
COPY . .

# Instala todas as bibliotecas Python que estão no seu requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando que o Render usará para iniciar sua aplicação
# O caminho completo garante que o gunicorn seja encontrado
CMD ["/usr/local/bin/gunicorn", "app:app"]