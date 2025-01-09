# lol-match-analysis

Este projeto tem como objetivo analisar partidas de League of Legends utilizando a API oficial da Riot Games. A análise visa extrair informações úteis sobre desempenho, estratégias e estatísticas de jogadores ou equipes, além de fornecer insights valiosos para melhorar a experiência de jogo.

## Funcionalidades

- **Consulta de Dados de Partidas**: Busca informações detalhadas sobre partidas específicas.
- **Análise de Estatísticas**: Geração de estatísticas relacionadas a campeões, builds e desempenhos de jogadores.
- **Geração de Relatórios**: Criação de gráficos e relatórios que visualizam os dados de forma intuitiva.

## Tecnologias Utilizadas

- **Linguagem**: Python
- **Bibliotecas**:
  - `requests`: Para realizar chamadas à API da Riot Games.
  - `pandas`: Para manipulação e análise de dados.
  - `matplotlib` e `seaborn`: Para visualização de dados.
- **API**: Riot Games API

## Pré-requisitos

Antes de utilizar, certifique-se de ter as seguintes ferramentas instaladas em seu ambiente:

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

Além disso, será necessário obter uma chave de API da Riot Games. Para isso, siga os passos:

1. Crie uma conta ou faça login no [Developer Portal da Riot Games](https://developer.riotgames.com/).
2. Gere uma chave de API e anote-a. Ela será usada para autenticação nas requisições à API.

## Instalação

1. Clone o repositório do projeto:


   git clone https://github.com/Nikao1/lol-match-analysis.git
   cd lol-match-analysis

2. Crie e ative um ambiente virtual (recomendado):

   python -m venv venv
   source venv/bin/activate # No Windows, use: venv\Scripts\activate

3. Instale as dependências do projeto:

   pip install -r requirements.txt

4. Configure a chave API:

   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   ```.env
   RIOT_API_KEY=(chave api que resgatar no site de desenvolvedor da RIOT)
   RIOT_NICKNAME=(nick desejado)
   RIOT_TAGLINE=(tag desejada)
   ```

## Como Usar

1. Execute o script principal através do terminal utilizando o comando:

   cd src
   python main.py
   

2. Receba os dados através de um arquivo CSV


## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Se você tiver dúvidas ou sugestões, sinta-se à vontade para entrar em contato:

- **Email**: nikolasadsms@gmail.com
- **GitHub**: [Nikao1](https://github.com/Nikao1)
