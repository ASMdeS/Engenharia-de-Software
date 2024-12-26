import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Projeto Engenharia de Software",
    layout="wide",
)

# Título
st.title("Projeto Engenharia de Software")

# Subtítulo
st.subheader("Curso de Sistema de Informação - UFPE | 2024.2")

# Introdução
st.markdown("""
Este projeto foi desenvolvido por alunos do curso de Sistema de Informação da Universidade Federal de Pernambuco - UFPE, 
para a cadeira de Engenharia de Software no semestre de 2024.2. É um projeto de autoria de **Rafael Mourato**, **Arthur Santos** 
e **Daniel Dias**, como forma de aplicar os conhecimentos e solucionar a problemática:

**Como posso fazer análises financeiras de maneira independente e intuitiva?**
""")

# Contexto
st.header("Contexto")
st.markdown("""
O mercado financeiro está cada vez mais presente na vida dos brasileiros, com um crescimento de 80% no número de investidores 
desde 2020, segundo a B3. Pensando em ajudar aqueles que adentram nesse mercado, nossa equipe idealizou um portfólio de informações 
financeiras para que investidores possam ter visualizações pertinentes na escolha das suas ações e fundos, juntamente com **Backtests** 
para análise de evolução de carteira em uma perspectiva passada.
""")

# Objetivos e funcionalidades
st.header("Objetivos principais e funcionalidades")
st.markdown("""
O objetivo principal é entregar um portfólio de informações diversas para auxiliar em decisões de investimentos. 
As principais funcionalidades incluem:
- **Backtests** para análise de carteira.
- Simulações financeiras de investimento.
- Análises financeiras em dashboards e indicadores como **DRE**, **Balanço Patrimonial** e **Demonstração do Fluxo de Caixa**.
""")

# Estrutura organizacional do código
st.header("Estrutura organizacional do código")
st.markdown("""
Para acessar a estrutura organizacional, visite o Miro em [Modelagem C4](https://www.miro.com).
""")

# Links para recursos importantes
st.header("Links para recursos importantes")
st.markdown("""
- **[Notion](https://www.notion.so)**: Onde organizamos o projeto.
- **[Miro](https://www.miro.com)**: Organizações internas.
- **BUILD.md**: Guia para construção local do sistema.
""")

# Lista de issues
st.header("Lista de Issues")
st.subheader("Issues Abertas")
st.markdown("""
1. Iniciar implementação da solução.
2. Seleção de ferramentas para construção.
""")
st.subheader("Issues Concluídas")
st.markdown("""
1. Preparar entregas iniciais da RFP.
2. Montar os requisitos funcionais e não funcionais.
3. Definir ideia do projeto.
4. Estruturação da equipe.
""")

# Requisitos
st.header("Requisitos")
st.subheader("Requisitos Funcionais")
st.markdown("""
- O sistema deve permitir que os usuários criem e gerenciem suas carteiras de investimentos.
- O sistema deve exibir informações financeiras detalhadas sobre ações e fundos.
- O sistema deve fornecer gráficos relevantes.
- O sistema deve permitir a realização de Backtests.
- O sistema deve permitir cadastro e autenticação com segurança.
""")
st.subheader("Requisitos Não Funcionais")
st.markdown("""
- O sistema deve responder às consultas de visualização de dados em até 5 segundos.
- O sistema deve proteger os dados sensíveis dos usuários.
- O sistema deve seguir as normas da LGPD.
- O design deve ser intuitivo e seguir boas práticas de usabilidade.
- O sistema deve consultar dados financeiros de APIs abertas.
""")

# Orientações sobre contribuições
st.header("Orientações sobre como contribuir")
st.markdown("""
Leia o **COLABORACAO.md** para detalhes sobre como contribuir com o projeto.
""")

# Equipe
st.header("Equipe")
st.markdown("""
- **Rafael Mourato** (GP/Dev)
- **Arthur Santos** (Dev)
- **Daniel Dias** (Dev)
""")
