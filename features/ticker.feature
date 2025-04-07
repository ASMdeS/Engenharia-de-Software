Feature: Análise de Ticker Financeiro

  Scenario: Verificar se o ticker é válido
    Given o ticker "AAPL"
    When verifico se o ticker é válido
    Then o resultado deve ser "válido"

  Scenario: Verificar se o ticker é inválido
    Given o ticker "XXXXINVALIDO"
    When verifico se o ticker é válido
    Then o resultado deve ser "inválido"
