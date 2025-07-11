import requests
from colorama import Fore, Style

def search_nhentai():
    print(f"{Fore.CYAN}NHentai Search{Style.RESET_ALL}")
    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        print(f"{Fore.RED}No keyword entered.{Style.RESET_ALL}")
        return []

    results = []
    page = 1
    per_page = 10
    while True:
        api_url = f"https://nhentai.net/api/galleries/search?query={keyword}&page={page}"
        try:
            resp = requests.get(api_url, timeout=20)
            if resp.status_code != 200:
                print(f"{Fore.RED}Search failed: HTTP {resp.status_code}{Style.RESET_ALL}")
                return []
            data = resp.json()
            if not data.get("result"):
                print(f"{Fore.YELLOW}No results found for: {keyword}{Style.RESET_ALL}")
                return []
            current_results = data["result"]
            print(f"\n{Fore.LIGHTCYAN_EX}Results for '{keyword}' (Page {page}):{Style.RESET_ALL}")
            for i, g in enumerate(current_results, 1):
                title = g["title"]["english"] or g["title"]["japanese"] or str(g["id"])
                print(f"{Fore.LIGHTMAGENTA_EX}{i}) {Fore.WHITE}{title} {Fore.YELLOW}[ID: {g['id']}]")
            print(f"\n{Fore.YELLOW}n: Next page | p: Previous page | e: Exit search | Numbers (comma/space sep) to select | Enter: return to main menu{Style.RESET_ALL}")
            choice = input("Choice: ").strip()
            if choice == '':
                # Return to main menu, do nothing
                return []
            elif choice.lower() in ['e', 'exit', 'q', 'quit']:
                return []
            elif choice.lower() in ['n', 'next']:
                page += 1
                continue
            elif choice.lower() in ['p', 'prev', 'previous', 'b', 'back']:
                if page > 1:
                    page -= 1
                else:
                    print(f"{Fore.RED}Already at first page.{Style.RESET_ALL}")
                continue
            else:
                # Parse numbers for selection
                import re
                selections = re.findall(r'\d+', choice)
                if not selections:
                    print(f"{Fore.RED}No valid selection. Try again.{Style.RESET_ALL}")
                    continue
                selected_galleries = []
                for sel in selections:
                    idx = int(sel)
                    if 1 <= idx <= len(current_results):
                        selected_galleries.append(str(current_results[idx-1]['id']))
                    else:
                        print(f"{Fore.YELLOW}Invalid selection: {idx}{Style.RESET_ALL}")
                return selected_galleries
        except Exception as e:
            print(f"{Fore.RED}Search error: {e}{Style.RESET_ALL}")
            return []