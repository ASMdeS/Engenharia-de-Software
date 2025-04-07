Feature: Testar lógica de backtesting para ações

  Scenario: Executar estratégia de cruzamento de médias móveis
    Given que eu tenho dados históricos simulados
    When eu aplico a estratégia de média móvel com janelas 5 e 20
    Then o resultado deve conter colunas "Short MA", "Long MA" e "Strategy Return"

  Scenario: Executar estratégia RSI com parâmetros padrão
    Given que eu tenho dados históricos simulados
    When eu aplico a estratégia RSI com janela 14, sobrevenda 30 e sobrecompra 70
    Then o resultado deve conter colunas "RSI" e "Strategy Return"
