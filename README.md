# 🏆lol-match-analysis

Este projeto tem como objetivo analisar partidas de **League of Legends** utilizando a API oficial da **Riot Games**. A análise foca em extrair informações sobre o desempenho de campeões, especialmente no que diz respeito ao uso de botas, fornecendo insights valiosos para análise do impacto do item obervado na taxa de vitórias.
Atualmente, a análise se concentra em partidas do elo Desafiante, onde se encontram os melhores jogadores, conforme o sistema de ranqueamento da Riot Games.

## 📊 Funcionalidades

- **Coleta de Dados de Partidas**: Busca informações detalhadas sobre partidas específicas de um jogador.
- **Análise de Estatísticas**: Gera estatísticas relacionadas ao uso de diferentes tipos de botas pelo(s) campe(ã)ões.
- **Visualização de Dados**: Cria gráficos que ilustram a taxa de vitória associada a cada tipo de bota utilizada.

## 🛠 Tecnologias Utilizadas

- **Linguagem**: Python
- **Bibliotecas**:
  - `requests`: Para realizar chamadas à API da Riot Games.
  - `pandas`: Para manipulação e análise de dados.
  - `matplotlib`: Para visualização de dados.

## 🚀 Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

Além disso, será necessário obter uma chave de API da Riot Games, disponível em: [Riot Games Developer Portal](https://developer.riotgames.com/)

**OBS.:** Precisará de uma conta na Riot Games para poder utilizar o recurso.

## 📥 Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/Nikao1/lol-match-analysis.git
   cd lol-match-analysis

2. Crie um ambiente virtual (recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows


3. Instale os pacotes necessários:

   ```bash
   pip install -r requirements.txt

4. Crie um arquivo .env na raiz do projeto
   
   ´´´bash
   echo RIOT_API_KEY= > .env & echo RIOT_NICKNAME= >> .env & echo RIOT_TAGLINE= >> .env

5. Preencha as variáveis no .env de acordo com o exemplo:

   RIOT_API_KEY=RGAPI-b4dadc-db2a-4444-95f9-d66b9aufe924
   RIOT_NICKNAME=Torricelli
   RIOT_TAGLINE=BR1

## 💻 Uso
Após configurar o projeto, você pode executá-lo de duas formas:

1. Através do editor de código
-  Execute o arquivo main.py diretamente pela interface do seu editor.

2. Através do terminal

  ´´´bash
   cd src
   python main.py

Isso garantirá que os dados e gráficos gerados sobre a relação entre botas e taxa de vitórias sejam armazenados, respectivamente, nas pastas:

-  📁 /data → Armazena os dados processados.
-  📁 /outputs → Contém os gráficos gerados.

## 🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias ou correções.

## 📱Contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nikolas-araujo/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nikao1)
