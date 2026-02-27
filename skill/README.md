# Meta Ads Campaign Expert - Guia de Sobrevivência e Operação 🚀

Bem-vindo ao centro de comando da skill **Meta Ads Campaign Expert**. Esta inteligência artificial não é apenas um assistente de texto gpt-wrapper; é um **Agente Autônomo Read/Write** integrado diretamente à API da Meta (via servidor MCP `facebook-ads-mcp-server`).

Ela foi desenhada com a arquitetura matemática, tática e estratégica dos melhores gestores de tráfego globais, unindo:

1. **Poder de Execução (CRUD):** Cria, edita, pausa e gerencia campanhas, conjuntos, anúncios e públicos (Custom/Lookalike) diretamente na sua conta.
2. **Diagnóstico Avançado (Breakdown Effect):** Não foca apenas no CPA médio enganoso, mas otimiza pela *Eficiência Marginal*.
3. **Tática de Copy & Retargeting:** Aplica obrigatoriamente fórmulas de alta conversão (PAS, BAB) e respeita limites milimétricos de caracteres da plataforma e janelas de funil de vendas (1-7 dias, 7-30 dias, 30-90 dias).
4. **Regras Matemáticas Inflexíveis (The Daily Check):** Possui travas de segurança contra *Significant Edits* (escala máxima de 20%), diagnostica *Fadiga Criativa* por queda real de CTR em 3 dias e classifica implacavelmente anúncios entre "Bleeders" (Sangradores) e "Winners" (Vencedores).

---

## 🛠️ Como Iniciar: O Menu de Comandos (Prompts)

Para operar esta skill com maestria, você pode usar os comandos abaixo (basta copiar e colar no chat adaptando os dados entre colchetes para a sua realidade). O agente saberá exatamente qual "Workflow" e qual "Arquivo de Inteligência" acionar.

### Fase 1: Planejamento e Criação do Zero (Workflow 1)

*Use quando quiser lançar uma nova campanha ou estrutura.*

* **Setup Inicial:** *"Inicie o planejamento de uma campanha do zero para [Nome do Infoproduto/Serviço]. O objetivo é [Vendas/Leads] e o orçamento é R$ [X]/dia. Vamos começar."*
* **Identificação de Contas:** *"Liste todas as contas de anúncio que eu tenho acesso atreladas a este MCP e me diga os IDs para eu escolher."*
* **Prospecção de Interesses (Targeting):** *"Faça uma pesquisa profunda de interesses ocultos na API da Meta para um público que compra [Seu Produto], focando em pessoas de [X a Y anos] no [Brasil/Estado]."*
* **Geração de Ad Copy (Copywriter Mode):** *"Use seus frameworks de alta conversão (Guia de Criativos) e escreva 3 opções de Ad Copy focadas no público de [Estudantes de Direito] usando o framework [PAS - Problem/Agitate/Solve]. O produto resolve o problema de [Falta de Tempo]."*
* **Deploy (Escrita na API com Segurança):** *"Tudo aprovado! Com base no público [X] e na copy [Y] que validamos, crie a estrutura completa da campanha na conta [ID_DA_CONTA]. Lembre-se da regra de ouro: crie TUDO com o status PAUSADO para minha revisão final no Gerenciador."*

### Fase 2: Gestão de Orçamento Diário e Escala (Workflow 4)

*A rotina matemática que você deve rodar todos os dias.*

* **O Daily Check (Saúde Financeira):** *"Faça a checagem de saúde diária (Workflow 4) nas minhas campanhas ativas da conta [ID]. Separe quem são os 'Bleeders' (sangrando dinheiro) e quem são os 'Winners'."*
* **Escala Segura (Scaling):** *"O anúncio [Nome/ID] está voando com ROAS de 4. Quero dobrar o orçamento amanhã usando o MCP. Qual é a sua instrução matemática final de escala segura para proteger a fase de aprendizado?"* (O agente vai te bloquear limitando a 20%).
* **Rotacionar Criativos (Fatigue Monitor):** *"Analise os anúncios ativos da campanha [Nome/ID]. Aplique a sua regra matemática de fadiga criativa. Há algum anúncio onde o CTR caiu mais de 20% em 3 dias seguidos ou a frequência passou de 3.5?"*
* **Efetivar Rebalanceamento:** *"Quero redistribuir o orçamento de hoje para focar na eficiência. Pause os Bleeders que você encontrou na API e use a matemática teto (20%) para escalar os orçamentos dos Winners."*

### Fase 3: Diagnóstico Avançado de Perdas (Workflow 2)

*Use quando uma campanha ficar muito cara e você precisar de um relatório pericial.*

* **Auditoria de Eficiência Marginal:** *"Faça uma auditoria minuciosa na minha campanha [Nome/ID]. Entregue o relatório com a análise pelo Efeito Breakdown e o status de Fase de Aprendizado de cada conjunto."*
* **Investigação de Gargalos:** *"Por que o CPA do Ad Set [X] está subindo tanto hoje? Puxe e analise os Ad Relevance Diagnostics (Quality Ranking, Engagement e CVR) no MCP para me dizer se o problema é o Anúncio em si ou a minha Página de Vendas."*
* **Decisão Segura:** *"Olhando para a campanha [XYZ], a inteligência me sugere pausar o conjunto B puramente pelo custo (CPA) médio consolidado de hoje, ou devo mantê-lo ativo por causa da Eficiência Marginal? Justifique baseando-se no arquivo de diagnóstico avançado."*

### Fase 4: Retargeting, CRM e Testes A/B Científicos (Workflow 3)

*Para explorar inteligência de dados, funis agressivos e descobrir as melhores combinações.*

* **Desenho de Funil (Remarketing):** *"Quero montar uma campanha de Retargeting agressiva para pessoas que iniciaram o checkout ontem e não compraram. Qual a janela temporal exata que devo usar segundo a nossa matriz de funil, e quais exclusões eu preciso criar obrigatoriamente na API antes de subir a campanha?"*
* **Criador de Públicos Especiais (Custom/LAL):** *"Aqui está um arquivo [CSV/Dados] com e-mails dos meus compradores recentes. Conecte pelo MCP, faça o encodamento de segurança (SHA-256) e crie um Público Personalizado no Meta. Depois, crie um Público Semelhante (Lookalike) de 1% focado na similaridade com esses compradores."*
* **O Laboratório de Conversão (Isolamento de Teste):** *"Quero testar uma variação da Imagem A contra a Imagem B no meu adset vencedor sem estragar a campanha. Qual o procedimento exato do 'Laboratório A/B Científico' que devo executar via MCP para garantir que as variáveis sejam isoladas?"*

---

## 🔒 Arquitetura de Segurança (Disclaimer)

- Nenhuma campanha ou anúncio é criado como `ACTIVE` por padrão. Para intervir na produção, a skill sempre enviará payloads como `status: "PAUSED"`. O disparo financeiro final é seu!
* Nenhuma deleção em massa (`delete_x`) faz parte dos fluxos recomendados.
* Orçamentos vencedores jamais sofrem mutações não solicitadas que extrapolem safe guides.
