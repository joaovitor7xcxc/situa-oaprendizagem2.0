# Documentação de Casos de Teste - Checkout Inteligente com ViaCEP

## 1. Visão Geral do Projeto
Sistema de Checkout Inteligente que consulta a API ViaCEP (https://viacep.com.br/ws/{CEP}/json/) para preencher automaticamente informações de endereço baseado no CEP inserido pelo cliente.

---

## 2. Tabela de Casos de Teste

| ID | Cenário | Entrada | Resultado Esperado | Tipo de Teste |
|----|---------|---------|-------------------|---------------|
| CT-001 | CEP válido com endereço existente | 01310100 (Av. Paulista, SP) | API retorna status 200 com logradouro, bairro e cidade preenchidos | Caminho Feliz ✓ |
| CT-002 | CEP com formato correto mas não existe | 99999999 | API retorna status 404 (CEP não encontrado) | Validação de Exceção |
| CT-003 | CEP com formato inválido (contém letras) | "ABC12345" | API retorna erro ou status 400 (Requisição inválida) | Validação de Formato |
| CT-004 | CEP com quantidade incorreta de dígitos | "123" | API retorna erro ou status 400 | Validação de Comprimento |
| CT-005 | CEP vazio ou nulo | "" | Sistema não faz requisição ou API retorna erro | Validação de Campo Obrigatório |
| CT-006 | CEP válido com resposta estruturada | 20040020 (Centro, RJ) | Resposta contém campos: logradouro, bairro, localidade, uf | Validação de Estrutura |

---

## 3. Análise de Cenários

### 🟢 Caminho Feliz (CT-001)
- **Objetivo**: Validar o fluxo normal do checkout inteligente
- **Dados**: CEP 01310100 (Avenida Paulista, São Paulo)
- **Validações**: Status 200, presença de logradouro, bairro e cidade

### 🟡 Validações de Negócio (CT-002)
- **Objetivo**: Garantir comportamento adequado em CEP válido mas inexistente
- **Dados**: CEP 99999999 (formato correto, mas não existe)
- **Validações**: Status 404 ou indicação de "não encontrado"

### 🔴 Validações de Formato (CT-003 a CT-005)
- **Objetivo**: Proteger o sistema contra entradas malformadas
- **Dados**: Letras, quantidade incorreta de dígitos, campos vazios
- **Validações**: Erros apropriados sem quebra do sistema

### 🔵 Validações de Estrutura (CT-006)
- **Objetivo**: Garantir que todos os campos necessários estão presentes
- **Dados**: CEP 20040020 (Centro, Rio de Janeiro)
- **Validações**: Verificação de campos obrigatórios na resposta JSON

---

## 4. Notas de Implementação
- Usar `requests.Session()` para manter conexão aberta durante os testes
- Implementar pytest fixtures com `scope='session'` e `scope='function'`
- Considerar timeout de resposta para API externa
- Tratar possíveis erros de conectividade

---

## 5. Tecnologias Utilizadas
- **Framework de Testes**: pytest
- **Cliente HTTP**: requests
- **API Externa**: ViaCEP
- **Linguagem**: Python 3.x
