Feature: Buscar dados de mercado e criptomoedas

  Scenario: Buscar dados de um ativo específico
    Given que eu tenho o ticker "^GSPC" e o período "1y"
    When eu busco os dados do ativo
    Then o resultado deve ser um DataFrame não vazio com "^GSPC" nas colunas

  Scenario: Buscar desempenho dos setores
    Given que eu tenho uma lista de setores ["XLK", "XLE", "XLF"] e o período "6mo"
    When eu busco os dados dos setores
    Then o resultado deve ser uma série não vazia ordenada de forma decrescente

  Scenario: Buscar desempenho de índices populares
    Given que eu tenho uma lista de índices ["^GSPC", "^BVSP", "^IXIC"] e o período "1mo"
    When eu busco os dados dos índices
    Then o resultado deve ser uma série de floats não vazia

  Scenario: Buscar dados de criptomoedas pela API
    When eu busco os dados das criptomoedas
    Then o resultado deve ser uma lista não vazia com informações válidas
