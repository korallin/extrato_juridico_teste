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

    # for id_principal in (
    # "numeroProcesso", "classeProcesso", "assuntoProcesso", "foroProcesso", "varaProcesso", "juizProcesso"):
    #     regex = re.search(rf'(<span id="{id_principal}"[^>]*>)(\s*.*)(\s*<\/span>)', html_text)
    #     if rege
    #     print(regex.group(2).strip())

    return dadosPrincipais


def partesProcesso(html_text):
    dadosPartesProcesso = {}

    dadosPartesProcesso['autor'] = re.search(
        r'<td class="nomeParteEAdvogado"[^>]*>([^<]*)<[^<]*<span class="mensagemExibindo">([^<]*)</span>([^<]*)',
        html_text).groups()
    print(dadosPartesProcesso)
