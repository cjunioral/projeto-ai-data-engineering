import os
import glob
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

def enrich_with_ai():

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("ERRO: GROQ_API_KEY não encontrada. Verifique seu arquivo .env")
        return

    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0, 
        groq_api_key=api_key
    )

    path_silver = "/opt/airflow/data/silver/supermarket_cleaned/*.csv"
    files = glob.glob(path_silver)
    
    csv_files = [f for f in files if "part-" in f]
    
    if not csv_files:
        print(f"Nenhum dado encontrado em: {path_silver}")
        return
    
    print(f"Lendo arquivo: {csv_files[0]}")
    df = pd.read_csv(csv_files[0])

    parser = JsonOutputParser()
    
    template = """
    Você é um Analista de Qualidade especializado em varejo.
    Analise os feedbacks dos clientes do supermercado e retorne uma LISTA de objetos JSON.
    Para cada item, use exatamente estes campos:
    'id': (id original),
    'sentimento': (Positivo ou Negativo),
    'urgencia': (Nota de 1 a 5),
    'acao_recomendada': (Sugestão curta para o gerente)
    
    Dados dos clientes: {dados}
    """

    prompt = PromptTemplate(template=template, input_variables=["dados"])
    chain = prompt | llm | parser

    dados_input = df[['id', 'produto_nome_bruto', 'comentario_cliente']].head(10).to_dict(orient='records')
    
    print("Enviando dados para análise na Groq")
    
    try:
        respostas = chain.invoke({"dados": dados_input})
        
        df_resultado = pd.DataFrame(respostas)
        df_final = df.merge(df_resultado, on='id', how='left')
        
        output_dir = '/opt/airflow/data/gold'
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = f"{output_dir}/insights_supermercado.parquet"
        df_final.to_parquet(output_path, index=False)
        
        print(f"Camada GOLD gerada com sucesso: {output_path}")
        print("\n--- AMOSTRA DOS INSIGHTS ---")
        print(df_final[['produto_nome_bruto', 'sentimento', 'acao_recomendada']].head())

    except Exception as e:
        print(f"Erro na integração com a Groq: {e}")

if __name__ == "__main__":
    enrich_with_ai()