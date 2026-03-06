(# RemoveDuplicatas

Este projeto é um script Python para identificar e remover arquivos duplicados em uma pasta, mantendo apenas uma cópia de cada arquivo único (baseado no conteúdo, não no nome).

## O que o script faz?

- Analisa todos os arquivos em um diretório e subdiretórios.
- Calcula uma assinatura (hash) para cada arquivo, baseada no conteúdo.
- Mantém apenas o arquivo original e remove as cópias duplicadas (mesmo conteúdo, nomes diferentes).
- Exibe no terminal quais arquivos foram mantidos e quais foram removidos.

## Como baixar

1. Clone este repositório ou baixe os arquivos diretamente:
	```bash
	git clone <URL_DO_REPOSITORIO>
	```
	Ou baixe o arquivo `main.py` manualmente.

2. (Opcional) Crie um ambiente virtual Python:
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

## Como usar

1. Edite o arquivo `main.py` e altere a variável `caminho_alvo` para o diretório que deseja analisar/remover duplicatas.

2. Execute o script:
	```bash
	python main.py
	```

3. O script irá mostrar no terminal os arquivos analisados, quais foram mantidos e quais duplicatas foram removidas.

**Atenção:** Faça um backup dos seus arquivos antes de rodar o script, pois os arquivos duplicados serão removidos permanentemente!

---
Projeto simples para automação de limpeza de arquivos duplicados.

---

## Como gerar um executável único (standalone)

Este projeto utiliza o [PyInstaller](https://pyinstaller.org/) para empacotar o script em um único arquivo executável, facilitando a execução em outros sistemas sem precisar instalar Python manualmente.

### 1. Instale as dependências com UV

```bash
uv add pyinstaller
```

### 2. Gere o executável para seu sistema

```bash
.venv/bin/pyinstaller --onefile main.py
```
O executável será criado na pasta `dist/`.

### 3. Executando em outros sistemas operacionais

- **Linux:** O comando acima já gera um executável para Linux.
- **Windows:** Execute o comando em um ambiente Windows (ou use cross-compilation avançada).
- **MacOS:** Execute o comando em um Mac (ou use cross-compilation avançada).

> **Dica:** Para garantir máxima compatibilidade, gere o executável no próprio sistema operacional de destino.

---
**Resumo dos comandos:**

```bash
uv add pyinstaller
.venv/bin/pyinstaller --onefile main.py
```

O executável estará em `dist/main` (Linux/Mac) ou `dist/main.exe` (Windows).

---

## Como gerar um executável da interface gráfica (Flet)

Para empacotar a versão com interface gráfica (main_flet.py) em um executável único:

```bash
uv add pyinstaller
pyinstaller --onefile main_flet.py
```
O executável será criado na pasta `dist/`.

> **Observação:** O executável gerado depende das bibliotecas do Flet Desktop e das dependências do sistema (como libmpv). Veja as instruções acima para garantir o funcionamento.

---

## Versão com interface gráfica (Flet)

Também está disponível uma versão com janela gráfica usando a biblioteca Flet.

### Instale a dependência:
```bash
uv add flet
```

### Execute a interface gráfica:
```bash
python main_flet.py
```

Nela, você pode escolher a pasta, visualizar o log do processo e executar ou cancelar a limpeza de duplicatas.

### Dependências obrigatórias para interface gráfica desktop
Para rodar a interface gráfica como aplicativo de desktop, instale também:
```bash
uv add flet-desktop
uv add flet-web
```
Esses pacotes são necessários para o funcionamento local do Flet.

#### Dependência do sistema (Linux)
Para rodar a interface gráfica desktop no Linux, é necessário instalar a biblioteca nativa libmpv:
Se após instalar o pacote libmpv-dev o Flet Desktop ainda não funcionar, crie um link simbólico para a versão correta da biblioteca:

```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1
sudo ldconfig
```
Esses comandos garantem compatibilidade do Flet Desktop com a biblioteca libmpv.
```bash
sudo apt update
sudo apt install libmpv-dev
```
Sem ela, o Flet Desktop não inicia.
