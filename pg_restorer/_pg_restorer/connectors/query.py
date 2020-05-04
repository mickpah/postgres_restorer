class Query:
    # execute no return query
    def execute(self, query: str, params: dict = None):
        print(f'execute -> {query}')

    # execute query returning multiple results
    def fetch(self, query: str, params: dict = None):
        print(f'fetch -> {query}')

    # execute query returning single result
    def fetch_first(self, query: str, params: dict = None):
        print(f'fetch_first -> {query}')
