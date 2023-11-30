import argparse
import json
import pickle
import time

FILENAME = "../notices/notices.pickle"

with open(FILENAME, 'rb') as f:
    notices = json.loads(pickle.load(f))


def filter_notices(notices, terms, ano, modalidade, numero, situacao):
    filtered_notices = []
    for notice in notices:
        if any(term.lower() in notice['title'].lower() for term in terms):
            if ano and notice['ano'] != ano:
                continue
            if modalidade and notice['modalidade'].lower() != modalidade.lower():
                continue
            if numero and notice['numero'] != numero:
                continue
            if situacao and notice['situacao'] != situacao:
                continue
            filtered_notices.append(notice)
    return filtered_notices


parser = argparse.ArgumentParser()
parser.add_argument("-ano", "--ano", help="ano")
parser.add_argument("-modalidade", "--modalidade", help="modalidade")
parser.add_argument("-numero", "--numero", help="numero")
parser.add_argument("-situacao", "--situacao", help="situacao")
parser.add_argument("terms", nargs="*", help="termos de busca")
args = parser.parse_args()

ano = args.ano
modalidade = args.modalidade
numero = args.numero
situacao = args.situacao
terms = args.terms


startTime = time.time()

print(f"Termo de busca: \"{' '.join(terms)}\"")
if (ano or modalidade or numero or situacao):
    print("Filtros:")
    if (ano):
        print(f"  ano: {ano}")
    if (modalidade):
        print(f"  modalidade: {modalidade}")
    if (numero):
        print(f"  numero: {numero}")
    if (situacao):
        print(f"  situacao: {situacao}")

filtered_notices = filter_notices(
    notices, terms, ano, modalidade, numero, situacao)

endTime = time.time()
responseTime = (endTime - startTime) * 1000
print(f"Tempo de resposta: {responseTime:.2f}ms\n")

print(f"{len(filtered_notices)} resultados")

if (len(filtered_notices)):
    print("------------")
    for notice in filtered_notices:
        print(f"{notice['title']}\nLink: {notice['pdfLink']}\n")
