import pandas as pd
import pdfplumber

class FileLoader:

    @staticmethod
    def load_csv(path):
        df = pd.read_csv(path)
        return FileLoader._df_to_text(df)

    @staticmethod
    def load_excel(path):
        df = pd.read_excel(path)
        return FileLoader._df_to_text(df)

    @staticmethod
    def _df_to_text(df):
        text_lines = []

        for _, row in df.iterrows():
            line = " ".join(str(x) for x in row if str(x) != "nan")
            text_lines.append(line)

        return "\n".join(text_lines)

    @staticmethod
    def load_pdf(path):
        text = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")

        return "\n".join(text)