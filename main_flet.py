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

def limpar_duplicados_nome(diretorio_raiz, log_callback):
    arquivos_por_nome = {}
    log_callback(f"🔍 Analisando arquivos em: {diretorio_raiz} (modo nome)...")
    for raiz, pastas, arquivos in os.walk(diretorio_raiz):
        for nome in arquivos:
            # Remove o (1) do nome, se existir
            if nome.endswith(').jpg') or nome.endswith(').png') or nome.endswith(').jpeg'):
                nome_base = nome.replace('(1)', '').replace('  ', ' ')
            else:
                nome_base = nome
            caminho_completo = os.path.join(raiz, nome)
            if nome_base not in arquivos_por_nome:
                arquivos_por_nome[nome_base] = []
            arquivos_por_nome[nome_base].append(caminho_completo)
    log_callback("\n🚀 Iniciando remoção de duplicatas por nome...")
    for nome_base, caminhos in arquivos_por_nome.items():
        if len(caminhos) > 1:
            caminhos.sort(key=lambda x: ("(1)" in os.path.basename(x), len(os.path.basename(x))))
            original = caminhos[0]
            duplicatas = caminhos[1:]
            log_callback(f"\n✅ Mantendo: {os.path.basename(original)}")
            for duplicata in duplicatas:
                try:
                    os.remove(duplicata)
                    log_callback(f"   🗑️  Removido: {os.path.basename(duplicata)}")
                except Exception as e:
                    log_callback(f"   ❌ Erro ao remover {duplicata}: {e}")


def limpar_duplicados_real(diretorio_raiz, log_callback):
    def limpar_duplicados_nome(diretorio_raiz, log_callback):
        # Mapeia nomes base para arquivos
        arquivos_por_nome = {}
        log_callback(f"🔍 Analisando arquivos em: {diretorio_raiz} (modo nome)...")
        for raiz, pastas, arquivos in os.walk(diretorio_raiz):
            for nome in arquivos:
                # Remove o (1) do nome, se existir
                if nome.endswith(').jpg') or nome.endswith(').png') or nome.endswith(').jpeg'):
                    nome_base = nome.replace('(1)', '').replace('  ', ' ')
                else:
                    nome_base = nome
                caminho_completo = os.path.join(raiz, nome)
                if nome_base not in arquivos_por_nome:
                    arquivos_por_nome[nome_base] = []
                arquivos_por_nome[nome_base].append(caminho_completo)
        log_callback("\n🚀 Iniciando remoção de duplicatas por nome...")
        for nome_base, caminhos in arquivos_por_nome.items():
            if len(caminhos) > 1:
                # Mantém o arquivo sem (1) no nome, se existir
                caminhos.sort(key=lambda x: ("(1)" in os.path.basename(x), len(os.path.basename(x))))
                original = caminhos[0]
                duplicatas = caminhos[1:]
                log_callback(f"\n✅ Mantendo: {os.path.basename(original)}")
                for duplicata in duplicatas:
                    try:
                        os.remove(duplicata)
                        log_callback(f"   🗑️  Removido: {os.path.basename(duplicata)}")
                    except Exception as e:
                        log_callback(f"   ❌ Erro ao remover {duplicata}: {e}")
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
    # Detecta se está rodando como desktop
    platform = getattr(page.platform, "value", str(page.platform))
    is_desktop = platform in ["desktop", "windows", "macos", "linux"]
    checkbox_nome = ft.Checkbox(label="Remover duplicatas apenas pelo nome (ignorar (1))", value=False)
    page.title = "Remove Duplicatas - Flet"
    page.window_width = 375  # Largura típica de celular
    page.window_height = 700
    page.window_resizable = True
    # Preenche o campo com o diretório atual do servidor
    caminho_input = ft.TextField(label="Caminho da pasta", value=os.getcwd(), expand=True)
    log_area = ft.TextField(label="Log", multiline=True, read_only=True, expand=True, min_lines=10, max_lines=20)
    running = False

    def log_callback(msg):
        log_area.value += msg + "\n"
        page.update()

    def escolher_caminho(e):
        def on_result(result):
            if hasattr(result, "path") and result.path:
                caminho_input.value = result.path
                page.update()
        if is_desktop:
            if hasattr(page, "get_directory_path"):
                page.get_directory_path(on_result)
            else:
                log_callback("Seleção de diretório não suportada nesta versão do Flet. Digite o caminho manualmente.")
        else:
            log_callback("Seleção de pasta só disponível no modo desktop. Digite o caminho manualmente.")

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
        if checkbox_nome.value:
            limpar_duplicados_nome(caminho, log_callback)
        else:
            limpar_duplicados_real(caminho, log_callback)
        log_callback("\n✨ Limpeza profunda concluída!")
        running = False

    def cancelar(e):
        if hasattr(page, "window_close"):
            page.window_close()
        elif hasattr(page, "window_destroy"):
            page.window_destroy()
        else:
            log_callback("Fechamento automático não suportado nesta versão. Feche a janela manualmente.")

    # Substituir IconButton e icons por um botão de texto simples
    row_widgets = [caminho_input]
    if is_desktop:
        row_widgets.append(ft.ElevatedButton("Selecionar", on_click=escolher_caminho))

    action_buttons = [ft.ElevatedButton("OK", on_click=executar, expand=True)]
    if is_desktop:
        action_buttons.append(ft.ElevatedButton("Cancelar", on_click=cancelar, expand=True))

    page.add(
        ft.Column([
            ft.Row(row_widgets, alignment="start", expand=True),
            checkbox_nome,
            ft.Text(
                "Dica: No modo desktop, clique em 'Selecionar' para escolher a pasta. No modo web, digite ou cole manualmente o caminho.",
                size=12, color="grey"
            ),
            log_area,
            ft.Row(action_buttons, alignment="end", expand=True)
        ], expand=True, horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)
    #ft.app(target=main, view=ft.WEB_BROWSER)