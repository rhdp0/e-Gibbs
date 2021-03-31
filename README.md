# e-Gibbs v.1.0
Calcule propriedades termodinâmicas com alguns clicks.

Nesta versão do e-Gibbs usaremos arquivos .out criados no mopac para calcular entalpia e entropia de moléculas usando temperaturas de 200°K à 400°K.

No projeto foi utilizado o PySimgleGUI para criar a interface gráfica.

# Usando o e-Gibbs:

1. Primeiramente use o botão 'Browse' para buscar o arquivo .out.
2. Informe o número de moléculas.
3. Informe a temperatura.
3. Dê um nome para a mólecula que será inserida.
4. Informe se ela é um produto ou um reagente.
5. Clique em 'Inserir'.
6. Após ter inserido produtos e reagentes clique em 'Calcular'.

# Exemplo:
"H2O + H2O ---> (H2O)2"

H2O: 	Número de moléculas = 2
     	Reagente

(H2O)2:	Número de moléculas = 1
	Produto


Para fazer um novo cálculo com novos produtos e reagentes clique em 'Reiniciar'.
