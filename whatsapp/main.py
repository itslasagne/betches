from pipelines import pipeline
import json
from flask import Flask, request

#conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
print("Pipeline is being loaded....")
model = pipeline("multitask-qa-qg")
print("Pipeline is loaded....")

app = Flask(__name__)

# <form method="POST">
#     TEXT: <input type="text" name="pdfText"><br>
#     <input type="submit" value="Submit"><br>
# </form>

@app.route('/getAnwers', methods = ['GET']) 
def getAnswers():
    if request.method == "GET":
        # text = request.form.get('pdfText')
        # questionToBeAsked = request.form.get('question')
# ipl = "The 2020 Indian Premier League, also known as IPL 13 and branded as Dream11 Indian Premier League 2020, was the thirteenth season of the IPL, a professional Twenty20 cricket (T20) league established by the Board of Control for Cricket in India (BCCI) in 2007. \
# The tournament was originally scheduled to commence on 29 March 2020, but was suspended until 15 April due to the global coronavirus pandemic. \
# After Indian Prime Minister Narendra Modi announced on 14 April that the lockdown in India would last until at least 3 May 2020, the BCCI suspended the tournament indefinitely. \
# On 2 August 2020, it was announced that the tournament would be played between 19 September and 10 November 2020 in the United Arab Emirates. \
# On 4 August 2020, Vivo pulled out as the title sponsor of the Indian Premier League (IPL) for this year's edition. \
# On 18 August, fantasy cricket league platform Dream11 was named the title sponsor with a bid of ₹222 crore (US$31 million) for the tournament. \
# Mumbai Indians were the defending champions, and they successfully defended their title following a 5 wicket win over Delhi Capitals in the final on 10 November, 2020. And Princeton is Chutiya of the century"

        text = "Question answering (QA) is a challenging task and has received considerable attention in the last years since it has assumed a central role in the next generation of both digital assistants, like Siri, Google Assistant, Alexa, and Cortana, as well as of cognitive systems like Watson [1]. QA systems have been actively studied to automatically answer with either short facts or long passages to natural language questions issued by users in different languages, in contrast to search engines, able to return a collection of related documents given some keywords. Even though there are many variations in the proposed QA systems [2-4], typical QA systems adopt a pipeline architecture that incorporates three major phases: (1) question processing; (2) information retrieval; (3) answer selection"
        questionToBeAsked = "what is the phases of architecture of QA?"

        print("Model is Searching your Answer....")

        answer = model({
                "question" : questionToBeAsked,
                "context" : text
            })

        return f"{answer}"

@app.route('/getQuestions', methods = ['GET']) 
def getQuestions():
    if request.method == "GET":
        # text = request.form.get('pdfText')
        text = "Question answering (QA) is a challenging task and has received considerable attention in the last years since it has assumed a central role in the next generation of both digital assistants, like Siri, Google Assistant, Alexa, and Cortana, as well as of cognitive systems like Watson [1]. QA systems have been actively studied to automatically answer with either short facts or long passages to natural language questions issued by users in different languages, in contrast to search engines, able to return a collection of related documents given some keywords. Even though there are many variations in the proposed QA systems [2-4], typical QA systems adopt a pipeline architecture that incorporates three major phases: (1) question processing; (2) information retrieval; (3) answer selection"
        
        print("Model is generating your Questions....")
        qANDa = model(text)
        
        questions = []
        answers = []
        for index in range(len(qANDa)):
            questions.append(qANDa[index]["question"])
            answers.append(qANDa[index]["answer"])

        returnData = {
            "questions" : questions,
            "answer" : answers
        }

        return json.dumps(returnData)

if __name__ == '__main__':
    app.run(port=5050 ,debug = True)