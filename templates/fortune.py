import string

def create_positional_index(documents):
    positional_index = {}
    for doc_id, text in enumerate(documents):
        # Convert text to lowercase and remove punctuation
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        for pos, word in enumerate(words):
            if word not in positional_index:
                positional_index[word] = {}
            if doc_id not in positional_index[word]:
                positional_index[word][doc_id] = []
            positional_index[word][doc_id].append(pos)
    return positional_index

def handle_phrase_query(phrase, positional_index):
    # Normalize the input phrase
    phrase = ' '.join(phrase.lower().split())
    words = phrase.split()

    if words[0] not in positional_index:
        return []

    candidate_docs = set(positional_index[words[0]].keys())
    for word in words[1:]:
        if word not in positional_index:
            return []
        candidate_docs &= set(positional_index[word].keys())

    matching_docs = []
    for doc_id in candidate_docs:
        positions = [positional_index[word][doc_id] for word in words]
        for start_pos in positions[0]:
            if all(start_pos + i in positions[i] for i in range(1, len(words))):
                matching_docs.append(doc_id)
                break
    return matching_docs

def handle_proximity_query(term1, term2, max_distance, positional_index):
    term1, term2 = term1.lower(), term2.lower()

    if term1 not in positional_index or term2 not in positional_index:
        return []

    candidate_docs = set(positional_index[term1].keys()) & set(positional_index[term2].keys())
    matching_docs = []

    for doc_id in candidate_docs:
        positions1 = positional_index[term1][doc_id]
        positions2 = positional_index[term2][doc_id]

        for pos1 in positions1:
            if any(abs(pos1 - pos2) <= max_distance for pos2 in positions2):
                matching_docs.append(doc_id)
                break
    return matching_docs

if __name__ == "__main__":
    default_documents = [
        "The quick brown fox jumps over the lazy dog.",
        "The lazy dog sleeps.",
        "A quick brown dog outpaces a quick fox."
    ]

    print("Enter the number of documents:")
    num_docs = int(input().strip())

    if num_docs == 0:
        documents = default_documents
    else:
        documents = []
        for i in range(num_docs):
            print(f"Enter document {i + 1}:")
            documents.append(input().strip())

    positional_index = create_positional_index(documents)
    print("\nGenerated Positional Index:")
    for term, doc_info in positional_index.items():
        print(f"{term}: {doc_info}")
    
    while True:
        print("\nSelect a query type:")
        print("1. Phrase Query")
        print("2. Proximity Query")
        print("3. Exit")
        choice = int(input().strip())

        if choice == 1:
            print("Enter your phrase query:")
            phrase = input().strip()
            results = handle_phrase_query(phrase, positional_index)
            print(f"Documents matching the phrase '{phrase}': {results}")

        elif choice == 2:
            print("Enter the first term:")
            term1 = input().strip()
            print("Enter the second term:")
            term2 = input().strip()
            print("Enter the maximum proximity (k):")
            max_distance = int(input().strip())
            results = handle_proximity_query(term1, term2, max_distance, positional_index)
            print(f"Documents where '{term1}' and '{term2}' are within {max_distance} positions: {results}")

        elif choice == 3:
            print("Exiting the program.")
            break

        else:
            print("Invalid selection. Please try again.")
