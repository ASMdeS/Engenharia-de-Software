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
streamlit run app.py
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

[Especificar a licença do projeto]

## Contato

[Informações de contato do mantenedor do projeto]
