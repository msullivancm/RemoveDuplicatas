import os
import hashlib

def calcular_hash(caminho_arquivo, bloco=65536):
    """Cria uma assinatura única baseada no conteúdo do arquivo."""
    hasher = hashlib.md5()
    try:
        with open(caminho_arquivo, 'rb') as f:
            buf = f.read(bloco)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(bloco)
        return hasher.hexdigest()
    except:
        return None

def limpar_duplicados_real(diretorio_raiz):
    # Dicionário para guardar {hash: [lista_de_caminhos]}
    arquivos_por_conteudo = {}

    print(f"🔍 Analisando arquivos em: {diretorio_raiz}...")

    for raiz, pastas, arquivos in os.walk(diretorio_raiz):
        for nome in arquivos:
            caminho_completo = os.path.join(raiz, nome)
            
            # 1. Filtro rápido por tamanho (ignora arquivos vazios)
            tamanho = os.path.getsize(caminho_completo)
            if tamanho == 0: continue

            # 2. Gera o Hash (o "RG" do arquivo)
            assinatura = calcular_hash(caminho_completo)
            if assinatura:
                if assinatura not in arquivos_por_conteudo:
                    arquivos_por_conteudo[assinatura] = []
                arquivos_por_conteudo[assinatura].append(caminho_completo)

    print("\n🚀 Iniciando remoção de duplicatas reais...")

    for assinatura, caminhos in arquivos_por_conteudo.items():
        if len(caminhos) > 1:
            # Ordena por tamanho do nome: o nome mais curto (original) fica primeiro
            # Ex: 'wall.jpg' vem antes de 'wall (1).jpg'
            caminhos.sort(key=lambda x: len(os.path.basename(x)))
            
            original = caminhos[0]
            duplicatas = caminhos[1:]

            print(f"\n✅ Mantendo: {os.path.basename(original)}")
            
            for duplicata in duplicatas:
                try:
                    os.remove(duplicata)
                    print(f"   🗑️  Removido: {os.path.basename(duplicata)}")
                except Exception as e:
                    print(f"   ❌ Erro ao remover {duplicata}: {e}")

if __name__ == "__main__":
    # Ajuste o caminho aqui novamente
    caminho_alvo = "/home/sullivan/Insync/marcus.sullivan@gmail.com/Google Drive/Imagens/wallpapers"
    
    if os.path.exists(caminho_alvo):
        limpar_duplicados_real(caminho_alvo)
        print("\n✨ Limpeza profunda concluída!")
    else:
        print("Caminho inválido.")