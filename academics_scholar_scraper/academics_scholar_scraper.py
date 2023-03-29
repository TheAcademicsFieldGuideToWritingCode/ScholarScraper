import argparse
import os
import requests
import json
import csv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from .openai_summarizer import generate_summary

API_KEY = os.environ.get("ELSEVIER_API_KEY")
if not API_KEY:
    raise ValueError("Environment variable ELSEVIER_API_KEY not set")

SUMMARY_PROMPT = "can you provide the following for the content of this article? Give one sentence for each of the following: summary, hypotheses, methods, findings. Even if no abstract is provided, use what knowledge is openly available about the author and their works to estimate. There's no need to restate what's been given to you in the prompt. format your output as json."
NUM_THREADS = 8


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Search for scholarly articles using the Elsevier Scopus API"
    )
    parser.add_argument("keyword", help="Keyword to search for")
    parser.add_argument(
        "-n",
        "--num_papers",
        type=int,
        default=10,
        help="Number of papers to retrieve (default: 10)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="papers.csv",
        help="Output CSV file (default: papers.csv)",
    )
    parser.add_argument(
        "-s",
        "--subject",
        type=str,
        default="",
        help="Subject area (e.g., AGRI, ARTS, BIOC, etc.)",
    )
    return parser.parse_args()


def search_papers(keyword, num_papers, subject):
    """
    Search for papers using the Elsevier Scopus API.
    
    Args:
        keyword (str): Keyword to search for.
        num_papers (int): Number of papers to retrieve.
        subject (str): Subject area (e.g., AGRI, ARTS, BIOC, etc.).

    Returns:
        dict: JSON response from the API.
    """
    base_url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": API_KEY,
    }
    query = f'TITLE-ABS-KEY("{keyword}")'
    if subject:
        query += f" AND SUBJAREA({subject})"
    params = {
        "query": query,
        "count": num_papers,
        "view": "STANDARD",
        "sort": "citedby-count",  # Sort by the number of citations
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


def process_paper(paper):
    """
    Process a paper by generating a summary and updating the paper dictionary.

    Args:
        paper (dict): Paper data dictionary.

    Returns:
        dict: Updated paper data dictionary with summary information.
    """
    data_dict = {
        "Title": paper.get("dc:title", "N/A"),
        "Authors": paper.get("dc:creator", "N/A"),
        "Publication Name": paper.get("prism:publicationName", "N/A"),
        "Publication Date": paper.get("prism:coverDate", "N/A"),
        "DOI": paper.get("prism:doi"),
    }

    prompt = f"{SUMMARY_PROMPT}\n\n{data_dict}"
    summary = generate_summary(prompt)
    try:
        new_data = json.loads(summary)
        data_dict.update(new_data)
    except:
        Exception()
    
    return data_dict

def export_to_csv(paper_data, output_file):
    """
    Export paper data to a CSV file.

    Args:
        paper_data (dict): Paper data.
        output_file (str): Output CSV file path.
    """
    fieldnames = [
        "Title",
        "Authors",
        "Publication Name",
        "Publication Date",
        "DOI",
        "Summary",
        "Hypotheses",
        "Methods",
        "Findings",
    ]
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        papers = paper_data["search-results"]["entry"]

        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            results = list(tqdm(executor.map(process_paper, papers), desc="Processing papers", total=len(papers)))

        for result in results:
            writer.writerow(result)


def main():
    """Main function."""
    args = parse_args()
    paper_data = search_papers(args.keyword, args.num_papers, args.subject)
    export_to_csv(paper_data, args.output)
    print(f"Data exported to {args.output}")

def conduct_litreview(keyword, num_papers, subject, output):
    """Conducts a literature review on Google Scholar for the given keyword and subject,
    and exports the results to a CSV file with the given filename."""

    # Search for papers on Google Scholar
    paper_data = search_papers(keyword, num_papers, subject)

    # Export the paper data to a CSV file
    # export_to_csv(paper_data, output)

    # Print a message indicating the output filename
    # print(f"Data exported to {output}")
    return paper_data


if __name__ == "__main__":
    main()