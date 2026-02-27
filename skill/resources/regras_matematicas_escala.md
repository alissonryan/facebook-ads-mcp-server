# Regras Matemáticas de Otimização, Escala e Testes A/B 📈

Este documento define regras de ouro, quantitativas e inflexíveis, para gerenciar orçamento e fadiga nas campanhas da Meta. **Não aja por achismo. Use esses números.**

---

## 1. Monitoramento Diário: Fadiga Criativa (Creative Fatigue)

A fadiga mata o ROAS lentamente. Monitorar a queda do CTR é mais importante que olhar apenas o CPA do dia.

* **⚠️ Alerta Crítico (Pausar):** Se o CTR de um anúncio cair **mais de 20% do seu pico** por 3 dias seguidos.
* **🟡 Alerta de Atenção (Frequência):** Se a frequência diária/semanal ultrapassar **3.5** no público frio. Significa que a mesma pessoa está vendo o ad vezes demais sem clicar. Hora de rotacionar os criativos.
* **🟡 Alerta de Leilão (CPC):** Se o CPC subir **mais de 15%** em relação a uma base de 7 dias seguidos, o leilão está rejeitando o criativo.

---

## 2. Otimização de Orçamento (Budget Shift)

Sempre que analisar campanhas e conjuntos, divida os anúncios em duas cestas matemáticas antes de tomar ação:

### A) Os "Bleeders" (Sangradores)

Anúncios que apenas torram dinheiro sem eficiência.

* **Regra:** `CTR < 1,0%` E `Spend (Gasto) > $10` (ou equivalente na moeda local que pague 1-2 leads).
* **Ação Mínima:** Pausar IMEDIATAMENTE.
* **Ação Avançada:** Realocar esse orçamento economizado para os Winners.

### B) Os "Winners" (Vencedores)

Anúncios com alta eficiência no ecossistema atual.

* **Regra:** `CTR > 1,5%` E `CPA abaixo da meta` (ou ROAS acima do breakeven).
* **Ação Mínima:** Escalar orçamento (Regra de Escala Segura abaixo).

---

## 3. A Regra de "Escala Segura" (Vertical Scaling)

Se você encontrar conjuntos de anúncios "Winners" e o usuário quiser escalar, **NUNCA dobre o orçamento do nada**. Isso reseta a Fase de Aprendizado (Learning Phase) do Meta, destruindo a otimização.

* **Regra de Ouro (Budget Smoothing):** Aumente o orçamento em **no máximo 20%** a cada **3 dias**.
  * *Exemplo:* De R$ 100/dia para R$ 120/dia. Espera 3 dias. Se o ROAS mantiver, sobe para R$ 144/dia.
* Sempre informe o usuário de que essa regra visa evitar o *Significant Edit* no algoritmo.

---

## 4. Laboratório de Testes Científicos (A/B)

Se o usuário quiser testar uma nova Headline, Copy ou Imagem, não crie bagunça na campanha principal que está performando.

* **O Princípio do Isolamento:** Para saber o que funciona, **apenas 1 variável pode ser alterada por vez**.
* **Workflow do Teste A/B Perfeito via MCP:**
    1. Peça para ler os IDs de sucesso.
    2. Crie um novo "Ad Set" de Laboratório (ou use o nativo).
    3. Duplique o anúncio vencedor (`Ad A`).
    4. Crie o `Ad B` com **exatamente as mesmas configurações**, alterando **SOMENTE** o que deseja testar (Ex: Muda só a imagem, mas mantém 100% da copy, título e público iguais).
    5. Deixe rodar por 72h-96h (ou até atingir R$ 50-R$ 100 de gasto mínimo) antes de decretar um vencedor baseado nos mesmos critérios da seção 2.
