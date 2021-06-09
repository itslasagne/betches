import requests
# from googlesearch import search
import bs4
import numpy as np
import re
import os
from tika import parser
import pandas as pd


#transformer models
import torch
from transformers import(
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
)


'''====================================================
              Question Generation Models
======================================================= '''


class Question_Generation_Pipline:

    def __init__(self, context=None, domain=False, para_min_length=200, para_threshold=2, include_line_breaks=True):
        self.context = context
        self.domain = domain
        self.para_min_length = para_min_length
        self.para_threshold = para_threshold
        self.include_line_breaks = include_line_breaks
