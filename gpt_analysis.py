import openai
import concurrent.futures

def setup_openai(api_key):
    """Set up the OpenAI API key."""
    openai.api_key = api_key

def analyze_single_prompt(prompt):
    """Analyze a single prompt using OpenAI GPT-3."""
    completions = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150, n=1, stop=None, temperature=0.5)
    return completions.choices[0].text.strip()

def analyze_abstract(abstract):
    """
    Analyze the abstract of a paper using OpenAI GPT-3.
    Returns the research question, method, and result.

    Args:
        abstract (str): The abstract of the paper.

    Returns:
        research_question (str): The main research question of the paper.
        method (str): The method used in the research.
        result (str): The main result of the research.
    """

    # Define the prompts for GPT-3 analysis
    prompts = [
        f"Please analyze the following abstract and identify the main research question, method, and result of the paper:\n\nAbstract: {abstract}\n\nResearch Question: ",
        f"Method: ",
        f"Result: "
    ]

    print("Analyzing abstract using GPT-3...")
    
    # Parallelize GPT-3 analysis for each prompt
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(analyze_single_prompt, prompt) for prompt in prompts]
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    research_question, method, result = results
    print("GPT-3 analysis completed.")
    
    return research_question, method, result