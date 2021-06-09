import requests
# from googlesearch import search
import bs4
import numpy as np
import re
import os
from tika import parser
import pandas as pd

#download nltk-stopwords
import nltk
nltk.download("stopwords") 
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


'''====================================================
            Convert Multiple pdfs to dataframe
======================================================= '''


class dataframe_converter:
    
    def __init__(self, para_min_length= 200, include_line_breaks=False):
        self.para_min_length = para_min_length
        self.include_line_breaks = include_line_breaks

    def paragraph_df_converter(self, context):
        paragraphs = re.split("\n\n(?=\u2028|[A-Z-0-9])", context)
        paragraph_list = []
        temp_para = ""
        for p in paragraphs:
            if not p.isspace():
                if self.include_line_breaks:
                    if len(p) >= self.para_min_length:
                        if temp_para:
                            paragraph_list.append(temp_para.strip())
                            temp_para = ( "" )
                            paragraph_list.append( p.replace("\n", "") )
                        else:
                            paragraph_list.append(p.replace("\n", ""))
                    else:
                        line = p.replace("\n", " ").strip()
                        temp_para = temp_para + f" {line}"
                else:
                    paragraph_list.append(p.replace("\n", ""))
            else:
                if temp_para:
                    paragraph_list.append(temp_para.strip())

        return paragraph_list


    def pdf_df_converter(self,directory_path):
        list_file = os.listdir(directory_path)
        list_pdf = []
        for file in list_file:
            if file.endswith("pdf"):
                list_pdf.append(file)
        df = pd.DataFrame(columns=["title", "paragraphs"])
        for i, pdf in enumerate(list_pdf):
            try:
                df.loc[i] = [pdf.replace(".pdf", ''), None]
                raw = parser.from_file(os.path.join(directory_path, pdf))
                raw_context = raw["content"].strip()

                df.loc[i, "paragraphs"] = self.paragraph_df_converter(raw_context)
            except:
                print("Unable to process file {}".format(pdf))
        return df