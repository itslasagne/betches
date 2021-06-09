from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
from utils2 import fetch_reply
import requests
import re
from tika import parser
app = Flask(__name__)


users = {}

@app.route('/')
def hello():
    return "hello Princy..."

@app.route('/sms', methods = ["POST"])
def sms_reply():
    msg = request.form.get('Body')
    phone_no = request.form.get('From')

    response = MessagingResponse()
    print(users)

    if request.form.get('MediaContentType0') == 'application/pdf':
        print('------------------------')
        url = request.form.get('MediaUrl0')
        # print(f"{request.form}")
        print(f"URl : {url}")
        with open (f"C:/Users/sherw/Desktop/Twilio/{msg}","wb") as f:
            f.write(requests.get(url).content)
        
        print("File saved successfully")

        
        if msg not in users[phone_no]["pdfs"]:
            users[phone_no]["pdfs"].append(msg)

            whichOption = users[phone_no]["option"]
            if whichOption == "QuestionAnswering":
                reply = "Please Ask a Question..."
                response.message(reply)
                users[phone_no]["flag"] = 1
                

            if whichOption == "QuestionGeneration":
                print("Request is being sent")
                content =""
                file_path = f"./{msg}"
                parsed_pdf = parser.from_file(file_path)
                content = parsed_pdf["content"]
                data = re.sub("\n"," ", content)
                json_to_be_sent = {"data": data}
                # headers = {'Content-Type': 'application/json'}
                r = requests.post(url = "http://127.0.0.1:5050/getQuestions", json = json_to_be_sent)
                print("REQUEST HAS BEEN PROCESSED")
                print(r.json()) 
                output = r.json() 
                questions = output['questions']   
                answers =output['answer'] 
                txt = ""          
                for i in range(len(questions)):
                    txt += f"*Question* : {questions[i]} \n*Answer*: {answers[i]} \n\n"

                print(f"Response : {txt}")
                response.message(txt)
    elif phone_no in users.keys() and users[phone_no]["flag"] == 1:
    
        #do question answering ka stuff
        print("Request is being sent")

        print(f"This is pdf to be processed : {users[phone_no]['pdfs'][0]}")
        filepath = f"C:/Users/sherw/Desktop/Twilio/{users[phone_no]['pdfs'][0]}"
        print(f"file path is : {filepath}")
        print(f"this is question : {msg}")
        content =""
        parsed_pdf = parser.from_file(filepath)
        content = parsed_pdf["content"]
        data = re.sub("\n"," ", content)
        answering_json = {
            "pdf_text" : data,
            "question" : msg
        }
        r = requests.post("http://127.0.0.1:5050/getAnwers", json = answering_json)
        print("Output is here")
        # print(r.json()) 
        output = r.json() 
        # questions = output['questions']   
        answer =output['answer'] 
        txt = ""          
        txt += f"*Answer*: {answer['Answer']} \n\n"

        print(txt)
        users[phone_no]["flag"] = 0
        response.message(txt)
    else:
        print("Reply being generated....")

        reply , option = fetch_reply(msg,phone_no)

        if len(option) > 1:
            users[phone_no] = { "option" : option, "pdfs" : [] , "flag" : 0}

        response.message(reply)
        print("Reply has been set....")

    return str(response)


if __name__ == "__main__":
    app.run(port = 5000, debug=True)