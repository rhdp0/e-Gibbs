# e-Gibbs v.1.0
# Desenvolvedor: Rafael Henrique Dias Pereira

import PySimpleGUI as sg

sg.theme('LightBrown13')

class TelaPython:
    def __init__(self):
        #Layout
        layout = [
            [sg.Text('Arquivo',size=(8,0)),sg.Input(size=(30,0),key='nome'),sg.FileBrowse()],

            [   
                sg.Text('Número de Moléculas',size=(8,0)),
                sg.Input(size=(7,0),key='nmol'),
                sg.InputOptionMenu((
                '298', '200', '210', '220', '230', '240', '250', '260', '270', '280', '290', '300', '310', '320', '330', '340', '350', '360', '370', '380', '390', '400'),key='Temperatura'),
                sg.Text('°K')
            ],

            [sg.Text('Molécula',size=(8,0)),sg.Input(size=(30,0),key='mol'),sg.InputOptionMenu(('Reagente', 'Produto'),key='P-R')],
            [sg.Button('Inserir'),sg.Button('Calcular'),sg.Button('Reiniciar')],
            [sg.Text('Molécula',size=(10,0)),sg.Text('Entalpia em kJ/mol',size=(17,0)),sg.Text('Entropia em  kJ/ K/mol',size=(20,0))],
            [sg.Output(size=(100,20),key = '_output_')]
        ]

        #Janela
        self.janela = sg.Window("e-Gibbs v.1.0").layout(layout)

    def iniciar(self):
        produto = [] #Receberá valores do produto
        reagente = [] #Receberá valores do reagente

        while True:
            self.button, self.values = self.janela.Read()

            mol = self.values['mol'].upper()
            nmol = int(self.values['nmol'])
            temperatura = self.values['Temperatura']

            tempList = ['298', '200', '210', '220', '230', '240', '250', '260', '270', '280', '290', '300', '310', '320', '330', '340', '350', '360', '370', '380', '390', '400']
            temp = tempValue(tempList, temperatura)

            result = openArchive(self.values['nome'], temp)
            deltaH = float(result[1]) * 4.18 #ΔH * 4.18
            deltaS = (float(result[4])/1000) * 4.18 #(ΔS/1000) * 4.18

            #Reinicia os valores para novos cálculos
            if self.button == 'Reiniciar':
                produto = []
                reagente = []
                self.janela['_output_'].update('')

            
            formProdutoEnta = []
            formReagenteEnta = []
            formProdutoEntr = []
            formReagenteEntr = []
            #Ação ao clicar no botão Calcular
            if self.button == 'Calcular':
                if len(produto) > 1:
                    for i in range(len(produto)-1):
                        formProdutoEnta = (produto[i][1]*produto[i][2]) + produto[i+1][1]*produto[i+1][2] #n*KCAL/MOL + KCAL/MOL entalpia
                        formProdutoEntr = (produto[i][1]*produto[i][3]) + produto[i+1][1]*produto[i+1][3] #n*CAL/K/MOL + CAL/K/MOL entropia
                else:
                        formProdutoEnta = produto[0][1]*produto[0][2] #n*KCAL/MOL
                        formProdutoEntr = produto[0][1]*produto[0][3] #n*CAL/K/MOL

                if len(reagente) > 1:
                    for i in range(len(reagente)-1):
                        formReagenteEnta = (reagente[i][1]*reagente[i][2]) + reagente[i+1][1]*reagente[i+1][2] #n*KCAL/MOL + KCAL/MOL entalpia
                        formReagenteEntr = (reagente[i][1]*reagente[i][3]) + reagente[i+1][1]*reagente[i+1][3] #n*CAL/K/MOL + CAL/K/MOL entropia
                else:
                    formReagenteEnta = reagente[0][1]*reagente[0][2] #n*KCAL/MOL
                    formReagenteEntr = reagente[0][1]*reagente[0][3] #n*CAL/K/MOL
                
                entalpia = float(formProdutoEnta) - float(formReagenteEnta) #(Soma dos produtos - soma dos reagentes)
                entropia = float(formProdutoEntr) - float(formReagenteEntr) #(Soma dos produtos - soma dos reagentes)
                deltaG = entalpia - (int(temperatura)*entropia) #Temperatura * entropia
                termoEntropico = -int(temperatura)*(float('%.5f'%entropia)) # -(Temperatura) * entropia

                print('')
                print ('ΔrH: ', '%.5f'%entalpia,'kJ/mol\n')
                print ('ΔrS: ', '%.5f'%entropia,'kJ/mol', ' '*5, 'Termo Entrópico: ','%.5f'%termoEntropico,'kJ/mol\n')
                print ('ΔG: ', '%.5f'%deltaG,'kJ/mol')
                print("__"*50)
                

            #Evento ao clicar no botão Inserir
            if self.button == 'Inserir':
                if self.values['P-R'] == 'Produto':
                    produto.append([mol, nmol, deltaH, deltaS])
                    print('')
                    print(mol, ' '*(21 - len(mol)), '%.5f'%deltaH, ' '*28, '%.5f'%deltaS, ' '*30, 'Produto')
                    print('__'*50)
                else:
                    reagente.append([mol, nmol, deltaH, deltaS, 'Reagente'])
                    print('')
                    print(mol, ' '*(21 - len(mol)), '%.5f'%deltaH, ' '*28, '%.5f'%deltaS, ' '*30, 'Reagente')
                    print('__'*50)
                
                


def openArchive(string, temp):
    arquivo = open(string, 'r') #Abre o arquivo .out
    text = [] #Vai armazenar todo o conteúdo do arquivo

    #Adiciona o conteúdo do arquivo na variável text
    for line in arquivo:
        text.append(line)

    #Descobrir quantos átomos tem a molécula
    listAtm = [] #Vai conter a linha exata onde é informado o último átomo
    stringAtm = ''
    #Identifica a linha exata onde é informado o último átomo
    for i in text[len(text) - 13]: 
        if i in '-1234567890.':
            stringAtm += i
        else:
            listAtm.append(stringAtm)
            stringAtm = ''
    
    #Captura a str que diz o número de átomos e transforma em int
    cont = 0
    nAtm = ''
    while cont < 7 and nAtm == '':
        if listAtm[cont] == '':
            cont += 1
        else:
            nAtm = int(listAtm[cont])


#   Pega o ΔH e o ΔS da molécula a 298°
    listAux = []
    string = ''
    for i in text[len(text) - nAtm - 159 + (temp*6)]:
        if i in '-1234567890.':
            string += i
        else:
            listAux.append(string)
            string =''

    #Elimina as str vazias
    listMaster = []
    for i in listAux:
        if i != '':
            listMaster.append(i)

    arquivo.close()
    return listMaster

def tempValue(lista, valor):
    for i in range(len(lista)):
        if lista[i] == valor:
            return i

tela = TelaPython()
tela.iniciar()
