import json
import re


# 0705677-72.2019.8.02.0001

def dadosPrincipaisProcesso(html_text):
    dadosPrincipais = {}

    dadosPrincipais['numero_processo'] = re.search(r'<span [^i]*id="numeroProcesso"[^>]*>([^<]*)</span>',
                                                   html_text).group(1).strip()
    dadosPrincipais['classe_processo'] = re.search(r'<(div|span)(.*?)id="classeProcesso"[^>]*>( <span(.*?)>)?([^<]*)</',
                                                   html_text).group(5).strip()
    # <(div|span)(.*?)id="classeProcesso"[^>]*>
    dadosPrincipais['assunto_processo'] = re.search(r'<span [^i]*id="assuntoProcesso"[^>]*>([^<]*)</span>',
                                                    html_text).group(1).strip()
    dadosPrincipais['foro_processo'] = re.search(r'<span [^i]*id="foroProcesso"[^>]*>([^<]*)</span>', html_text).group(
        1).strip()
    dadosPrincipais['vara_processo'] = re.search(r'<span [^i]*id="varaProcesso"[^>]*>([^<]*)</span>', html_text).group(
        1).strip()
    dadosPrincipais['juiz_processo'] = re.search(r'<span [^i]*id="juizProcesso"[^>]*>([^<]*)</span>', html_text).group(
        1).strip()
    dadosPrincipais['distribuicao'] = re.search(r'<div id="dataHoraDistribuicaoProcesso">((.|\s)+?)</div>',
                                                html_text).group(1).strip()
    dadosPrincipais['controle'] = re.search(r'<div id="numeroControleProcesso">((.|\s)+?)</div>',
                                            html_text).group(1).strip()
    dadosPrincipais['area'] = re.search(r'<div id="areaProcesso"[^>]*>\s?<span[^>]*>((.|\s)+?)</span>',
                                        html_text).group(1).strip()
    dadosPrincipais['valor_acao'] = re.search(r'<div id="valorAcaoProcesso">((.|\s)+?)</div>',
                                              html_text).group(1).strip()

    # for id_principal in (
    # "numeroProcesso", "classeProcesso", "assuntoProcesso", "foroProcesso", "varaProcesso", "juizProcesso"):
    #     regex = re.search(rf'(<span id="{id_principal}"[^>]*>)(\s*.*)(\s*<\/span>)', html_text)
    #     if rege
    #     print(regex.group(2).strip())

    return dadosPrincipais


def partesProcesso(html_text):
    dadosPartesProcesso = {}
    dadosPartesProcesso['partes'] = []
    confrontante = []
    terceiros = []
    # html_text = html_text.replace('&nbsp;', '')

    partes = r'<tr class="fundoClaro"[^>]*>[^<]*<td valign="top"[^>]*>((.|\s)+?)(\<\/tr\>)'
    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)
        tipoDeParticipacao = re.search(r'<span class="mensagemExibindo tipoDeParticipacao">((.|\s)+?)</span>',
                                       parte_completa).group(1).strip()
        nomeParteEAdvogado = re.search(r'<td class="nomeParteEAdvogado"[^>]*>((.|\s)+?)</td>', parte_completa).group(
            1).strip()

        if 'span' in nomeParteEAdvogado:

            autor = re.search(r'<td class="nomeParteEAdvogado"[^>]*>((.|\s)+?)<br />', parte_completa).group(1).strip()
            row = {
                'nome': autor,
                'tipo_participacao': tipoDeParticipacao
            }

            if not row in dadosPartesProcesso['partes']:
                dadosPartesProcesso['partes'].append(row)

            nomeParteEAdvogado += '<end>'

            advogado = re.search(r'<span class="mensagemExibindo">((.|\s)+?)</span>((.|\s)+?)<end>',
                                 nomeParteEAdvogado).groups()
            nomeParteEAdvogado = advogado[0].strip() + ' ' + advogado[2].strip()
            tipoDeParticipacao = 'Advogado'

        row = {
            'nome': nomeParteEAdvogado.strip(),
            'tipo_participacao': tipoDeParticipacao
        }

        if not row in dadosPartesProcesso['partes']:
            dadosPartesProcesso['partes'].append(row)

    return dadosPartesProcesso


def movimentacoesProcesso(html_text):
    dadosMovimentacoesProcesso = {}
    dadosMovimentacoesProcesso['movimentacoes'] = []

    partes = r'<tr class="fundo.{5,6} containerMovimentacao"[^>]*>((.|\s)+?)</tr>'
    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)

        data_movimentacao = re.search(r'<td class="dataMovimentacao"[^>]*>((.|\s)+?)</td>', parte_completa).group(
            1).strip()

        descricao_movimentacao_titulo = re.search(r'<td class="descricaoMovimentacao"[^>]*>((.|\s)+?)<br />',
                                                  parte_completa)

        descricao_movimentacao_titulo_link = re.search(
            r'<td class="descricaoMovimentacao"[^<]*<a class="linkMovVincProc"[^>]*>((.|\s)+?)</a>',
            parte_completa)

        subdescricao = re.search(r'<td class="descricaoMovimentacao"[^>]*>(.|\s)+?<span[^>]*>(('
                                 r'.|\s)+?)</span>', parte_completa).group(2).strip()

        row = {
            'data': data_movimentacao,
            'descricao': descricao_movimentacao_titulo_link.group(1).strip() + f' {subdescricao}'
            if descricao_movimentacao_titulo_link
            else descricao_movimentacao_titulo.group(1).strip() + f' {subdescricao}'
        }

        dadosMovimentacoesProcesso['movimentacoes'].append(row)

    return dadosMovimentacoesProcesso


def peticoesProcesso(html_text):
    dadosPeticoesProcesso = {}
    dadosPeticoesProcesso['peticoes'] = []

    partes = r'\t<tr class="fundo.{5,6}">((.|\s)+?)</tr>'
    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)
        data_peticao = re.search(r'\t<td width="140"[^>]*>((.|\s)+?)</td>', parte_completa).group(1).strip()
        tipo_peticao = re.search(r'\t<td width="\*"[^>]*>((.|\s)+?)<br/>', parte_completa).group(1).strip()

        row = {
            'data_peticao': data_peticao,
            'tipo_peticao': tipo_peticao
        }

        dadosPeticoesProcesso['peticoes'].append(row)

    return dadosPeticoesProcesso
