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


#import files
from .rank_bm import rank_bm25
from .dataframe import dataframe_converter
from .question_answering_pipleline import Question_Answering_Pipline
from .question_generation_pipeline import Question_Generation_Pipline


'''====================================================
            itsLasagne pipeline
======================================================= '''


class itsLasagne:

    def __init__(self, context=None, question=None, model=1, para_min_length=200, para_threshold=2, include_line_breaks=True):
        self.context = context
        self.question = question
        self.model = model
        self.para_min_length = para_min_length
        self.para_threshold = para_threshold
        self.include_line_breaks = include_line_breaks
        self.cdqa = {'Question': question}

    def generate_answer(self, context=None, question=None):
        selected_context = None
        if context != None:
          self.context = context
        if self.context == None:
          return {"Error_encountered": "Please Give a Context to the Question"}

        if question != None:
          self.question = question
          self.cdqa['Question'] = question
        if self.question == None:
          return {"Error_encountered": "Please Give a Question to Answer"}

        #preprocess the context
        df_converter = dataframe_converter(
            self.para_min_length, self.include_line_breaks)
        paragraph_list = df_converter.paragraph_df_converter(self.context)

        #intilize rank_bm25 searching
        search_engine = rank_bm25(
            [self.question], paragraph_list, self.para_threshold)
        selected_context, bm_1_idx = search_engine.select_context()

        # error handling
        if selected_context == '':
          self.cdqa['Answer'] = "Answer Not Found in the given context, Add more details or perform online search!!"
          return self.cdqa

        self.cdqa['Answer_Paragraph'] = selected_context
        self.cdqa['Paragraph_Numbers'] = bm_1_idx

        self.cdqa['Answer'] = self.answer_pipeline(
            self.context, self.question, self.model)

        return self.cdqa

    def doc_generate_answer(self, directory_path=None, question=None):
        selected_context = None
        if directory_path == None:
          return {"Error_encountered": "Please Give a Directory Path to the PDFs"}

        if question != None:
          self.question = question
          self.cdqa['Question'] = question
        if self.question == None:
          return {"Error_encountered": "Please Give a Question to answer"}

        #preprocess the Pdf for context
        df_converter = dataframe_converter(
            self.para_min_length, self.include_line_breaks)
        para_dataframe = df_converter.pdf_df_converter(directory_path)

        #intilize rank_bm25 searching
        answer = {
            'doc_name': [],
            'para_id': [],
            'answer_para': []
        }
        for ele in para_dataframe.index:
          search_engine = rank_bm25(
              [self.question], para_dataframe['paragraphs'][ele], self.para_threshold)
          selected_context, bm_1_idx = search_engine.select_context()
          if selected_context != '':
            answer['doc_name'].append(para_dataframe['title'][ele])
            answer['para_id'].append(bm_1_idx)
            answer['answer_para'].append(selected_context)

        # error handling
        if len(answer['para_id']) == 0:
          self.cdqa['Answer'] = "Answer Not Found in the given context, Add more details or perform online search!!"
          return self.cdqa

        if len(answer['para_id']) == 1:
          self.cdqa['Answer_Paragraph'] = answer['answer_para'][0]
          self.cdqa['Document_name'] = answer['doc_name'][0]
          self.cdqa['Paragraph_Numbers'] = answer['para_id'][0]
        else:
          search_engine = rank_bm25(
              [self.question], answer['answer_para'], self.para_threshold)
          self.cdqa['Answer_Paragraph'], idx = search_engine.select_context()
          self.cdqa['Document_Name'] = answer['doc_name'][int(idx)]
          self.cdqa['Paragraph_Numbers'] = answer['para_id'][int(idx)]

        self.context = self.cdqa['Answer_Paragraph']
        self.cdqa['Answer'] = self.answer_pipeline(
            context=self.context, question=self.question, model=self.model)
        if self.cdqa['Answer'] == None:
           self.cdqa['Answer'] = "Answer Not Found in the given context, Add more details or perform online search!!"

        return self.cdqa
