from document_search import search_pdf_folder

folder = input("Enter folder path: ").strip().strip('"')
query = input("Enter keyword or phrase: ")

results = search_pdf_folder(folder, query)

if isinstance(results, dict) and "error" in results:
    print(results["error"])

elif not results:
    print("No matching documents found.")

else:
    print(f"\nFound {len(results)} matching page(s):\n")

    for result in results:
        print(f"File: {result['file']}")
        print(f"Page: {result['page']}")
        print(f"Match: {result['match']}")
        print(f"Path: {result['path']}")
        print("-" * 40)