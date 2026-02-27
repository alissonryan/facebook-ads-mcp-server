# Referência de Endpoints Meta Marketing API (v25.0)

> Endpoints disponíveis para targeting e estimativas. Use esta referência para entender o que cada endpoint faz e como enriquecer as recomendações de campanha.

---

## Endpoints que JÁ usamos no script

| Endpoint | Tipo | Descrição |
|----------|------|-----------|
| `targetingbrowse` | Conta | Taxonomia estruturada de todos os targets |
| `targetingsearch` | Conta | Busca por termo em todos os tipos de targeting |
| `targetingsuggestions` | Conta | Sugestões baseadas em interesses selecionados |
| `adTargetingCategory` | Global | Browse por classe (interests, behaviors, demographics, life_events, industries, income, family_statuses, user_device, user_os) |
| `adinterest` | Global | Busca de interesses por nome |
| `adinterestsuggestion` | Global | Sugestões de interesses relacionados |
| `adinterestvalid` | Global | Validação de interesses (nome ou ID) |
| `targetingoptionstatus` | Global | Status de targeting options (NORMAL/DEPRECATING/NON-DELIVERABLE) |
| `adgeolocation` | Global | Países, regiões, cidades, CEPs, geo_markets |
| `adlocale` | Global | Idiomas disponíveis |
| `adeducationschool` | Global | Escolas e universidades |
| `adeducationmajor` | Global | Cursos/áreas de formação |
| `adworkemployer` | Global | Empregadores |
| `adworkposition` | Global | Cargos/job titles |

---

## Endpoints ADICIONAIS (não coletamos ainda)

### 1. Reach Estimate API ⭐

**URL:** `GET /act_{AD_ACCOUNT_ID}/reachestimate`
**O que faz:** Estima o alcance de uma combinação de targeting ANTES de criar a campanha.
**Útil para:** Validar se um público sugerido tem tamanho adequado.
**Parâmetros:**

- `targeting_spec` — a spec completa de targeting
- `optimize_for` — objetivo de otimização
**Retorna:** Estimativa de alcance diário e mensal (users_lower_bound, users_upper_bound)
**Documentação:** <https://developers.facebook.com/docs/marketing-api/audiences/guides/reach-estimate>

### 2. Estimated Daily Results

**URL:** `GET /act_{AD_ACCOUNT_ID}/delivery_estimate`
**O que faz:** Estima resultados diários para uma spec de targeting + orçamento.
**Útil para:** Prever CPA, CPM, impressões antes de gastar dinheiro.
**Parâmetros:**

- `targeting_spec` — targeting completo
- `optimization_goal` — objetivo (LINK_CLICKS, CONVERSIONS, etc.)
- `daily_budget` — orçamento diário
**Documentação:** <https://developers.facebook.com/docs/marketing-api/audiences/reference/estimated-daily-results>

### 3. Radius Suggestions (adradiussuggestion)

**URL:** `GET /search?type=adradiussuggestion`
**O que faz:** Dado uma lat/lng, sugere o raio ideal para alcançar pessoas suficientes.
**Útil para:** Negócios locais — qual raio usar ao redor da localização.
**Parâmetros:**

- `latitude` — latitude
- `longitude` — longitude
- `distance_unit` — "mile" ou "kilometer"
**Retorna:** `suggested_radius` e `distance_unit`

### 4. Geo Locations Metadata (adgeolocationmeta)

**URL:** `GET /search?type=adgeolocationmeta`
**O que faz:** Retorna metadata enriquecida para localizações específicas (país, região, cidade, CEP).
**Útil para:** Validar e enriquecer dados geográficos antes de usar no targeting.

### 5. Electoral Districts

**URL:** `GET /search?type=adgeolocation&location_types=["electoral_district"]`
**O que faz:** Busca distritos eleitorais (apenas EUA).
**Útil para:** Campanhas políticas e regionais nos EUA.

### 6. Country Groups

**URL:** `GET /search?type=adgeolocation&location_types=["country_group"]`
**O que faz:** Grupos de países predefinidos (Mercosur, EU, NAFTA, etc.)
**Útil para:** Campanhas internacionais que targetam blocos econômicos.

### 7. Targeting Description

**URL:** `GET /act_{AD_ACCOUNT_ID}/targetingsentencelines`
**O que faz:** Converte um targeting_spec em texto legível humano (ex: "Pessoas de 25-55 anos em São Paulo interessadas em fitness").
**Útil para:** Gerar descrições para relatórios ou propostas.
**Documentação:** <https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-description>

### 8. Targeting Validation (targetingvalidation)

**URL:** `GET /act_{AD_ACCOUNT_ID}/targetingvalidation`
**O que faz:** Valida múltiplos targets de uma vez (interesses + comportamentos + demografias) via targeting_list.
**Útil para:** Verificar se uma combinação completa de targeting é válida antes de criar o ad set.

### 9. Advantage Targeting (Advantage+)

**URL:** Parâmetro `targeting_automation` no ad set
**O que faz:** Permite ao Meta expandir automaticamente o targeting para encontrar mais conversões.
**Documentação:** <https://developers.facebook.com/docs/marketing-api/audiences/reference/advantage-targeting>

### 10. Flexible Targeting

**URL:** Parâmetro `flexible_spec` no targeting_spec
**O que faz:** Permite combinações OR entre múltiplos tipos de targeting (ex: "interesse A OU comportamento B").
**Útil para:** Criar públicos mais amplos sem stacking restritivo.
**Documentação:** <https://developers.facebook.com/docs/marketing-api/audiences/reference/flexible-targeting>

---

## Insights API (pós-campanha)

**URL:** `GET /act_{AD_ACCOUNT_ID}/insights`
**O que faz:** Retorna métricas de performance (impressões, cliques, CPA, ROAS, etc.)
**Útil para:** Analisar quais públicos performaram melhor.
**Documentação:** <https://developers.facebook.com/docs/marketing-api/insights>

---

## Prioridade de Implementação para Enriquecer a Skill

| Prioridade | Endpoint | Impacto |
|-----------|----------|---------|
| ⭐ Alta | Reach Estimate API | Validar tamanho de público antes de recomendar |
| ⭐ Alta | Targeting Description | Gerar descrições legíveis das recomendações |
| 🟡 Média | Estimated Daily Results | Prever CPA/CPM antes de gastar |
| 🟡 Média | Radius Suggestions | Essencial para negócios locais |
| 🟢 Baixa | Country Groups | Útil para campanhas internacionais |
| 🟢 Baixa | Electoral Districts | Apenas EUA, nicho político |
