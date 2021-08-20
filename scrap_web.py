import json
import re


# 0705677-72.2019.8.02.0001

def dadosPrincipaisProcesso(html_text):
    dadosPrincipais = {}

    dadosPrincipais['numero_processo_regex'] = re.search(r'<span id="numeroProcesso"[^>]*>([^<]*)</span>',
                                                         html_text).group(1).strip()
    dadosPrincipais['classe_processo_regex'] = re.search(r'<span id="classeProcesso"[^>]*>([^<]*)</span>',
                                                         html_text).group(1).strip()
    dadosPrincipais['assunto_processo_regex'] = re.search(r'<span id="assuntoProcesso"[^>]*>([^<]*)</span>',
                                                          html_text).group(1).strip()
    dadosPrincipais['foro_processo_regex'] = re.search(r'<span id="foroProcesso"[^>]*>([^<]*)</span>', html_text).group(
        1).strip()
    dadosPrincipais['vara_processo_regex'] = re.search(r'<span id="varaProcesso"[^>]*>([^<]*)</span>', html_text).group(
        1).strip()
    dadosPrincipais['juiz_processo_regex'] = re.search(r'<span id="juizProcesso"[^>]*>([^<]*)</span>', html_text).group(
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
    confrontante = []
    terceiros = []
    # html_text = html_text.replace('&nbsp;', '')

    partes = r'<tr class="fundoClaro"[^>]*>[^<]*<td valign="top"[^>]*>((.|\s)+?)(\<\/tr\>)'
    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)

        autor = re.search(
            r'<td class="nomeParteEAdvogado"[^>]*>([^<]*)<[^<]*<span class="mensagemExibindo">([^<]*)</span>([^<]*)',
            parte_completa)
        autora = re.search(r'Autora</span>[\s</\w>]+<td class="nomeParteEAdvogado"[^>]*>((.|\s)+?)</td>',
                           parte_completa)
        pessoa_re = re.search(r'Ré</span>[\s</\w>]+<td class="nomeParteEAdvogado"[^>]*>((.|\s)+?)</td>', parte_completa)

        confrontan = re.search(r'Confrontan</span>[\s</\w>]+<td class="nomeParteEAdvogado"[^>]*>((.|\s)+?)</td>',
                               parte_completa)
        terceiro_i = re.search(r'Terceiro I</span>[\s</\w>]+<td class="nomeParteEAdvogado"[^>]*>((.|\s)+?)</td>',
                               parte_completa)

        if confrontan:
            pessoa_confrontan = confrontan.group(1).strip().title()
            if not pessoa_confrontan in confrontante:
                confrontante.append(pessoa_confrontan)

        if terceiro_i:
            pessoa_terceiro_i = terceiro_i.group(1).strip().title()
            if not pessoa_terceiro_i in terceiros:
                terceiros.append(pessoa_terceiro_i)

        if pessoa_re:
            dadosPartesProcesso['re'] = pessoa_re.group(1).strip()

        if autora:
            dadosPartesProcesso['autora'] = autora.group(1).strip()

        if autor:
            autor = autor.groups()
            dadosPartesProcesso['autor'] = autor[0].strip() + '\n' + autor[1].strip() + f' {autor[2].strip()}'

    # tipo_re = re.search()
    dadosPartesProcesso['confrontante'] = confrontante
    dadosPartesProcesso['terceiros'] = terceiros

    return dadosPartesProcesso


def movimentacoesProcesso(html_text):
    dadosMovimentacoesProcesso = {}

    partes = r'<tr class="fundo.{5,6} containerMovimentacao"[^>]*>((.|\s)+?)</tr>'
    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)
        data_movimentacao = re.search(r'<td class="dataMovimentacao"[^>]*>((.|\s)+?)</td>', parte_completa).group(
            1).strip().replace('/', '')

        descricao_movimentacao_titulo = re.search(r'<td class="descricaoMovimentacao"[^>]*>((.|\s)+?)<br />',
                                                  parte_completa)

        descricao_movimentacao_titulo_link = re.search(
            r'<td class="descricaoMovimentacao"[^<]*<a class="linkMovVincProc"[^>]*>((.|\s)+?)</a>',
            parte_completa)

        subdescricao = re.search(r'<td class="descricaoMovimentacao"[^>]*>(.|\s)+?<span[^>]*>(('
                                 r'.|\s)+?)</span>', parte_completa).group(2).strip()

        dadosMovimentacoesProcesso[data_movimentacao] = {}

        dadosMovimentacoesProcesso[data_movimentacao]['descricao_movimentacao'] = \
            descricao_movimentacao_titulo_link.group(1).strip()\
            if descricao_movimentacao_titulo_link else descricao_movimentacao_titulo.group(1).strip()

        dadosMovimentacoesProcesso[data_movimentacao]['subdescricao'] = subdescricao

    # return json.dumps(dadosMovimentacoesProcesso)
    return dadosMovimentacoesProcesso


def peticoesProcesso(html_text):
    dadosPeticoesProcesso = {}
    # \t<tr class="fundo.{5,6}">[\s\t]*<td[^>]*>((.|\s)+?)</td>
    partes = r'\t<tr class="fundo.{5,6}">((.|\s)+?)</tr>'
    for parte in re.findall(partes, html_text):
        parte_completa = ' '.join(parte)
        data_peticao = re.search(r'\t<td width="140"[^>]*>((.|\s)+?)</td>', parte_completa).group(1).strip()
        tipo_peticao = re.search(r'\t<td width="\*"[^>]*>((.|\s)+?)</td>', parte_completa).group(1).strip()

        dadosPeticoesProcesso[data_peticao] = {}
        dadosPeticoesProcesso[data_peticao]['tipo'] = tipo_peticao

    return dadosPeticoesProcesso