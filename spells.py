import requests
import os

def display_spells(index, spellData):
    print(index, '-' ,spellData['name'])

def display_spells_info(index, spellData):
    print(index, '-' ,spellData['name'])
    print()    
    for item in spellData['desc']:
        print("     ", item)
        
    print("     Duração: ", spellData['duration'])
    print("     Tempo para utilizar: ", spellData['casting_time'])

    print()    
    print("     Classes: ")
    for index, classe in enumerate(spellData['classes']):
        print("     ", index,'-', classe['name'])
    
    print()
    print("     Subclasses: ")
    for index, subclasse in enumerate(spellData['subclasses']):
        print("     ", index,'-', subclasse['name'])
    
    
def main():
    url = "https://www.dnd5eapi.co/api/spells"
    headers = {'Accept' : 'application/json'}
    urlInfo = "https://www.dnd5eapi.co"
    
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        spells_data = response.json()
        spells = spells_data['results']
        
        print('Welcome to the DnD 5e Spellbook!')
        print('Total de Spells: ', spells_data['count'])
        
        while True:
            print("Comandos:")
            print("1 - Listar todas as Spells.")
            print("2 - Procurar uma Spell por nome.")
            print("3 - Sair.")
            
            choice = input("Digite sua escolha: ")
            
            if choice == '1':
                os.system('clear')
                print("\nLista das Spells:")
                for index, spell in enumerate(spells):
                    display_spells(index, spell)
                input()
                os.system('clear')
                
            elif choice == '2':
                os.system('clear')
                spellName = input("Digite a Spell que dejesa procurar: ")
                matching_spells = [spell for spell in spells if spellName in spell['name'].lower()]
                print("\nSpells encontradas: \n\n")

                for index, spell in enumerate(matching_spells):
                    spellInfo = requests.get(urlInfo+spell['url'], headers = headers).json()
                    display_spells_info(index, spellInfo)
                
                input()    
                os.system('clear')
                
            elif choice == '3':
                os.system('clear')
                print("-------------------------------------------------------------------------")     
                print("A paz do senhor e tchau tchau")
                print("-------------------------------------------------------------------------")     
                break
                
            else:
                print("-------------------------------------------------------------------------")     
                print("\nOpção inválida.")
            
            print("-------------------------------------------------------------------------")     
if __name__ == "__main__":
    main()