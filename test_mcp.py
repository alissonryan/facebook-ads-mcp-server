import sys
import json

# Adicionar o diretório atual ao sys.path para poder importar o server
sys.path.insert(0, '.')
import server

def test_mcp():
    print("Testing MCP initialization...")
    
    # Simular a passagem de token via sys.argv para que o _get_fb_access_token() funcione
    sys.argv.append('--fb-token')
    sys.argv.append('SEU_META_ACCESS_TOKEN_AQUI')
    
    try:
        # Testa a primeira funcao - listando contas
        print("Calling list_ad_accounts()...")
        accounts = server.list_ad_accounts()
        print(f"✅ Success! Data returned:\n{json.dumps(accounts, indent=2)}")
        
        # Testa uma das novas funcoes de targeting search
        print("\nCalling search_interests(query='fitness')...")
        interests = server.search_interests("fitness", limit=2)
        print(f"✅ Success! Data returned:\n{json.dumps(interests, indent=2)}")
        
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    test_mcp()
