import json
import re


# 0705677-72.2019.8.02.0001

def dadosPrincipaisProcesso(html_text):
    dadosPrincipais = {}

    dadosPrincipais['numero_processo'] = re.search(r'<span [^i]*id="numeroProcesso"[^>]*>([^<]*)</span>',
                                                   html_text).group(1).strip()
    dadosPrincipais['classe_processo'] = re.search(r'<(div|span)(.*?)id="classeProcesso"[^>]*>( <span(.*?)>)?([^<]*)</',
                                                   html_text).group(5).strip()

    dadosPrincipais['assunto_processo'] = re.search(
        r'<(div|span)(.*?)id="assuntoProcesso"[^>]*>(\s?<span(.*?)>)?([^<]*)</',
        html_text).group(5).strip()

    dadosPrincipais['area'] = re.search(r'<div(.*?)id="areaProcesso"[^>]*>\s?<span[^>]*>((.|\s)+?)</span>',
                                        html_text).group(2).strip()

    dadosPrincipais['valor_acao'] = re.search(r'<div(.*?)id="valorAcaoProcesso">(<span[^>]*>)?([^<]*)</',
                                              html_text).group(3).strip()

    if re.search(r'Consulta\s?de\s?Processos\s?de\s?1º\s?Grau', html_text):
        dadosPrincipais['foro_processo'] = re.search(r'<span [^i]*id="foroProcesso"[^>]*>([^<]*)</span>',
                                                     html_text).group(
            1).strip()

        dadosPrincipais['vara_processo'] = re.search(r'<span [^i]*id="varaProcesso"[^>]*>([^<]*)</span>',
                                                     html_text).group(
            1).strip()

        dadosPrincipais['juiz_processo'] = re.search(r'<span [^i]*id="juizProcesso"[^>]*>([^<]*)</span>',
                                                     html_text).group(
            1).strip()

        dadosPrincipais['distribuicao'] = re.search(r'<div id="dataHoraDistribuicaoProcesso">((.|\s)+?)</div>',
                                                    html_text).group(1).strip()

        dadosPrincipais['controle'] = re.search(r'<div id="numeroControleProcesso">((.|\s)+?)</div>',
                                                html_text).group(1).strip()

    elif re.search(r'Consulta\s?de\s?Processos\s?de\s?2º\s?Grau', html_text):
        dadosPrincipais['secao'] = re.search(r'<div(.*?)id="secaoProcesso">\s?<span[^>]*>(.*?)</', html_text).group(
            2).strip()
        dadosPrincipais['orgao_julgador'] = re.search(r'<div(.*?)id="orgaoJulgadorProcesso">\s?<span[^>]*>(.*?)</',
                                                      html_text).group(2).strip()
        dadosPrincipais['relatorProcesso'] = re.search(r'<div(.*?)id="relatorProcesso">\s?<span[^>]*>(.*?)</',
                                                       html_text).group(2).strip()
        dadosPrincipais['origem'] = re.search(r'<span[^>]*>Origem</span>\s*(.*?)<span[^>]*>(.*?)</',
                                              html_text).group(2).strip()
        dadosPrincipais['volume/apenso'] = re.search(r'<div(.*?)id="volumeApensoProcesso"><span[^>]*>(.*?)</',
                                                     html_text).group(2).strip()

    else:
        return 'Instância do Processo não encontrada.'

    return dadosPrincipais


def partesProcesso(html_text):
    dadosPartesProcesso = {}
    dadosPartesProcesso['partes'] = []
    autor = ''

    partes = r'<tr class="fundoClaro( polo.{5,7})?"[^>]*>[^<]*<td valign="top" width="141"[^>]*>((.|\s)+?)</tr>'

    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)
        tipoDeParticipacao = re.search(r'<span class="mensagemExibindo tipoDeParticipacao">((.|\s)+?)</span>',
                                       parte_completa).group(1).strip()

        nomeParteEAdvogado = re.search(r'<td(.*?)class="nomeParteEAdvogado"[^>]*>((.|\s)+?)</td>',
                                       parte_completa).group(
            2).strip()

        if 'span' in nomeParteEAdvogado:
            autor = re.search(r'class="nomeParteEAdvogado"(.*?)?>((.|\s)+?)<', parte_completa).group(1).strip()
            span = r'<span class="mensagemExibindo">(.*?)</span>(\s*)?((.|\s)+?)<'
            for span_parte in re.findall(span, nomeParteEAdvogado):
                autor += '\n' + span_parte[0] + f'{span_parte[2]}\n'

            row = {
                'tipo_participacao': tipoDeParticipacao,
                'nome': autor
            }

            if not row in dadosPartesProcesso['partes']:
                dadosPartesProcesso['partes'].append(row)
        else:
            row = {
                'tipo_participacao': tipoDeParticipacao,
                'nome': nomeParteEAdvogado.strip()
            }

            if not row in dadosPartesProcesso['partes']:
                dadosPartesProcesso['partes'].append(row)

    return dadosPartesProcesso


def movimentacoesProcesso(html_text):
    dadosMovimentacoesProcesso = {}
    dadosMovimentacoesProcesso['movimentacoes'] = []

    partes = r'<tr class="fundo.{5,6} (containerMovimentacao|movimentacaoProcesso)"[^>]*>((.|\s)+?)</tr>'
    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)

        data_movimentacao = re.search(
            r'<td(.*?)class="(dataMovimentacao|dataMovimentacaoProcesso)"[^>]*>((.|\s)+?)</td>',
            parte_completa).group(
            3).strip()

        descricao_movimentacao_titulo = re.search(
            r'<td(.*?)class="(descricaoMovimentacao|descricaoMovimentacaoProcesso)"[^>]*>((.|\s)+?)<br(\s)?/>',
            parte_completa)

        descricao_movimentacao_titulo_link = re.search(
            r'<td(.*?)class="(descricaoMovimentacao|descricaoMovimentacaoProcesso)"[^<]*<a class="linkMovVincProc"[^>]*>((.|\s)+?)</a>',
            parte_completa)

        # subdescricao = re.search(r'<td(.*?)?class="(descricaoMovimentacao|descricaoMovimentacaoProcesso)"((.|\s)+?)<span[^>]*>(\s*)?(.*?)(\s*)?</span>',
        #     parte_completa).group(6).strip()

        row = {
            'data': data_movimentacao,
            'descricao': descricao_movimentacao_titulo_link.group(3).strip()
            if descricao_movimentacao_titulo_link
            else descricao_movimentacao_titulo.group(3).strip()
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
