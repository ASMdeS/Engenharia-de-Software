# Projeto de Mercado Financeiro - Guia de Configuração e Instalação

## Pré-requisitos

Antes de começar, verifique se você tem instalado:

- Python 3.9+
- pip (gerenciador de pacotes do Python)
- Git (opcional, mas recomendado)

## Configuração do Ambiente Virtual

1. Crie um ambiente virtual:

```bash
python -m venv venv
```

2. Ative o ambiente virtual:

No Windows:

```bash
venv\Scripts\activate
```

No macOS/Linux:

```bash
source venv/bin/activate
```

## Instalação de Dependências

Instale as dependências usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Lista de Dependências Principais

- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- yfinance

## Estrutura do Projeto

```
projeto_mercado_financeiro/
│
├── Diagramas/
│   └── test_analysis.py
│
├── app.py
├── requirements.txt
├── CONTRIBUTING.md
├── README.md
└── BUILD.md
```

## Executando o Projeto

### Iniciar Aplicação Streamlit

Para iniciar a aplicação web:

```bash
streamlit run Homepage.py
```

### Executar Testes

Para rodar os testes unitários:

```bash
python -m pytest tests/
```

### Geração de Relatórios

Para gerar relatórios de cobertura de testes:

```bash
python -m pytest --cov=src tests/
```

### Erros de Importação de Bibliotecas

- Certifique-se de que todas as dependências estão instaladas corretamente
- Verifique se o ambiente virtual está ativado
- Reinstale as dependências se necessário

## Contribuição

1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

### MIT License

Este projeto está licenciado sob a MIT License - uma licença permissiva de código aberto que permite praticamente
qualquer uso, incluindo comercial, com pouquíssimas restrições.

```
MIT License

Copyright (c) [ano] [nome completo ou nome da organização]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contato

Arthur Santos Marinho de Souza (asms@cin.ufpe.br)
Daniel Dias Martins Fernandes (dmdf@cin.ufpe.br)
Rafael Mourato Dantas Vilar (rmdv@cin.ufpe.br)

[Informações de contato do mantenedor do projeto]
