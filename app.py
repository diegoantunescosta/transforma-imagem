from PIL import Image, ImageDraw, ImageFont
import io
from rembg import remove

def adicionar_faixa_com_nome(
    imagem_principal_path, novo_fundo_path, imagem_adicional_path, output_path
):
    # Carregar imagem principal
    with open(imagem_principal_path, "rb") as f:
        imagem_principal = f.read()

    # Remover fundo da imagem
    imagem_sem_fundo = remove(imagem_principal)
    imagem_sem_fundo = Image.open(io.BytesIO(imagem_sem_fundo)).convert("RGBA")

    # Carregar e redimensionar o novo fundo
    novo_fundo = Image.open(novo_fundo_path).convert("RGBA")
    novo_fundo = novo_fundo.resize(imagem_sem_fundo.size)

    # Combinar imagem sem fundo com o novo fundo
    resultado = Image.alpha_composite(novo_fundo, imagem_sem_fundo)

    # Carregar a imagem adicional
    imagem_adicional = Image.open(imagem_adicional_path).convert("RGBA")

    # Redimensionar a imagem adicional para caber na largura do resultado
    largura_resultado, altura_resultado = resultado.size
    largura_adicional = largura_resultado
    proporcao = largura_adicional / imagem_adicional.width
    altura_adicional = int(imagem_adicional.height * proporcao)
    imagem_adicional = imagem_adicional.resize((largura_adicional, altura_adicional))

    # Criar uma nova imagem para o resultado final com espaço para a imagem adicional
    altura_total = altura_resultado + altura_adicional
    imagem_final = Image.new("RGBA", (largura_resultado, altura_total), (255, 255, 255, 0))

    # Colocar o resultado no topo e a imagem adicional na parte inferior
    imagem_final.paste(resultado, (0, 0))
    imagem_final.paste(imagem_adicional, (0, altura_resultado), imagem_adicional)

    # Salvar o resultado final
    imagem_final.save(output_path, format="PNG")
    print(f"Imagem salva em: {output_path}")


# Exemplo de uso
adicionar_faixa_com_nome(
    imagem_principal_path="processed_avatar.jpg",
    novo_fundo_path="fundo_padrao.png",
    imagem_adicional_path="tarja avatar.png",  # Caminho da imagem a ser adicionada
    output_path="imagem_resultante_final.png",
)
