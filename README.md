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
sudo tcpdump -i 1 tcp
sudo tcpdump -D
sudo tcpdump -i enp2s0
sudo tcpdump -i enp2s0 tcp
sudo tcpdump -i enp2s0 tcp -w ./captura.pcap
```