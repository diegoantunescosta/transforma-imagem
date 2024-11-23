# Usar uma imagem base do Python
FROM python:3.10-slim

# Configurar o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos necessários para o contêiner
COPY app.py .
COPY requirements.txt .
COPY fundo_padrao.png .
COPY tarja_avatar.png ./tarja_avatar.png

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["python", "app.py"]
