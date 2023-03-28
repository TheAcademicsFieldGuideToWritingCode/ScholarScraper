import argparse
import csv
import os
import random
from scholarly import scholarly, ProxyGenerator
from tqdm import tqdm
from gpt_analysis import setup_openai, analyze_abstract

# Load the OpenAI API key from the environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
NUM_PAPERS = 1
NUM_AUTHORS = 1


# Check if the OpenAI API key is present and set the flag accordingly
if OPENAI_API_KEY:
    setup_openai(OPENAI_API_KEY)
    use_gpt_analysis = True
    print("OpenAI API key found. GPT analysis will be performed.")
else:
    use_gpt_analysis = False
    print("OpenAI API key not found. GPT analysis will be skipped.")

def parse_arguments():
    """
    Parse command-line arguments for the keyword and output file name.
    """
    parser = argparse.ArgumentParser(description='Collect paper summaries based on a keyword.')
    parser.add_argument('keyword', type=str, help='Keyword for paper search')
    parser.add_argument('output_file', type=str, help='CSV file name to export the data')
    args = parser.parse_args()
    return args.keyword, args.output_file

def setup_scholarly():
    """
    Set up the Scholarly package with a proxy for requests.
    """
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)
    

def search_authors_by_interest(keyword):
    """
    Search for authors on Google Scholar based on their interest keyword.
    """
    print("searching authors by keyword")
    return scholarly.search_author(keyword)

def get_top_cited_papers(author, keyword):
    """
    Get the top 10 cited papers for an author, including GPT analysis if enabled.
    """
    top_cited_papers = []
    for publication in author['publications'][:NUM_PAPERS]:
        full_pub = scholarly.fill(publication)
        paper = {
            'title': full_pub['bib']['title'],
            'author_name': author['name'],
            'key_word_list': keyword,
            'date_of_publication': full_pub['bib']['pub_year'],
        }
        
        if use_gpt_analysis:
            abstract = full_pub['bib']['abstract']
            research_question, method, result = analyze_abstract(abstract)
            paper.update({
                'abstract': abstract,
                'research_question': research_question,
                'method': method,
                'result': result,
            })

        top_cited_papers.append(paper)
    return top_cited_papers

def export_to_csv(data, output_file):
    """
    Export the collected paper data to a CSV file.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'author_name', 'key_word_list', 'date_of_publication']
        if use_gpt_analysis:
            fieldnames.extend(['abstract', 'research_question', 'method', 'result'])

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def collect_paper_data(keyword):
    """
    Collect paper data based on the keyword, including author and citation information.
    """
    setup_scholarly()
    print("starting authors collection")
    authors = list(search_authors_by_interest(keyword))[:NUM_AUTHORS]
    print(f"Found {len(authors)} authors for keyword '{keyword}'.")
    
    papers = []
    for author in authors:
        papers.extend(get_top_cited_papers(author, keyword))
    
    return papers

def main():
    keyword, output_file = parse_arguments()
    print(f"Collecting paper data for keyword '{keyword}'...")
    papers = collect_paper_data(keyword)
    print(f"Collected data for {len(papers)} papers.")
    
    print(f"Exporting data to {output_file}...")
    export_to_csv(papers, output_file)
    print(f'Data successfully exported to {output_file}')

if __name__ == '__main__':
    main()