# 🛒 Supermarket Data Pipeline: Medallion Architecture & GenAI

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-3.x-E25A1C?style=flat&logo=apachespark&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Groq%20%7C%20Llama%203.1-1C3C3C?style=flat)

> Pipeline de dados ponta a ponta que transforma feedbacks brutos de clientes em **recomendações estratégicas automatizadas por IA**, aplicado ao setor varejista com Arquitetura Medalhão.

---

## 💡 Problema & Solução

Supermercados recebem centenas de feedbacks de clientes diariamente — e a maior parte é ignorada por falta de estrutura para analisá-los em escala.

Este projeto resolve isso automatizando todo o fluxo: da extração no banco de dados até a entrega de insights prontos para a gerência, com **análise de sentimento** e **sugestões de ação** geradas por LLM (Llama 3.1 via Groq).

**Resultado prático:** feedbacks que antes exigiam análise manual passam a ser processados, classificados e priorizados automaticamente — com urgência e ação recomendada para cada caso.

---

## 🏗️ Arquitetura do Pipeline (Medallion)

```
[PostgreSQL] ──► [Bronze Layer] ──► [Silver Layer] ──► [Gold Layer] ──► [Parquet .output]
   Raw DB           Ingestão          PySpark              GenAI
                    bruta             Limpeza &         LangChain +
                                    Normalização        Groq API
                                                      (Sentimento +
                                                        Ação IA)
```

| Camada | Responsabilidade | Tecnologia |
|--------|-----------------|------------|
| 🥉 Bronze | Ingestão dos dados brutos do banco operacional | PostgreSQL → Python |
| 🥈 Silver | Limpeza, normalização e padronização de esquemas | PySpark |
| 🥇 Gold | Enriquecimento com IA: sentimento + ação recomendada | LangChain + Groq (Llama 3.1) |

---

## 📊 Outputs Gerados

O pipeline entrega um arquivo Parquet enriquecido com as seguintes colunas por feedback:

| Campo | Descrição |
|-------|-----------|
| `sentimento` | Classificação automática: **Positivo** ou **Negativo** |
| `urgencia` | Escala de prioridade para atendimento (Alta / Média / Baixa) |
| `acao_recomendada` | Sugestão objetiva gerada pela IA para a gerência agir |

---

## 🛠️ Stack Tecnológica

| Categoria | Tecnologia |
|-----------|-----------|
| Orquestração | Apache Airflow (Dockerizado) |
| Processamento | PySpark & Pandas |
| Inteligência Artificial | LangChain + Groq API (Llama 3.1-8b) |
| Banco de Dados | PostgreSQL |
| Armazenamento | Parquet (Camada Gold) |
| Infraestrutura | Docker & Docker Compose |

---

## 🔧 Como Executar

### Pré-requisitos

- Docker & Docker Compose instalados
- Chave de API da [Groq](https://console.groq.com)

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/cjunioral/projeto-ai-data-engineering.git
cd projeto-ai-data-engineering
```

**2. Configure as variáveis de ambiente**
```plaintext
# .env
GROQ_API_KEY=sua_chave_aqui
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
```

**3. Suba os serviços**
```bash
docker-compose up -d
```

**4. Acesse o Airflow e ative a DAG**
```
http://localhost:8080
```

---

## 👤 Sobre o Autor

**Cícero Ramalho da Rocha Júnior**  
Data Engineer  


[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/cicerorjunior)
