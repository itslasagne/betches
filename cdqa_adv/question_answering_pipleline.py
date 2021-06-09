#transformer models
import time
import torch
import torch
from transformers import AlbertTokenizer, AlbertForQuestionAnswering
from transformers import pipeline as Electra_Roberta


'''====================================================
              Question Answering Models
======================================================= '''


class Question_Answering_Pipline:

    def __init__(self, context=None, question=None, model=None, **kwargs):
        self.context = context
        self.question = question
        self.model_name = model
        self.model_download()

    def model_download(self):
        if self.model_name in [None, "Huggingface"]:
          self.tokenizer = None
          self.model = pipeline("multitask-qa-qg")
        elif self.model_name == "ALBERT":
          model_name = 'ahotrod/albert_xxlargev1_squad2_512'
          self.tokenizer = AlbertTokenizer.from_pretrained(model_name)
          self.model = AlbertForQuestionAnswering.from_pretrained(model_name)
        elif self.model_name == "ELECTRA":
          model_name = "deepset/electra-base-squad2"
          self.model = Electra_Roberta(
              'question-answering', model=model_name, tokenizer=model_name)
        elif self.model_name == "ROBERTa":
          model_name = "deepset/roberta-base-squad2"
          self.model = Electra_Roberta(
              'question-answering', model=model_name, tokenizer=model_name)
        else:
          return None, "Model Not Found!! Try another model?"

    # def answer_pipeline(self, context=context, question=question, model=None):
    #     if model == "Huggingface":

    def Huggingface_model(self):
        return self.model({'question': self.question, 'context': self.context})

    def ALBERT_model(self):
        input_dict = self.tokenizer.encode_plus(
            self.question, self.context, return_tensors='pt')
        input_ids = input_dict["input_ids"].tolist()
        start_scores, end_scores = self.model(**input_dict)

        start = torch.argmax(start_scores)
        end = torch.argmax(end_scores)

        all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        answer = ''.join(all_tokens[start: end + 1]).replace('▁', ' ').strip()
        answer = answer.replace('[SEP]', '')
        return answer if answer != '[CLS]' and len(answer) != 0 else None

    def ELECTRA_model(self):
        return self.model({'question': self.question, 'context': self.context})['answer']

    def ROBERTa_model(self):
        return self.model({'question': self.question, 'context': self.context})['answer']


'''----------------------------------------------------
                    CDQA Example
------------------------------------------------------- '''

# context = "Question answering (QA) is a challenging task and has received considerable attention in the last years since it has assumed a central role in the next generation of both digital assistants, like Siri, Google Assistant, Alexa, and Cortana, as well as of cognitive systems like Watson [1]. QA systems have been actively studied to automatically answer with either short facts or long passages to natural language questions issued by users in different languages, in contrast to search engines, able to return a collection of related documents given some keywords. Even though there are many variations in the proposed QA systems [2-4], typical QA systems adopt a pipeline architecture that incorporates three major phases: (1) question processing; (2) information retrieval; (3) answer selection"
# question = 'what are the phases of QA Architecture?'
# context="ELECTRA is one of the latest classes of pre-trained Transformer models released by Google and it switches things up a bit compared to most other releases. For the most part, Transformer models have followed the well-trodden path of Deep Learning, with larger models, more training, and bigger datasets equalling better performance. ELECTRA, however, bucks this trend by outperforming earlier models like BERT while using less computational power, smaller datasets, and less training time. (In case you are wondering, ELECTRA is the same “size” as BERT)."
# question="What is electra?"

# start = time.time()

# #Huggingface
# cdqa = Question_Answering_Pipline(context=context, question=question, model="Huggingface")
# ans = cdqa.Huggingface_model()

# #ALBERT
# cdqa = Question_Answering_Pipline(context=context, question=question, model="ALBERT")
# ans = cdqa.ALBERT_model()

# #ELECTRA
# cdqa = Question_Answering_Pipline(context=context, question=question, model="ELECTRA")
# ans = cdqa.ELECTRA_model()

# #Roberta
# cdqa = Question_Answering_Pipline(context=context, question=question, model="ROBERTa")
# ans = cdqa.ROBERTa_model()

# print(ans, time.time()-start)
