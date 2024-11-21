import requests

# URL da API Flask
url = "http://127.0.0.1:5000/alterarimagem"

# Caminho para o arquivo de imagem
caminho_imagem = "processed_avatar.jpg"

# Enviar a imagem para a API
with open(caminho_imagem, "rb") as imagem:
    files = {"imagem_principal": imagem}
    response = requests.post(url, files=files)

# Verificar o status da resposta
if response.status_code == 200:
    # Salvar a imagem retornada pela API
    with open("imagem_resultante.png", "wb") as arquivo_saida:
        arquivo_saida.write(response.content)
    print("Imagem processada salva como 'imagem_resultante.png'")
else:
    # Exibir mensagem de erro da API
    print(f"Erro: {response.status_code} - {response.text}")
