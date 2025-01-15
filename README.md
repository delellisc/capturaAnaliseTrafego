# Avaliação de Redes

## comandos da avaliação

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

Comandos para verificar o tráfico tcp da placa ethernet:
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

![alt text](./images/image-1.png)

![alt text](./images/image-2.png)

Ao abrir, serão apresentadas as capturas feitas pelo tcpdump:
![alt text](./images/image.png)

Pesquisar por um IP específico:
![alt text](image.png)

![alt text](image-1.png)

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
