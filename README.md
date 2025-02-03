<!-- # Avaliação de Redes -->

# Avaliação 2 - Aplicação de Redes de Computadores: Captura & Análise de Tráfego

## Realizando captura
Nesse capítulo serão comentados os passos realizados para obter um arquivo de captura de tráfego utilizando a ferramenta TShark.

### Instalando TShark:
```sh
sudo apt-get update
sudo apt-get -y install tshark
```

Verificando após a instalação:
```sh
tshark --version
```
### Fazendo a captura:
Criando um arquivo para receber informações da captura:
```sh
touch captura_limitada.cap
chmod 666 captura_limitada.cap 
```

Realizando a captura limitando a 30.000 pacotes:
```sh
sudo tshark -i enp2s0 -w ./captura_limitada.cap -a filesize:30000
```

### Obter informações do arquivo de captura:
```sh
sudo capinfos ./captura_limitada.cap && ls -la ./captura_limitada.cap && uname -ompvn
```
OBS.: apenas para verificar se está correto.

### Exibindo informações no nível TCP:

Algumas informações de fluxo:
```sh
tshark -r ./captura_limitada.cap -Y tcp -T fields -e frame.time_relative -e ip.proto -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport
```

Tamanho do pacote e tempo entre chegadas em formato CSV:
```sh
tshark -r ./captura_limitada.cap -Y tcp -T fields -e frame.time_relative -e ip.proto -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e ip.len -e frame.time_delta -E separator=,
```

Pacotes que envolvem solicitação de conexão TCP:
```sh
tshark -r ./captura_limitada.cap -Y '(tcp && tcp.flags.syn==1 && tcp.flags.ack==0)' -T fields -e frame.number -e frame.time_relative -e ip.proto -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e ip.len -e frame.time_delta -E separator=,
```

Redirecionando a saída do comando a seguir para o arquivo "tcp.tmp":
```sh
tshark -r ./captura_limitada.cap -Y '(tcp && tcp.flags.syn==1 && tcp.flags.ack==0)' -T fields -e frame.number -e frame.time_relative -e ip.proto -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e ip.len -e frame.time_delta -E separator=, > ./tcp.tmp
```

Estatísicas do volume de dados em fluxo TCP:
```sh
tshark -r ./captura_limitada.cap -q -z 'conv,tcp,ip'
```

Filtrando as colunas a serem exibidas no comando acima (exibindo colunas 1, 3, 8 e 9):
```sh
tshark -r ./captura_limitada.cap -q -z 'conv,tcp,ip' | grep '<->' | awk '{ print $1 "," $3 "," $8 "," $9"," $11 }'
```

### Extraindo informações HTTP
Tráfego HTTP:
```sh
tshark -r ./captura_limitada.cap -Y 'tcp && (tcp.dstport==80 || tcp.dstport==443)' -T fields -e frame.number -e frame.time_relative -e ip.proto -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e ip.len -e frame.time_delta -E separator=\,
```

Domínios visitados:
```sh
tshark -r ./captura_limitada.cap -Y http.request -T fields -e http.host | sort -u
```

Domínios mais visitados (filtrado por quantidade n=10):
```sh
tshark -r ./captura_limitada.cap -Y http.request -T fields -e http.host | sort -u
```

Conexões HTTP inseguras (fitrado pela porta dstport==80):
```sh
for stream in $(tshark -nlr "./captura_limitada.cap" -Y '(tcp.flags.syn==1 && tcp.dstport==80)' -T fields -e tcp.stream | sort -n | uniq); 
    do echo "DADOS DO FLUXO $stream" ; tshark -nlr "./captura_limitada.cap" -q -z "follow,tcp,ascii,$stream";
done | more
```

Exemplo de saída:
```sh
DADOS DO FLUXO 12

===================================================================
Follow: tcp,ascii
Filter: tcp.stream eq 12
Node 0: 10.49.10.60:60274
Node 1: 23.212.191.102:80
431
POST / HTTP/1.1
Host: r10.o.lencr.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/
[...]
```

## Refinamento dos dados recebidos
Após a obtenção da captura, foi utilizada a ferramenta Tranalyzer2 para extrair informações relevantes, que posteriormmente seriam utilizadas na análise dos dados coletados.

### Instalação do Tranalyzer2:
Passo a passo para instalação:
```sh
wget https://tranalyzer.com/download/tranalyzer/tranalyzer2-0.9.0lmw1.tar.gz
tar xzf tranalyzer2-0.9.0lmw1.tar.gz tranalyzer2-0.9.0/ls
cd tranalyzer2-0.9.0/
./setup.sh 
source ~/.bashrc
```
Verificando após a instalação:
```sh
t2 --version
```

### Exibindo colunas desejadas no terminal
Verificando o conteúdo do arquivo [results_headers.txt](./resultados/results_headers.txt), é possível verificar as existentes no arquivo de capture e informações correspondentes a elas:
```sh
cat ./resultados/results_headers.txt
```

Exemplo de saída:
```sh
# Date: 1737652709.850808 sec (Thu 23 Jan 2025 14:18:29 -03)
# Tranalyzer 0.9.0 (Anteater), Cobra
# Core configuration: L2, IPv4, IPv6
# SensorID: 666
# PID: 21566
[...]
# Plugins loaded:
#   01: protoStats, version 0.9.0
#   02: basicFlow, version 0.9.0
#   03: macRecorder, version 0.9.0
#   04: portClassifier, version 0.9.0
#   05: basicStats, version 0.9.0
[...]
# Col No.       Type    Name    Description
1       C       dir     Flow direction
2       U64     flowInd Flow index
3       H64     flowStat        Flow status and warnings
4       U64.U32 timeFirst       Date time of first packet
5       U64.U32 timeLast        Date time of last packet
```
Sabendo disso, é possível selecionar algumas colunas relevantes para serem extraídas, como as dispostas na tabela abaixo:

| Informação                                     | Nome do Campo      | Número da Coluna |
|------------------------------------------------|--------------------|------------------|
| Duração do Fluxo                               | duration           | 6                |
| Tamanho médio do pacote na camada 3            | avePktSize         | 35               |
| Desvio padrão do tamanho do pacote na camada 3 | stdPktSize         | 36               |
| Tempo médio entre chegadas (IAT)               | aveIAT             | 39               |
| Contagem de sequência de pacotes TCP           | tcpPSeqCnt         | 58               |
| Tamanho médio efetivo da janela TCP            | tcpAveWinSz        | 66               |
| Média de viagem de ACK TCP                     | tcpRTTAckTripAve   | 92               |

Utilizando o comando tawk para visualizar colunas selecionadas:
```sh
tawk -F" " '{print $6, $35, $36, $39, $58, $66, $92}' ./resultados/results_flows.txt
```

<!-- | Informação                          | Nome do campo      | Número da Coluna |
|-------------------------------------|--------------------|------------------|
| Duração do Fluxo                    | duration           | 6                |
| Tamanho Médio do Pacote da Camada 3 | avePktSize         | 35               |
| Desvio Padrão do Tamanho do Pacote  | stdPktSize         | 36               |
| Tempo Médio entre Chegadas          | aveIAT             | 39               |
| Contagem de Sequência TCP           | tcpPSeqCnt         | 58               |
| Tamanho Médio da Janela TCP         | tcpAveWinSz        | 66               |
| Média do RTT de Viagem do ACK TCP   | tcpRTTAckTripAve   | 92               | -->

<!-- 
| Informação                             | Nome do campo      | Número da Coluna |
|----------------------------------------|--------------------|------------------|
| Flow Duration                          | duration           | 6                |
| Average layer 3 packet size            | avePktSize         | 35               |
| Standard deviation layer 3 packet size | stdPktSize         | 36               |
| Average IAT (Inter-Arrival Time)       | aveIAT             | 39               |
| TCP packet seq count                   | tcpPSeqCnt         | 58               |
| TCP average effective window size      | tcpAveWinSz        | 66               |
| TCP ACK trip average                   | tcpRTTAckTripAve   | 92               |
-->

### Extraindo colunas desejadas e inserindo em um arquivo
Redirecionando a saída do comando acima para o arquivo [colunas_extraidas.csv](./colunas_extraidas.csv):

```sh
tawk -F" " '{print $6, $35, $36, $39, $58, $66, $92}' ./resultados/results_flows.txt > colunas_extraidas.csv
```

## Elaboração do relatório
7.1. Elabore um relatório e inclua textos e gráficos para responder às seguintes perguntas.
Confeccione um relatório demonstrando em texto e gráficos, com o objetivo de responder os
seguintes quesitos:

### a) Qual o tempo médio de duração de um fluxo
...

### b) Qual o tamanho médio de um pacote da camada 3
...

### c) Qual o desvio padrão do tamanho de um pacote de camada 3
...

### d) Qual o inter-arrival time (IAT) - O tempo entre chegadas - de cada pacote
...

### e) No contador de sequência dos números de pacotes há algum tempo com “0”, por que isso ocorre?
...

### f) Qual a média do tempo de viagem (RTT - Round Trip Time) da flag ACK no TCP
...


<!-- ## Comandos para instalar ferramentas necessarias

Instalação das ferramentas necessárias para a avaliação:
```sh
sudo apt-get update
sudo apt-get -y install wireshark-common tshark tcpdump
```

Verificando a instalação:
```sh
wireshark --version
```

Esses pacotes não foram instalados:
```sh
tshark --version
tcpdump --version
```

Instalei individualmente:
```sh
sudo apt-get -y install tshark
sudo apt-get -y install tcpdump
```

Verificando após a segunda instalação:
```sh
tcpdump --version
tshark --version
```

Rodando esse comando apenas para garantir:
```sh
sudo apt -y --fix-broken install
```

## Comandos para realizar a captura

Comandos para verificar o tráfego tcp da placa ethernet:
```sh
sudo tcpdump -D
```

O comando abaixo exibe o trafego de rede da placa de rede 1:
```sh
sudo tcpdump -i 1 tcp
```

E equivalente ao comando a seguir:
```sh
sudo tcpdump -i enp2s0
```

Filtrar para trafego TCP:
```sh
sudo tcpdump -i enp2s0 tcp
```

Redirecionando a saida do comando para um arquivo:
```sh
sudo tcpdump -i enp2s0 tcp -w ./captura.pcap
```

Copiando o arquivo para uma pasta que qualquer um consegue ler o arquivo:
```sh
cp captura.pcap /tmp/
```

OBS.: não é necessário se for criado na pasta de aluno

Dando permissão de leitura:
```sh
chmod 444 /tmp/captura.pcap 
```

## Wireshark

Apos isso, e preciso abrir o wiresharkpara visualizar as informacoes do arquivo de captura:
```sh
wireshark
```
O programa sera aberto, apresentando a seguinte interface grafica:
![alt text](./images/image-1.png)

No canto superior direito seleciona-se a opcao "File" e em seguida "Open" para abrir o arquivo. A interface abaixo sera aberta e o caminho do arquivo deve ser acessado/fornecido no campo de texto:
![alt text](./images/image-2.png)

Ao abrir, serão apresentadas as capturas feitas pelo tcpdump:
![alt text](./images/image.png)

Para pesquisar por um IP específico, eh preciso formular uma string de busca informando o IP desejado e inserir no campo de texto na parte superior da pagina:
![alt text](./images/image-3.png)

## Exportacao e tratamento dos dados de captura

Por fim, para exportar os dados em formato .csv, sera necessario selecionar "File", "Export Packet Dissections" e "As CSV" como mostra a imagem abaixo:
![alt text](./images/image-4.png)

Convertendo o campo tempo das capturas para o formato Epoch e apresentando o resultado no terminal:
```sh
tshark -r /tmp/captura.pcap -Y tcp -T fields -e frame.time_epoch
```

Redirecionando a saída para um arquivo de texto:
```sh
tshark -r /tmp/captura.pcap -Y tcp -T fields -e frame.time_epoch > /tmp/tempo
```

Exibir portas de origem das capturas:
```sh
tshark -r /tmp/captura.pcap -Y tcp -T fields -e tcp.srcport
```

Redirecionando a saída para umm arquivo de texto:
```sh
tshark -r /tmp/captura.pcap -Y tcp -T fields -e tcp.srcport > /tmp/porta_origem
```

## Adicionar campo tempo e porta de origem na captura exportada
Primeiramente movi/copiei os arquivos gerados no passo anterior para o diretório atual:
```sh
cp /tmp/porta_origem ./csv
cp /tmp/tempo ./csv
```
### Escrevendo script
Depois disso escrevi o seguinte [script](./script.py):
```py
with open("./csv/captura_exportada2.csv", "r") as input, open("./csv/tempo", "r") as f1, open("./csv/porta_origem", "r") as f2:
    input_lines = input.readlines()
    f1_lines = f1.readlines()
    f2_lines = f2.readlines()
with open("./csv/captura_alterada.csv", "w") as captura_alterada:
    for line1, line2, input_line in zip(f1_lines, f2_lines, input_lines):
        captura_alterada.write(f"{input_line.strip()}, {line1.strip()}, {line2.strip()}\n")
```

Esse script é responsável por ler três arquivos, o arquivo .csv com as informações da captura, o arquivo com o tempo criado anteriormente e o arquivo com as portas de origem também criados anteriormente. Após fazer a leitura desses arquivos e criar uma lista com as linhas, essas linhas são iteradas e escritas em um novo arquivo, "[captura_alterada](./csv/captura_alterada.csv)".

### Executando script
O script pode ser rodado com o seguinte comando:
```sh
python3 ./script.py 
``` -->