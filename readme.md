# Facebook/Meta Ads MCP Server

Este projeto fornece um servidor Model Context Protocol (MCP) que atua como uma interface completa para a API do Meta Ads. Ele permite que LLMs e agentes acessem dados programáticos e gerenciem ativamente campanhas, conjuntos de anúncios, criativos e audiências no Facebook e Instagram.

> **Nota de Versão:** Este repositório é um fork evoluído do projeto original da `gomarble-ai`, agora expandido para suportar não apenas leitura (`Read-Only`), mas também operações avançadas de configuração, estimativa e escrita/CRUD (`Read/Write`).

---

## 🚀 Funcionalidades Principais

O servidor foi atualizado e agora possui **mais de 45 ferramentas disponíveis**, cobrindo o ciclo completo de planejamento, criação e análise de campanhas:

- **Targeting Inteligente:** Busca sugestões de interesses, comportamentos, dados demográficos, e geolocalizações.
- **Predição de Delivery:** Estimação em tempo real de alcance potencial (Reach) e leilão (CPA/CPM) baseado em orçamentos.
- **Gestão de Campanhas (CRUD):** Crie, atualize, delete ou arquive Campaigns, Ad Sets e Ads via ferramentas MCP nativas.
- **Gestão de Criativos & Mídia:** Upload de imagens e vídeos usando URLs; listagem de acervos da conta; geração de Iframes de preview do anúncio (`get_ad_preview`).
- **Audiências Avançadas:** Criação nativa de Custom Audiences (base de clientes/CRM via e-mails com SHA-256 implícito) e Lookalike Audiences.
- **Reporting e Insights:** Acesse dados robustos de performance de anúncios em qualquer nível com parâmetros configuráveis (ROAS, CPA, Cliques, etc).

> ⚠️ **Operações de Escrita (WRITE OPERATIONS):** A nova suíte de endpoints permite deleção local e configurações no seu Meta AdsManager. Todos os endpoints construtivos criam objetos no estado `PAUSED` por segurança, a menos que especificado caso contrário pelo Agente.

---

## 💻 Setup Inicial

### Pré-requisitos

* Python 3.10+
- Token de Acesso da Meta API contendo permissões como `ads_read` e `ads_management`

### Instalação

1. Clone o repositório e acesse a pasta do projeto.
2. Crie um ambiente virtual para isolar as dependências e o SDK local:

```bash
python3 -m venv venv
source venv/bin/activate
# ou no windows: venv\Scripts\activate
```

1. Instale os requerimentos:

```bash
pip install -r requirements.txt
# Certifique-se também da instalação interna correta
pip install mcp requests
```

---

## 🛠️ Integrando ao Claude Desktop

Para integrar aos clientes MCP padrão (como Cursor ou Claude Desktop), basta abrir o seu arquivo de configurações MCP (ex: `claude_desktop_config.json`) e inserir:

```json
{
  "mcpServers": {
    "fb-ads-mcp-server": {
      "command": "/caminho/completo/para/venv/bin/python",
      "args": [
        "/caminho/completo/para/seu/server.py",
        "--fb-token",
        "SEU_META_ACCESS_TOKEN"
      ]
    }
  }
}
```

## 🤖 Integrando ao DROID CLI (Factory.ai)

O DROID se benefícia grandemente de ferramentas MCP utilizando modo `stdio`. Abra ou edite o arquivo `~/.factory/mcp.json` e registre o Meta Ads Server.

> Certifique-se de substituir e utilizar os **caminhos absolutos** do python da `venv` e do script `server.py`:

```json
{
  "mcpServers": {
    "meta-ads": {
      "type": "stdio",
      "command": "/Users/NAME/path/facebook-ads-mcp-server/venv/bin/python",
      "args": [
        "/Users/NAME/path/facebook-ads-mcp-server/server.py",
        "--fb-token",
        "SEU_META_ACCESS_TOKEN"
      ],
      "disabled": false
    }
  }
}
```

Após essa configuração, apenas reinicie sua instância do DROID para que as ferramentas sejam catalogadas.

---

## 📚 Novas Ferramentas (Destaques da Atualização)

Aqui está uma prévia simplificada das novas ferramentas injetadas nos LLMs. (*Existem dezenas de ferramentas clássicas de Insights e Activity History também incluídas no script `server.py`*).

| Nova Ferramenta MCP             | Descrição                                                                 |
| -------------------------------- | ------------------------------------------------------------------------- |
| **Planejamento de Públicos**      |                                                                           |
| `search_interests` / `behaviors`  | Puxa opções de target para uso no payload da API e estimativa de tamanho. |
| `get_delivery_estimate`           | Estima os custos CPA/CPM de um conjunto com base no target + orçamento.   |
| **Criação & Edição**              |                                                                           |
| `create_campaign`, `update_campaign`| Cria campanhas (ex: CONVERSIONS) de forma programática.                |
| `create_adset`, `update_adset`    | Configura grupos de anúncios com o target_spec montado pelo Agente.       |
| `create_ad`, `update_ad`          | Dispara os anúncios criativos.                                            |
| `upload_ad_image`                 | Sobe criativo da Web para a biblioteca do seu gerenciador.                |
| `delete_object`                   | Ferramenta universal de limpeza/arquivamento via Meta Node/ObjectId.      |
| **CRM e Audiências**              |                                                                           |
| `create_custom_audience`          | Cria um container para público personalizado (CRM/Base Interna).          |
| `update_custom_audience_users`    | Processa e envia os dados (emails, phones) hashados para popular um Custom Audience. |
| `create_lookalike_audience`       | Gera públicos semelhantes a partir de uma fonte prévia do site ou CRM.     |

---

## 📜 Licença

Distribuído sob a Licença MIT.
*Forked originalmente de Gomarble-AI.*
