import requests
import os

from pywebio.session import go_app
from pywebio.pin import *
from pywebio import session, config, start_server
from pywebio.input import *
from pywebio.output import *

url = "https://www.dnd5eapi.co/api/spells"
headers = {'Accept' : 'application/json'}
urlInfo = "https://www.dnd5eapi.co"

css = """
#pywebio-scope-direita {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-direita:hover {
    overflow-y: scroll;
}
#pywebio-scope-esquerda {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-esquerda:hover {
    overflow-y: scroll;
}
/* Works on Firefox */
* {
  scrollbar-width: thin;
}
/* Works on Chrome, Edge, and Safari */
*::-webkit-scrollbar {
  width: 7px;
}
*::-webkit-scrollbar-track {
  background: gray;
}
*::-webkit-scrollbar-thumb {
  background-color: gray;
  border-radius: 20px;
  border: 2px
}
"""


def main():
    
    response = requests.get(url, headers = headers)
    check_response(response)



@config(theme="minty", css_style=css)
def novoMenu(spells_data, spells):
    session.set_env(title='spells', output_max_width='100%')
    
    put_row(
        [put_scope('esquerda'), None, put_scope('direita')],
        size="2fr 40px minmax(60%, 6fr)",
    )
    
    with use_scope('esquerda'):
        put_markdown('## Selecione a opção desejada: '),
        put_button(['Listar todas as Spells'], onclick=lambda: primeira_opcao(spells, spells_data)),
        put_button(['Pesquisar por uma Spell'], onclick=lambda:segunda_opcao(spells))


    with use_scope('direita'):
        put_markdown('# Bem-vindo(a) ao livro de Spells de DnD 5e!')
        put_markdown('#### Total de Spells: ' +str(spells_data['count']))
    


def check_response(response): 
    if response.status_code == 200:
        spells_data = response.json()
        spells = spells_data['results']
        # print_menu(spells_data, spells)
        novoMenu(spells_data, spells)



@use_scope('direita', clear=True)
def primeira_opcao(spells, spellData):

    # print(spellData)
    put_markdown("## Lista das Spells:")
    for index, spell in enumerate(spellData['results']):
        put_markdown('### '+ str(index + 1) + ' - ' + str(spell['name']))
            
            
def segunda_opcao(spells):
    with use_scope('direita'):
        spellName = input("Digite a Spell que dejesa procurar: ")
        matching_spells = [spell for spell in spells if spellName in spell['name'].lower()]
        put_markdown("## Spells encontradas:")

        for index, spell in enumerate(matching_spells):
            spellInfo = requests.get(urlInfo+spell['url'], headers = headers).json()
            display_spells_info(index, spellInfo)        


@use_scope('direita', clear=True)
def display_spells_info(index, spellData):
    put_markdown('## ' + str(index + 1) + ' - ' + spellData['name'])
    
    for item in spellData['desc']:
        put_markdown("###     " + item)
        
    put_markdown("###     Duração: " + spellData['duration'])
    put_markdown("###     Tempo para utilizar: " + spellData['casting_time'])

    put_markdown("###     Classes: ")
    for index, classe in enumerate(spellData['classes']):
        put_markdown("###     " + str(index + 1) + ' - ' + classe['name'])
    
    if len(spellData['subclasses']) != 0:
        put_markdown("###     Subclasses: ")
        for index, subclasse in enumerate(spellData['subclasses']):
            put_markdown("###     " + index + ' - ' + subclasse['name'])
    
    
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def print_menu(spells_data, spells):
    print('Welcome to the DnD 5e Spellbook!')
    print('Total de Spells: ', spells_data['count'])
    
    while True:
        print("Comandos:")
        print("1 - Listar todas as Spells.")
        print("2 - Procurar uma Spell por nome.")
        print("3 - Sair.")
        
        choice = input("Digite sua escolha: ")
        
        if choice == '1':
            primeira_opcao(spells)
        elif choice == '2':
            segunda_opcao(spells)