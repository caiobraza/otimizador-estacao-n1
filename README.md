# Otimizador de Estação Windows — Automação Suporte N1

Ferramenta CLI em Python voltada para a rotina de **Suporte Técnico / Help Desk N1**, automatizando a limpeza preventiva de diretórios temporários seguros em estações Windows, medindo o espaço em disco antes e depois da execução e gerando um relatório técnico para registro e encerramento de chamados.

## Vídeo Explicativo 



https://github.com/user-attachments/assets/df4027ed-e38b-4208-a54b-c00d2fcf09a1




## Problema Resolvido

Na rotina de atendimento N1, chamados relacionados a lentidão ou falta de espaço em disco costumam exigir verificações repetitivas e limpeza manual de arquivos temporários em estações de trabalho. Este script padroniza a execução e gera evidência objetiva do atendimento em segundos.

## Funcionalidades

- **Medição de Disco:** consulta o espaço livre em GB na unidade `C:\` antes e depois da limpeza.
- **Limpeza Segura de Temporários:** percorre diretórios temporários (`%TEMP%` e `C:\Windows\Temp`), removendo arquivos e subpastas vazias sem interromper o script quando algum item estiver em uso pelo sistema ou por aplicativos abertos.
- **Relatório de Evidência:** salva automaticamente um arquivo `.txt` na pasta `relatorios/` com data/hora, *hostname*, espaço antes/depois, quantidade de arquivos removidos e volume liberado.

## Tecnologias Utilizadas

- **Python** (módulos nativos `os`, `shutil` e `datetime` — sem dependências externas)
- **Git & GitHub** para versionamento

## Como Executar

1. Clone o repositório e acesse a pasta do projeto:
   ```bash
   git clone [https://github.com/caiobraza/otimizador-estacao-n1.git](https://github.com/caiobraza/otimizador-estacao-n1.git)
   cd otimizador-estacao-n1
