import requests
import re
from scrap_web import dadosPrincipaisProcesso, partesProcesso, movimentacoesProcesso

# 0705677-72.2019.8.02.  (0001 = numero Unificado)

"""
https://www2.tjal.jus.br/cpopg/search.do;jsessionid=21EEB739CFE070D504F34C97BEB07F75.cpopg4?conversationId=&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0705677-72.2019&foroNumeroUnificado=0001&dadosConsulta.valorConsultaNuUnificado=0705677-72.2019.8.02.0001&dadosConsulta.valorConsultaNuUnificado=UNIFICADO&dadosConsulta.valorConsulta=&dadosConsulta.tipoNuProcesso=UNIFICADO&uuidCaptcha=


"""
numeroProcesso = '0705677-72.2019.8.02.0001'


def numeroProcessoURL(numeroProcesso):
    regex = re.findall(r"\d+", numeroProcesso)
    numeroDigitoAnoUnificado = f'{regex[0]}-{regex[1]}.{regex[2]}'
    foroNumeroUnificado = regex[-1]
    valorConsultaUnificado = numeroProcesso
    url_concatenada = f"https://www2.tjal.jus.br/cpopg/search.do?conversationId=&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={numeroDigitoAnoUnificado}&foroNumeroUnificado={foroNumeroUnificado}&dadosConsulta.valorConsultaNuUnificado={valorConsultaUnificado}&dadosConsulta.valorConsultaNuUnificado=UNIFICADO&dadosConsulta.valorConsulta=&dadosConsulta.tipoNuProcesso=UNIFICADO&uuidCaptcha="
    dados_processo(url_concatenada)


def dados_processo(url_search):
    request = requests.get(url_search)
    html_text = request.text.replace('&nbsp;', '')
    principais = dadosPrincipaisProcesso(html_text)
    partes = partesProcesso(html_text)
    movimentacoes = movimentacoesProcesso(html_text)
    print(movimentacoes)

numeroProcessoURL(numeroProcesso)
