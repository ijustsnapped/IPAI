
# -*- coding: utf-8 -*-

import pandas as pd
from unidecode import unidecode
import isbnlib
import re
import json
import os

def normalize_column_names(df):
    column_map = {
        'ISBN': 'isbn13',
        'ISBN_13': 'isbn13',
        'parent_asin': 'asin',
        'ASIN': 'asin',
        'authors': 'author',
        'Authors': 'author',
        'Book-Author': 'author',
        'Author': 'author',
        'AUTHOR': 'author',
        'title_text': 'title',
        'TITLE': 'title',
        'Book-Title': 'title',
        'Book Name': 'title',
        'Title': 'title'
        # podes adicionar mais conforme necessário
    }
    df = df.rename(columns={col: column_map.get(col, col) for col in df.columns})
    return df


#Funcoes para a normalização 
# Função para normalizar títulos
def normalize_text(text):
    if pd.isna(text):
        return ""
    text = text.lower().strip()  # Converter para minúsculas e remover espaços extras
    text = re.sub(r'[^\w\s]', '', text)  # Remover pontuação e caracteres especiais
    text = re.sub(r'\s+', ' ', text)  # Substituir múltiplos espaços por um único
    return unidecode(text)  # Remover acentos

# Normalizar ISBNs
def normalize_isbn(isbn):
    if not isbn or not isinstance(isbn, str) or isbn.strip() == "":  # Verifica se é NaN ou não é string
        return None
    isbn = isbnlib.canonical(isbn)
    if isbnlib.is_isbn10(isbn):
        return isbnlib.to_isbn13(isbn)
    return isbn if isbnlib.is_isbn13(isbn) else None

# Função para normalizar o ASIN: remover espaços extras e converter para maiúsculas
def normalize_asin(asin):
    if pd.isna(asin):
        return ""
    return asin.strip().upper()

# Função para normalizar nomes de autores (iniciais de todos os primeiros nomes + último nome)
def normalize_author1(author):
    if pd.isna(author):
        return ""
    author = unidecode(author)               # Remover acentos
    author = re.sub(r"[^A-Za-z0-9\s]", "", author)  # Remover caracteres especiais
    author = re.sub(r"\s+", " ", author)     # Substituir múltiplos espaços por um único
    author = author.strip().upper()          # Remover espaços nas pontas e pôr em maiúsculas
    return author

# Função para normalizar nomes de autores (vários autores separados por "/")
def normalize_authors2(authors):
    if pd.isna(authors) or not isinstance(authors, str):
        return ""
    author_list = [a.strip() for a in authors.split('/')]
    normalized_authors = []
    for author in author_list:
        author = unidecode(author)                           # Remover acentos
        author = re.sub(r"[^A-Za-z0-9\s]", "", author)       # Remover caracteres especiais
        author = re.sub(r"\s+", " ", author)                 # Reduzir espaços múltiplos
        author = author.strip().upper()                      # Strip + maiúsculas
        normalized_authors.append(author)
    return ", ".join(normalized_authors)

def normalize_authors3(authors):
    if pd.isna(authors) or not isinstance(authors, str) or authors.strip() == "":
        return ""
    author_list = [a.strip() for a in authors.split(",")]
    normalized_authors = []
    for author in author_list:
        author = unidecode(author)                           # Remover acentos
        author = re.sub(r"[^A-Za-z0-9\s]", "", author)       # Remover caracteres especiais
        author = re.sub(r"\s+", " ", author)                 # Substituir múltiplos espaços por um
        author = author.strip().upper()                      # Trim e maiúsculas
        normalized_authors.append(author)
    return ", ".join(normalized_authors)


def normalize_author4(author):
    if pd.isna(author) or not isinstance(author, str):  # Verifica se é NaN ou não é string
        return ""
    
    # Se houver mais de um autor, separar os autores por vírgulas e normalizar cada um individualmente
    authors = author.split(',')
    
    # Normalizar cada autor individualmente
    normalized_authors = []
    for individual_author in authors:
        individual_author = individual_author.strip()
        # Remover "By" ou "by" em qualquer parte do nome
        individual_author = individual_author.replace("by ", "").replace("By ", "")
        # Remover acentos
        individual_author = unidecode(individual_author)
        # Converter para maiúsculas
        individual_author = individual_author.upper()
        normalized_authors.append(individual_author)
    
    # Juntar os autores normalizados com vírgulas
    return ", ".join(normalized_authors)

## 

df1 = pd.read_csv("C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\1_amazon\\amazon_meta_books.csv")

df1['parent_asin'] = df1['parent_asin'].apply(normalize_asin)
df1['title'] = df1['title'].apply(normalize_text)
#não existe coluna para os autores mas sim uma com os detalhes dos livros onde inclui o autor e outras informações
df1=normalize_column_names(df1)
df1_normalized_only = df1[['asin', 'title']]

output_path1 = "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\1_amazon\\amazon_meta_books_normalized.csv"
n1=df1_normalized_only.to_csv(output_path1, index=False)

###

df2 = pd.read_csv("C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\2_3_goodreads\\goodReads_2019_2020_fixed.csv")

# Aplicar normalizações

df2['title'] = df2['title'].apply(normalize_text)
df2['authors'] = df2['authors'].apply(normalize_authors2)
df2['isbn13'] = df2['isbn13'].apply(normalize_isbn)
#não existe asin
df2=normalize_column_names(df2)
df2_normalized_only = df2[['title', 'author', 'isbn13']]

output_path2 = "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\2_3_goodreads\\goodreads_2019_2020_normalized.csv"
n2=df2_normalized_only.to_csv(output_path2, index=False)

### 

input_path = "C:\\Users\\maria\\Downloads\\Trabalho de grupo\\Datasets\\Datasets\\2_3_goodreads\\goodreads_3000RCount.json"
df = pd.read_json(input_path, lines=True)

# Normalizar ASIN
df['asin'] = df.apply(lambda row: row.get('asin') or row.get('kindle_asin') or "", axis=1)

# Normalizar ISBN
df['isbn'] = df.apply(lambda row: row.get('isbn13') or row.get('isbn') or "", axis=1)
df['isbn'] = df['isbn'].apply(normalize_isbn)

# Selecionar apenas as colunas desejadas
df_cleaned = df[['asin', 'isbn']]

output_path3 = "C:\\Users\\maria\\Downloads\\Trabalho de grupo\\Datasets\\Datasets\\2_3_goodreads\\goodreads_3000RCount_normalized.csv"
# Exportar para CSV
df_cleaned.to_csv(output_path3, index=False)

###

# Carregar dados 
df4 = pd.read_csv("C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\4_bookcrossing\\book_crossing_Books.csv")

# Aplicar normalização
df4['ISBN'] = df4['ISBN'].apply(normalize_isbn)
df4['Book-Title'] = df4['Book-Title'].apply(normalize_text)
df4['Book-Author'] = df4['Book-Author'].apply(normalize_author1)
#não existe asin
df4=normalize_column_names(df4)
df4_normalized_only = df4[['isbn13', 'title', 'author']]

output_path4 = "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\4_bookcrossing\\book_crossing_Books_normalized.csv"
n4=df4_normalized_only.to_csv(output_path4, index=False)

###

df5 = pd.read_csv("C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\5_sales_N_ratings\\Books_Data_Clean.csv")

df5['Book Name'] = df5['Book Name'].apply(normalize_text)
df5['Author'] = df5['Author'].apply(normalize_authors3)
#não existe qualquer número de identificação único isbn ou asin
df5=normalize_column_names(df5)
df5_normalized_only = df5[['title', 'author']]

output_path5 = "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\5_sales_N_ratings\\Books_Data_Clean_normalized.csv"
n5=df5_normalized_only.to_csv(output_path5, index=False)

### 

df6 = pd.read_csv("C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\6_ranks_print_kindle\\amazon_com_extras.csv", encoding="latin1", on_bad_lines="skip", quotechar='"')

df6['ASIN'] = df6['ASIN'].apply(normalize_asin)
df6['Title'] = df6['TITLE'].apply(normalize_text)
df6['AUTHOR'] = df6['AUTHOR'].apply(normalize_author1)
#não existe isbn
df6=normalize_column_names(df6)
df6_normalized_only = df6[['asin','title', 'author']]

output_path6 = "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\6_ranks_print_kindle\\amazon_com_extras_normalized.csv"
n6=df6_normalized_only.to_csv(output_path6, index=False)

###

df7 = pd.read_csv("C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\7_kindle\\kindle_data-v2.csv")

df7['asin'] = df7['asin'].apply(normalize_asin)
df7['title'] = df7['title'].apply(normalize_text)
df7['author'] = df7['author'].apply(normalize_author1)
df7=normalize_column_names(df7)
df7_normalized_only = df7[['asin','title', 'author']]

output_path7 = "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\7_kindle\\kindle_data-v2_normalized.csv"
n7=df7_normalized_only.to_csv(output_path7, index=False)

###

df8 = pd.read_csv("C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\8_wonderbk\\BooksDataset.csv")

df8['Title'] = df8['Title'].apply(normalize_text)
df8['Authors'] = df8['Authors'].apply(normalize_author4)
df8=normalize_column_names(df8)
df8_normalized_only = df8[['title', 'author']]

output_path8 = "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\8_wonderbk\\BooksDataset_normalized.csv"
n8=df8_normalized_only.to_csv(output_path8, index=False)

############################################################
    
import pandas as pd
import jellyfish

# --- Funções auxiliares para similaridade ---
def jaccard_sim(str1, str2):
    set1 = set(str1.split())
    set2 = set(str2.split())
    intersecao = set1.intersection(set2)
    uniao = set1.union(set2)
    return len(intersecao) / len(uniao) if uniao else 0

# --- Gera as chaves para cada dataset individualmente ---
def gerar_chaves_por_dataset(df, nome_dataset):
    chaves = {}
    for idx, row in df.iterrows():
        isbn = str(row.get("isbn13") or row.get("isbn") or "").strip()
        asin = str(row.get("asin") or "").strip()
        titulo = str(row.get("title") or row.get("titulo") or "").strip()
        autor = str(row.get("author") or row.get("autor") or "").strip()

        if isbn:
            chave = "isbn_" + isbn
        elif asin:
            chave = "asin_" + asin
        else:
            chave = "titulo_autor_" + titulo + "_" + autor
        chaves[chave] = (idx, nome_dataset)  # Guarda o índice e o nome do dataset
    return chaves

# --- Blocking principal com similaridade ---
def encontrar_comuns(datasets, nomes_datasets, limiar_autor=0.9, limiar_titulo=0.8, minimo_datasets=2):
    chaves_por_dataset = []
    for i, df in enumerate(datasets):
        chaves_por_dataset.append(gerar_chaves_por_dataset(df, nomes_datasets[i]))

    matches = []
    total_datasets = len(datasets)

    # Criar uma lista para armazenar os matches e os datasets onde ocorreu a correspondência
    for chave_base in chaves_por_dataset[0]:
        idxs = [None] * total_datasets
        presencas = 1
        datasets_com_match = [nomes_datasets[0]]  # Armazenar os datasets que têm match

        idxs[0] = chaves_por_dataset[0][chave_base][0]
        
        tipo = ""

        if chave_base.startswith("isbn_"):
            tipo = "isbn"
            for i in range(1, total_datasets):
                if chave_base in chaves_por_dataset[i]:
                    idxs[i] = chaves_por_dataset[i][chave_base][0]
                    presencas += 1
                    datasets_com_match.append(nomes_datasets[i])

        elif chave_base.startswith("asin_"):
            tipo = "asin"
            for i in range(1, total_datasets):
                if chave_base in chaves_por_dataset[i]:
                    idxs[i] = chaves_por_dataset[i][chave_base][0]
                    presencas += 1
                    datasets_com_match.append(nomes_datasets[i])

        elif chave_base.startswith("titulo_autor_"):
            tipo = "fuzzy"
            titulo_base = datasets[0].loc[chaves_por_dataset[0][chave_base][0]]["title"]
            autor_base = datasets[0].loc[chaves_por_dataset[0][chave_base][0]]["author"]

            for i in range(1, total_datasets):
                for chave_cand, (idx_cand, _) in chaves_por_dataset[i].items():
                    if chave_cand.startswith("titulo_autor_"):
                        row_cand = datasets[i].loc[idx_cand]
                        sim_autor = jellyfish.jaro_winkler_similarity(autor_base, row_cand["author"])
                        sim_titulo = jaccard_sim(titulo_base, row_cand["title"])
                        if sim_autor >= limiar_autor and sim_titulo >= limiar_titulo:
                            idxs[i] = idx_cand
                            presencas += 1
                            datasets_com_match.append(nomes_datasets[i])
                            break

        # Se o livro for encontrado em pelo menos 2 datasets, adicionamos ao resultado
        if presencas >= minimo_datasets:
            grupo = []
            for i, idx in enumerate(idxs):
                if idx is not None:
                    grupo.append(datasets[i].loc[idx])

            # Adicionar a informação de qual dataset contém a correspondência
            grupo.append({"datasets_match": ", ".join(datasets_com_match)})
            matches.append(grupo)

    return matches

# --- Ponto de entrada principal ---
if __name__ == "__main__":
    caminhos_datasets = [
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\1_amazon\\amazon_meta_books_normalized.csv", 
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\2_3_goodreads\\goodreads_2019_2020_normalized.csv", 
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\2_3_goodreads\\goodreads_3000RCount_normalized.csv", 
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\4_bookcrossing\\book_crossing_Books_normalized.csv", 
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\5_sales_N_ratings\\Books_Data_Clean_normalized.csv",
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\6_ranks_print_kindle\\amazon_com_extras_normalized.csv",
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\7_kindle\\kindle_data-v2_normalized.csv",
        "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\Datasets\\Datasets\\8_wonderbk\\BooksDataset_normalized.csv"
    ]
    nomes_datasets = ["1_amazon", "2_goodreads", "3_goodreads", "4_bookcrossing", "5_sales_N_ratings", "6_ranks_print_kindle", "7_kindle", "8_wonderbk" ]

    datasets = [pd.read_csv(caminho) for caminho in caminhos_datasets]

    matches = encontrar_comuns(datasets, nomes_datasets, minimo_datasets=2)

    # Exportar os resultados para um CSV com a coluna datasets_match
    def exportar_csv(matches, nome_ficheiro):
        linhas = []
        for grupo in matches:
            registo_comum = {}
            for i, livro in enumerate(grupo[:-1]):  # Exclui a última entrada que é o 'datasets_match'
                for chave, valor in livro.items():
                    registo_comum[f"{chave}_dataset{i+1}"] = valor
            # Adicionar a informação do dataset onde o match foi encontrado
            registo_comum["datasets_match"] = grupo[-1]["datasets_match"]
            linhas.append(registo_comum)

        df_resultado = pd.DataFrame(linhas)
        df_resultado.to_csv(nome_ficheiro, index=False)

    exportar_csv(matches, "C:\\Users\\diogo\\Desktop\\Mestrado\\IPAI\\pasta\\matches_resultado.csv")