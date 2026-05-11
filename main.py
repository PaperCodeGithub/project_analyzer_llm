import warnings
from colorama import init, Fore, Style

warnings.filterwarnings("ignore")
init(autoreset=True)

#####
print(f"{Fore.LIGHTBLUE_EX}Welcome to the Codebase Explainer!{Style.RESET_ALL}")
print(f"{Fore.LIGHTCYAN_EX}This tool allows you to ask questions about your codebase and get detailed explanations or code snippets in response.{Style.RESET_ALL}")
print(f"{Fore.LIGHTCYAN_EX}You can choose to see the response formatted or raw answer.{Style.RESET_ALL}")
print(f"{Fore.LIGHTGREEN_EX}It is recommended to use the formatted output for better readability.{Style.RESET_ALL}")
print(f"{Fore.LIGHTGREEN_EX}It is recommended to use the Raw output for Codes.{Style.RESET_ALL}")

print(f"{Fore.LIGHTYELLOW_EX}Please wait while the agents are initializing...{Style.RESET_ALL}")
#####


from sub.retrival import scan_and_load_codebase
from sub.reader import stream_response

def main():
    path_prompt = f"{Fore.CYAN}Enter the path to your codebase (default is current directory): {Style.RESET_ALL}"
    path = input(path_prompt).strip() or "."

    print(f"{Fore.LIGHTYELLOW_EX}Indexing codebase... this may take a moment.{Style.RESET_ALL}")
    try:
        retrieval_chain = scan_and_load_codebase(path=path)
    except Exception as e:
        print(f"{Fore.RED}Failed to index codebase: {e}{Style.RESET_ALL}")
        return

    while True:
        question_prompt = f"\n{Fore.CYAN}Ask a question about the codebase (or type 'exit' to quit): {Style.RESET_ALL}"
        question = input(question_prompt).strip()
        
        if not question:
            continue
        if question.lower() in ['exit', 'quit']:
            break

        do_format = input(f"{Fore.GREEN}Do you want formatted/raw output? (y/n): {Style.RESET_ALL}").lower()

        if do_format == 'y':            
            stream_response(retrieval_chain, question)
        else:
            
            print(f"{Fore.YELLOW}Thinking...{Style.RESET_ALL}")
            response = retrieval_chain.invoke({"input": question})
            print(f"\n{Fore.WHITE}{response.get('answer')}")

if __name__ == "__main__":
    main()