# Boas Práticas Meta Ads 2025

> Guia completo baseado em pesquisa com 45+ fontes especializadas (Meta oficial, Jon Loomer, AdAmigo, Reddit r/FacebookAds, etc.)

---

## 1. Estrutura de Campanha

### CBO vs ABO

- **CBO (Campaign Budget Optimization)** — Recomendado para 90% dos casos. A IA do Meta distribui o budget entre ad sets automaticamente.
- **ABO (Ad Set Budget Optimization)** — Usar apenas para testes iniciais onde precisa de exposição igual entre criativos/audiências.

### Regras de Estrutura

- **3-5 ad sets por campanha CBO** — cada um com público distinto
- **3-6 anúncios por ad set** — variações de criativo
- **Budget mínimo: $20-50/dia por ad set** — para sair da fase de aprendizado
- **Meta: 50 conversões por ad set por semana** — o ideal para otimização do algoritmo
- **CBO total: R$150-250/dia** — mínimo recomendado para otimização eficiente

### Naming Convention

```
[Objetivo]_[Público]_[Data]_[Variação]
Exemplo: CONV_InteressesFitness_2025-02_v1
```

---

## 2. Targeting & Segmentação

### Hierarquia de Eficácia (2025)

1. **Custom Audiences** (retargeting) — Maior ROI
2. **Lookalike Audiences** — Melhor equilíbrio alcance/qualidade
3. **Advantage+ (Broad)** — IA otimiza, bom para conversão
4. **Interesses/Comportamentos** — Para nicho ou awareness

### Quando usar cada tipo

| Cenário | Targeting Recomendado |
|---------|----------------------|
| E-commerce com pixel maduro | Advantage+ ou Broad |
| Negócio local | Geo + Interesses |
| Lançamento sem dados | Interesses + Comportamentos |
| Retargeting | Custom Audiences (7-30 dias) |
| Escalar campanha vencedora | Lookalike 1-5% |

### Boas Práticas de Targeting

- **NÃO estreitar demais** — audiências <500K pessoas limitam o algoritmo
- **Tamanho ideal**: 1M-10M pessoas para conversão
- **Combinar interesses + comportamentos** — melhor que usar só um tipo
- **Broad targeting para conversão** — em 2025, performa melhor que targeting granular quando há pixel maduro
- **Lookalike audiences**: seed de 1.000-10.000 usuários, testar tiers 1%, 3%, 5%
- **Refreshar audiences a cada 1-2 meses**

### Advantage+ Audience

- Funciona como "sugestão" ao algoritmo, não como restrição
- Ideal para campanhas de conversão com pixel maduro (50+ conversões/semana)
- Combinar com interesse como "sinal" mas deixar IA expandir

---

## 3. Criativos

### Formatos por Performance (2025)

1. **Vídeo vertical (4:5 ou 9:16 Reels)** — Melhor performance geral
2. **Carousel** — Bom para e-commerce e produtos múltiplos
3. **Imagem estática** — Melhor para retargeting e mensagens simples

### Hook (Primeiros 3-5 segundos)

- O hook determina **mais de 50% do resultado** da campanha
- Tipos eficazes:
  - **Problema relato**: "Cansado de gastar dinheiro em ads sem resultado?"
  - **Afirmação bold**: "Isso mudou meu faturamento em 30 dias"
  - **Visual surpreendente**: Transformação, antes/depois
  - **Pergunta direta**: "Você sabia que 90% dos anunciantes erram nisso?"

### Copy Best Practices

- **Headline**: 6-8 palavras, benefício direto
- **Texto primário**: 125-150 caracteres para mobile
- **CTA claro**: "Compre Agora", "Saiba Mais", "Faça o Teste"
- **Texto de alto contraste para som desligado** — 85% dos vídeos são vistos sem som

### Testing Framework

- **Testar 3-5 variações** de hook e formato
- **Duração mínima**: 48h-72h (idealmente 2-4 semanas)
- **Confidence level**: 95% para declarar vencedor
- **Refreshar criativos a cada 3-4 semanas** para evitar fadiga

---

## 4. Bidding & Orçamento

### Estratégias de Lance

| Estratégia | Quando Usar | Risco |
|-----------|-------------|-------|
| **Lowest Cost** | Maximizar volume, orçamento flexível | Sem controle de CPA |
| **Cost Cap** | Manter CPA médio, escalar com previsibilidade | Pode limitar entrega |
| **Bid Cap** | Controle rígido de custo máximo por resultado | Alta limitação de entrega |

### Regras de Orçamento

- **Mínimo por ad set**: Budget que gere 1-2 conversões por dia
- **Fórmula**: CPA alvo × 2 = budget diário mínimo por ad set
- **Exemplo**: Se CPA alvo = R$30, budget mínimo = R$60/dia/ad set

### Escalar Sem Quebrar

- **Aumento gradual: 10-25% a cada 3-5 dias**
- **NUNCA dobre o orçamento de uma vez** — reseta a fase de aprendizado
- **Use CBO para escalar** — distribui budget automaticamente
- **Ao escalar, criar novo ad set** em vez de alterar o existente (opcional)

---

## 5. Funil de Campanha

### TOFU (Top of Funnel) — Awareness

- **Objetivo**: Alcance ou Vídeo Views
- **Público**: Broad, Interesses amplos ou Lookalike 5-10%
- **Criativo**: Conteúdo educacional, branding, problem-aware
- **Métrica chave**: CPM, Alcance, Video View Rate

### MOFU (Middle of Funnel) — Consideração

- **Objetivo**: Tráfego, Engagement ou Lead Gen
- **Público**: Custom Audience (visitou site 7-30 dias), Lookalike 1-3%
- **Criativo**: Social proof, depoimentos, comparativos
- **Métrica chave**: CTR, CPC, Custo por Lead

### BOFU (Bottom of Funnel) — Conversão

- **Objetivo**: Conversão (Compra, Lead, App Install)
- **Público**: Custom Audience (add to cart, iniciou checkout, 1-7 dias)
- **Criativo**: Urgência, desconto, CTA direto
- **Métrica chave**: CPA, ROAS, Taxa de Conversão

### Retargeting Windows

| Fase | Janela | Ação |
|------|--------|------|
| Quente | 1-3 dias | Lembrete direto, CTA forte |
| Morno | 7-14 dias | Social proof, benefícios |
| Frio | 15-30 dias | Reengajamento, nova oferta |
| Perda | 30-90 dias | Exclusivo para alto ticket |

---

## 6. Métricas & Otimização

### KPIs por Objetivo

| Objetivo | Métrica Principal | Benchmark |
|----------|------------------|-----------|
| Awareness | CPM | R$15-40 |
| Tráfego | CPC | R$0.50-2.00 |
| Leads | CPL | R$5-30 (varia por nicho) |
| Vendas | ROAS | 3x+ |
| App Install | CPI | R$3-10 |

### Quando Pausar um Anúncio

- **CTR < 1%** após 1000+ impressões
- **CPA > 2x do alvo** por 3+ dias consecutivos
- **Frequência > 3** (audiência saturada)
- **ROAS < 1.5x** por 5+ dias (e-commerce)

### Quando Escalar

- **CPA consistente abaixo do alvo** por 5+ dias
- **ROAS > 3x** por 7+ dias
- **CTR > 2%** com volume alto

### A/B Testing

- **Testar UMA variável por vez** (criativo OU público OU copy)
- **Mínimo 72 horas** de teste
- **Mínimo 100 conversões** por variante para significância
- **95% de confiança** para declarar vencedor

---

## 7. Mudanças 2025 — O que Saber

### Removido

- ❌ **Exclusões de targeting detalhado** (desde Mar/2025)
- ❌ **Interesses granulares consolidados** — muitos foram fundidos em categorias amplas (Jun/2025)

### Adicionado/Reforçado

- ✅ **Advantage+ Audience** — targeting automático pela IA
- ✅ **Advantage+ Shopping Campaigns** — e-commerce automatizado
- ✅ **Broader interest categories** — menos opções mas mais estáveis

### Impacto Prático

- Campanhas usando interesses antigos (criados antes de Out/2025) podem parar de entregar a partir de Jan/2026
- Use o campo `status` no arquivo de targeting para verificar se um público ainda é válido
- Migre para Advantage+ quando possível, mantendo interesses como "sinais"

---

## 8. Erros Comuns — O que NÃO Fazer

1. ❌ **Targeting muito estreito** (<500K) — mata o algoritmo
2. ❌ **Muitos ad sets competindo** (>10) — fragmenta o budget
3. ❌ **Alterar ads durante a fase de aprendizado** (primeiras 50 conversões)
4. ❌ **Dobrar orçamento de uma vez** — reseta aprendizado
5. ❌ **Testar por menos de 72 horas** — dados insuficientes
6. ❌ **Ignorar o criativo** — em 2025, criativo > targeting
7. ❌ **Landing page ruim** — melhor ad do mundo não salva LP lenta
8. ❌ **Copiar exatamente campanha do concorrente** — contexto muda
9. ❌ **Usar interesses com status ❌ ou ⚠️** — podem parar de funcionar
10. ❌ **Não instalar/configurar Pixel** — sem dados, sem otimização
