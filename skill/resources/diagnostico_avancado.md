# Diagnóstico Avançado Meta Ads 🧠

Este documento contém a base teórica avançada de funcionamento do algoritmo da Meta (Facebook/Instagram). **Você DEVE consultar as regras contidas aqui antes de recomendar qualquer pausa ou alteração de orçamento em anúncios e conjuntos de anúncios.**

---

## 1. O Efeito Breakdown (The Breakdown Effect)

O erro mais comum na análise de Meta Ads é interpretar que o sistema transferiu orçamento para segmentos de pior performance ao olhar quebras (breakdowns) por posicionamento, idade, etc.

* **A Ilusão:** Você olha um relatório por Posicionamento e vê que *Facebook Stories* teve um CPA de $1.10 (e gastou $50), enquanto *Instagram Stories* teve um CPA de $1.46 (mas gastou $450). A conclusão amadora é: "Desligue o Instagram Stories, ele está mais caro!".
* **A Realidade:** O algoritmo do Meta otimiza buscando a **Eficiência Marginal** (o custo da *próxima* conversão), não a Eficiência Média (o custo estático listado na tabela). No cenário acima, o Facebook Stories esgotou suas conversões baratas. Se o algoritmo tentasse forçar mais $1 nele, a próxima conversão (CPA Marginal) custaria $5.00. No Instagram, a próxima ainda custaria $1.50.
* **A Regra:** **NUNCA recomende pausar ou reduzir orçamento de um segmento baseando-se apenas no seu CPA ou CPM médio estar mais alto em um relatório de breakdown.** Se ele está recebendo mais orçamento global, é porque a previsão de custo *da próxima* conversão dele é a mais barata disponível.

## 2. Pacing (Ritmo de Gasto)

O Meta ajusta ativamente o quanto gasta por dia ou hora (Budget Pacing) e o quanto dá de lance no leilão (Bid Pacing).

* **Comportamento Normal:** O algoritmo frequentemente retém o orçamento (subentrega) hoje porque previu que existirão leilões muito mais baratos amanhã.
* **A Regra:** Analise a "lentidão" do gasto através da lente da campanha toda (janela de 7 dias). Nunca force um adset a gastar hoje o que o algoritmo preferiu guardar.

## 3. Diagnóstico de Relevância do Anúncio (Ad Relevance)

As métricas de Relevância indicam o porquê de um anúncio estar perdendo leilões (Total Value = Lance x pAction + Ad Quality).
Quando auditar anúncios (Via Insights), requisite/olhe para as seguintes métricas de diagnóstico:

| Ranking (Métrica) | O que mede e Como Corrigir |
| :--- | :--- |
| **Quality Ranking** (Qualidade) | Avalia feedback negativo e atributos ruins (clickbait). *Solução: Mude a imagem/vídeo e o tom do copy.* |
| **Engagement Rate Ranking** (Engajamento) | Predição de curtidas/cliques. *Solução: Crie ganchos (hooks) melhores para prender a atenção e pareça menos com propaganda pura.* |
| **Conversion Rate Ranking** (Conversão)** | Predição de ação pós-clique. *Solução: Melhore o CTA ou audite a Landing Page. O público está clicando mas não comprando.* |

> **Nota:** Se todas as métricas estão na "Média" ou "Acima da Média" e o CPA continua ruim, o problema não é o criativo. É o orçamento muito baixo, targeting excessivamente restrito, ou a oferta/produto em si.

## 4. O Nível Correto de Avaliação

Sempre julgue a performance baseando-se em QUEM controla o dinheiro. Avaliar no lugar errado quebra o algoritmo.

| Estrutura | Nível Correto para Auditar/Pausar | Erro Comum |
| :--- | :--- | :--- |
| **Advantage+ CBO** | Analisar e tomar ação no nível de **Campaign** | Pausar um Ad Set dentro do CBO só porque tem CPA maior. |
| **Placements Automáticos (Sem CBO)** | Analisar no nível de **Ad Set** | Pausar um "posicionamento X" dentro do Ad Set. |
| **Múltiplos Anúncios num Ad Set** | Analisar no nível de **Ad Set** | Desligar todos os ads "ruins", tirando opções de aprendizado do sistema. |

## 5. Fase de Aprendizado (Learning Phase)

Sempre verifique se a campanha/adset teve uma **Edição Significativa** recente. Mudanças grandes de orçamento (mais de 20%), alteração de público ou troca de criativo "zeram" a inteligência.

* O algoritmo precisa de cerca de **50 eventos de conversão** em 7 dias para sair dessa fase.
* *Orientação:* Na fase de aprendizado, CPAs flutuam insanamente. Nunca audite decretando "falência" do anúncio se ele estiver nos 3 primeiros dias dessa fase de flutuação extrema.

---
**Padrão Nomenclatura Pós-Auditoria:** Na sua saída para o usuário, sempre chame `clicks` de *Clicks (all)*, `cost_per_action_type:purchase` de *Cost per Purchase*, e `reach` de *Reach (Accounts Center accounts)*. Crianças métricas genéricas causam confusões graves.
