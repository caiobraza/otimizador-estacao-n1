# Importa os módulos padrão do Python (não precisa instalar nada com pip)
import os          # Manipula caminhos de pastas, arquivos e variáveis de ambiente
import shutil      # Ajuda a apagar pastas inteiras e consultar espaço em disco
import datetime    # Gera data e hora atuais para o log e relatório do chamado

# Define a letra da unidade principal do sistema (geralmente C:\ no Windows)
UNIDADE_SISTEMA = "C:\\"

# Lista de pastas temporárias seguras para limpeza preventiva em estações Windows
PASTAS_ALVO = [
    os.environ.get("TEMP", ""),          # Pasta temporária do usuário atual (%TEMP%)
    os.path.join(UNIDADE_SISTEMA, "Windows", "Temp"),  # Pasta temporária global do Windows
]


def obter_espaco_livre_gb(unidade: str) -> float:
    """Retorna o espaço livre em disco (em GB) arredondado para 2 casas decimais."""
    # shutil.disk_usage retorna total, used e free em bytes
    _, _, livre_bytes = shutil.disk_usage(unidade)
    # Converte bytes para Gigabytes (1 GB = 1024^3 bytes)
    livre_gb = livre_bytes / (1024 ** 3)
    return round(livre_gb, 2)


def limpar_pasta_temporaria(caminho_pasta: str) -> tuple[int, int, int]:
    """
    Percorre os arquivos e subpastas de um diretório temporário e remove o que for possível.
    Retorna: (arquivos_removidos, itens_ignorados_em_uso, bytes_liberados)
    """
    arquivos_removidos = 0
    itens_ignorados = 0
    bytes_liberados = 0

    # Verifica se o caminho existe e é realmente uma pasta antes de tentar limpar
    if not caminho_pasta or not os.path.isdir(caminho_pasta):
        return arquivos_removidos, itens_ignorados, bytes_liberados

    # os.walk percorre a pasta atual e todas as subpastas dentro dela
    for raiz, dirs, arquivos in os.walk(caminho_pasta, topdown=False):
        # Tenta remover cada arquivo encontrado
        for nome_arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz, nome_arquivo)
            try:
                # Lê o tamanho do arquivo antes de apagar para somar no total liberado
                tamanho = os.path.getsize(caminho_arquivo)
                os.remove(caminho_arquivo)  # Apaga o arquivo
                arquivos_removidos += 1
                bytes_liberados += tamanho
            except (PermissionError, OSError):
                # Se o arquivo estiver em uso por algum programa aberto, o Windows bloqueia.
                # Ignoramos com segurança sem travar o script!
                itens_ignorados += 1

        # Tenta remover subpastas vazias (exceto a pasta raiz principal)
        for nome_dir in dirs:
            caminho_dir = os.path.join(raiz, nome_dir)
            if caminho_dir == caminho_pasta:
                continue
            try:
                os.rmdir(caminho_dir)  # Só remove se a subpasta estiver vazia
            except (PermissionError, OSError):
                itens_ignorados += 1

    return arquivos_removidos, itens_ignorados, bytes_liberados


def gerar_relatorio_atendimento(
    hostname: str,
    espaco_antes: float,
    espaco_depois: float,
    total_arquivos: int,
    total_ignorados: int,
    total_mb_liberados: float,
    detalhes_pastas: list[str],
) -> str:
    """Monta um relatório técnico pronto para anexar no encerramento do chamado N1."""
    ganho_gb = round(espaco_depois - espaco_antes, 2)
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Monta o texto estruturado do relatório
    linhas = [
        "=" * 60,
        "RELATÓRIO DE MANUTENÇÃO PREVENTIVA - SUPORTE N1",
        "=" * 60,
        f"Data/Hora execução : {agora}",
        f"Estação (Hostname) : {hostname}",
        f"Espaço livre antes : {espaco_antes} GB",
        f"Espaço livre depois: {espaco_depois} GB",
        f"Variação líquida   : {ganho_gb:+.2f} GB",
        f"Arquivos removidos : {total_arquivos}",
        f"Itens em uso/pulados: {total_ignorados}",
        f"Volume temporário  : {total_mb_liberados} MB",
        "-" * 60,
        "Detalhes por pasta:",
    ]
    linhas.extend(detalhes_pastas)
    linhas.append("=" * 60)

    conteudo = "\n".join(linhas)

    # Garante que a pasta de relatórios exista
    os.makedirs("relatorios", exist_ok=True)
    nome_arquivo = f"relatorio_{hostname}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    caminho_relatorio = os.path.join("relatorios", nome_arquivo)

    # Salva o relatório em UTF-8 para não quebrar acentos
    with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

    return caminho_relatorio


def executar_otimizacao() -> None:
    """Fluxo principal da rotina de limpeza e geração de evidência."""
    hostname = os.environ.get("COMPUTERNAME", "ESTACAO-WINDOWS")
    print(f"\n=== Iniciando Otimizador de Estação N1 ({hostname}) ===\n")

    # 1. Mede o espaço livre antes da limpeza
    espaco_antes = obter_espaco_livre_gb(UNIDADE_SISTEMA)
    print(f"Espaço livre antes da limpeza: {espaco_antes} GB")

    total_arquivos = 0
    total_ignorados = 0
    total_bytes = 0
    detalhes_pastas = []

    # 2. Executa a limpeza em cada pasta alvo
    for pasta in PASTAS_ALVO:
        removidos, ignorados, bytes_lib = limpar_pasta_temporaria(pasta)
        mb_lib = round(bytes_lib / (1024 ** 2), 2)

        total_arquivos += removidos
        total_ignorados += ignorados
        total_bytes += bytes_lib

        linha_detalhe = (
            f"  - {pasta}: {removidos} removidos, {ignorados} em uso ({mb_lib} MB)"
        )
        detalhes_pastas.append(linha_detalhe)
        print(linha_detalhe)

    # 3. Mede o espaço livre após a limpeza
    espaco_depois = obter_espaco_livre_gb(UNIDADE_SISTEMA)
    total_mb_liberados = round(total_bytes / (1024 ** 2), 2)

    print(f"\nEspaço livre após a limpeza: {espaco_depois} GB")
    print(f"Total de arquivos removidos: {total_arquivos}")
    print(f"Total em arquivos temporários liberado: {total_mb_liberados} MB")

    # 4. Gera o arquivo de evidência para o chamado
    caminho_relatorio = gerar_relatorio_atendimento(
        hostname=hostname,
        espaco_antes=espaco_antes,
        espaco_depois=espaco_depois,
        total_arquivos=total_arquivos,
        total_ignorados=total_ignorados,
        total_mb_liberados=total_mb_liberados,
        detalhes_pastas=detalhes_pastas,
    )
    print(f"\nRelatório salvo em: {caminho_relatorio}\n")


# Ponto de entrada padrão: só roda se o arquivo for executado diretamente
if __name__ == "__main__":
    executar_otimizacao()