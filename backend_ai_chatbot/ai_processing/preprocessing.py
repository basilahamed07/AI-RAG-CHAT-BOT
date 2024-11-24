from langchain_community.document_loaders.csv_loader import CSVLoader
loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
pages = loader.load_and_split()


def csv_loader(file_path):
    loader = CSVLoader(file_path=file_path)
    pages = loader.load_and_split()
    return pages