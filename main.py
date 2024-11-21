from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
from rembg import remove

app = Flask(__name__)

@app.route('/alteraimagem', methods=['POST'])
def adicionar_faixa_com_nome():
    # Verificar se os arquivos necessários foram enviados
    if 'imagem_principal' not in request.files or 'novo_fundo' not in request.files or 'imagem_adicional' not in request.files:
        return jsonify({"error": "Faltam arquivos obrigatórios (imagem_principal, novo_fundo ou imagem_adicional)"}), 400

    try:
        # Carregar os arquivos enviados
        imagem_principal = request.files['imagem_principal'].read()
        novo_fundo = request.files['novo_fundo']
        imagem_adicional = request.files['imagem_adicional']

        # Remover fundo da imagem principal
        imagem_sem_fundo = remove(imagem_principal)
        imagem_sem_fundo = Image.open(io.BytesIO(imagem_sem_fundo)).convert("RGBA")

        # Carregar e redimensionar o novo fundo
        novo_fundo_imagem = Image.open(novo_fundo).convert("RGBA")
        novo_fundo_imagem = novo_fundo_imagem.resize(imagem_sem_fundo.size)

        # Combinar imagem sem fundo com o novo fundo
        resultado = Image.alpha_composite(novo_fundo_imagem, imagem_sem_fundo)

        # Carregar a imagem adicional
        imagem_adicional_imagem = Image.open(imagem_adicional).convert("RGBA")

        # Redimensionar a imagem adicional para caber na largura do resultado
        largura_resultado, altura_resultado = resultado.size
        largura_adicional = largura_resultado
        proporcao = largura_adicional / imagem_adicional_imagem.width
        altura_adicional = int(imagem_adicional_imagem.height * proporcao)
        imagem_adicional_imagem = imagem_adicional_imagem.resize((largura_adicional, altura_adicional))

        # Criar uma nova imagem para o resultado final com espaço para a imagem adicional
        altura_total = altura_resultado + altura_adicional
        imagem_final = Image.new("RGBA", (largura_resultado, altura_total), (255, 255, 255, 0))

        # Posicionar o resultado no topo e a imagem adicional na parte inferior
        imagem_final.paste(resultado, (0, 0))
        imagem_final.paste(imagem_adicional_imagem, (0, altura_resultado), imagem_adicional_imagem)

        # Salvar o resultado em memória
        output = io.BytesIO()
        imagem_final.save(output, format="PNG")
        output.seek(0)

        # Retornar a imagem resultante
        return send_file(output, mimetype='image/png', as_attachment=True, download_name="imagem_resultante.png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
