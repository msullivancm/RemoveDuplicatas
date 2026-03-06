import flet as ft
import os
import hashlib

def calcular_hash(caminho_arquivo, bloco=65536):
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

def limpar_duplicados_real(diretorio_raiz, log_callback):
    arquivos_por_conteudo = {}
    log_callback(f"🔍 Analisando arquivos em: {diretorio_raiz}...")
    for raiz, pastas, arquivos in os.walk(diretorio_raiz):
        for nome in arquivos:
            caminho_completo = os.path.join(raiz, nome)
            tamanho = os.path.getsize(caminho_completo)
            if tamanho == 0:
                continue
            assinatura = calcular_hash(caminho_completo)
            if assinatura:
                if assinatura not in arquivos_por_conteudo:
                    arquivos_por_conteudo[assinatura] = []
                arquivos_por_conteudo[assinatura].append(caminho_completo)
    log_callback("\n🚀 Iniciando remoção de duplicatas reais...")
    for assinatura, caminhos in arquivos_por_conteudo.items():
        if len(caminhos) > 1:
            caminhos.sort(key=lambda x: len(os.path.basename(x)))
            original = caminhos[0]
            duplicatas = caminhos[1:]
            log_callback(f"\n✅ Mantendo: {os.path.basename(original)}")
            for duplicata in duplicatas:
                try:
                    os.remove(duplicata)
                    log_callback(f"   🗑️  Removido: {os.path.basename(duplicata)}")
                except Exception as e:
                    log_callback(f"   ❌ Erro ao remover {duplicata}: {e}")

def main(page: ft.Page):
    page.title = "Remove Duplicatas - Flet"
    page.window_width = 600
    page.window_height = 500
    # Preenche o campo com o diretório atual do servidor
    caminho_input = ft.TextField(label="Caminho da pasta", width=400, value=os.getcwd())
    log_area = ft.TextField(label="Log", multiline=True, read_only=True, width=580, height=300)
    running = False

    def log_callback(msg):
        log_area.value += msg + "\n"
        page.update()

    def escolher_caminho(e):
        def on_result(result):
            if hasattr(result, "path") and result.path:
                caminho_input.value = result.path
                page.update()
        # Flet web não suporta diálogo nativo, então use um campo de texto manual
        try:
            page.get_directory_path(on_result)
        except Exception:
            log_callback("Seleção de pasta não suportada neste modo. Digite o caminho manualmente.")

    def executar(e):
        nonlocal running
        if running:
            return
        running = True
        log_area.value = ""
        page.update()
        caminho = caminho_input.value.strip()
        if not caminho or not os.path.exists(caminho):
            log_callback("Caminho inválido.")
            running = False
            return
        limpar_duplicados_real(caminho, log_callback)
        log_callback("\n✨ Limpeza profunda concluída!")
        running = False

    def cancelar(e):
        page.window_close()

    # Substituir IconButton e icons por um botão de texto simples
    page.add(
        ft.Row([
            caminho_input
        ], alignment="start"),
        ft.Text("Dica: No modo web, digite ou cole manualmente o caminho da pasta desejada. O caminho exibido é o diretório atual do servidor.", size=12, color="grey"),
        log_area,
        ft.Row([
            ft.ElevatedButton("OK", on_click=executar),
            ft.ElevatedButton("Cancelar", on_click=cancelar)
        ], alignment="end")
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
