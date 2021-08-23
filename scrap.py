import html
import json
import requests
import re
from scrap_web import dadosPrincipaisProcesso, partesProcesso, movimentacoesProcesso, peticoesProcesso

# 0705677-72.2019.8.02.  (0001 = numero Unificado)

"""
https://www2.tjal.jus.br/cpopg/search.do;jsessionid=21EEB739CFE070D504F34C97BEB07F75.cpopg4?conversationId=&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0705677-72.2019&foroNumeroUnificado=0001&dadosConsulta.valorConsultaNuUnificado=0705677-72.2019.8.02.0001&dadosConsulta.valorConsultaNuUnificado=UNIFICADO&dadosConsulta.valorConsulta=&dadosConsulta.tipoNuProcesso=UNIFICADO&uuidCaptcha=


"""
# numeroProcesso = '0705677-72.2019.8.02.0001'
numeroProcesso = '0705360-45.2017.8.02.0001'
processoDados = {}


def numeroProcessoURL(numeroProcesso):
    regex = re.findall(r"\d+", numeroProcesso)
    numeroDigitoAnoUnificado = f'{regex[0]}-{regex[1]}.{regex[2]}'
    foroNumeroUnificado = regex[-1]
    valorConsultaUnificado = numeroProcesso

    # url_concatenada = f"https://www2.tjal.jus.br/cpopg5/search.do?conversationId=&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={numeroDigitoAnoUnificado}&foroNumeroUnificado={foroNumeroUnificado}&dadosConsulta.valorConsultaNuUnificado={valorConsultaUnificado}&dadosConsulta.valorConsultaNuUnificado=UNIFICADO&dadosConsulta.valorConsulta=&dadosConsulta.tipoNuProcesso=UNIFICADO&uuidCaptcha="

    url_concatenada = f"https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={numeroDigitoAnoUnificado}&foroNumeroUnificado={foroNumeroUnificado}&dePesquisaNuUnificado={numeroProcesso}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"

    dados_processo(url_concatenada)


def dados_processo(url_search):
    request = requests.get(url_search)

    html_text = html.unescape(request.text)

    html_text = html_text.replace('&nbsp;', '')

    principais = dadosPrincipaisProcesso(html_text)
    partes = partesProcesso(html_text)
    movimentacoes = movimentacoesProcesso(html_text)
    # peticoes = peticoesProcesso(html_text)

    processoDados[numeroProcesso] = {}
    processoDados[numeroProcesso]['principais'] = principais
    processoDados[numeroProcesso]['partes_processo'] = partes
    processoDados[numeroProcesso]['movimentacoes_processo'] = movimentacoes
    # processoDados[numeroProcesso]['peticoes_processo'] = peticoes

    with open("unicodeFile.json", "w", encoding='utf-8') as write_file:
        json.dump(processoDados, write_file, ensure_ascii=False)
    print("Done writing JSON serialized Unicode Data as-is into file")


numeroProcessoURL(numeroProcesso)
