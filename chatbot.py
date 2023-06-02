import json

with open("intents.json") as file:
	data = json.load(file)

class ChatBot:
    nama=""
    resp = []
    label = []   
    
    def tes(self):
        for intent in data['intents']:
            self.label.append(intent['tag'])
            self.resp.append(intent['responses'])
    
    def __init__(self, nama):
        self.nama = nama
    def get_response(self, str):
        inp = str.split(' ')
        for i in inp:
            for j in self.label:
                if i == j:
                    return self.resp[self.label.index(j)]

chatbot = ChatBot('Informatika')
chatbot.tes()
print(chatbot.get_response("DPFP"))