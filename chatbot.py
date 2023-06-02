import json
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

with open("data.json") as file:
	data = json.load(file)

class ChatBot:
    nama=""
    resp = []
    label = []
    prodi = []
    alt = {}
    fact = []   

    for intent in data['intents']:
        label.append(intent['tag'].lower())
        resp.append(intent['responses'])
    for fak in data['programstudi']:
        for prod in fak['prodi']:
            prodi.append(prod)
    for alter in data['alternatives']:
        label.append(alter['tag'])
        alt[alter['tag']] = alter['alt']
    
    def __init__(self, nama):
        self.nama = nama
    
    def get_response(self, str):
        #create stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        
        #parsing
        inp = re.sub(r'[^a-zA-Z]','', str)
        inp = stemmer.stem(inp)
        inp = inp.lower().split(' ')

        #phrase check
        del_list =[]
        for i in range(len(inp)):
            if inp[i] == "sistem" and inp[i+1] == "informasi":
                inp.append(inp[i]+inp[i+1])
                del_list.append(inp[i])
                del_list.append(inp[i+1])
            if inp[i] == "filsafat" and inp[i+1] == "keilahian":
                inp.append(inp[i]+inp[i+1])
                del_list.append(inp[i])
                del_list.append(inp[i+1])
            if inp[i] == "desain" and inp[i+1] == "produk":
                inp.append(inp[i]+inp[i+1])
                del_list.append(inp[i])
                del_list.append(inp[i+1])
            if inp[i] == "bahasa" and inp[i+1] == "inggris":
                inp.append(inp[i]+inp[i+1])
                del_list.append(inp[i])
                del_list.append(inp[i+1])
            for j in range(len(inp[i:])):
                if inp[i] == "harga" and inp[j] == "sks":
                    inp.append(inp[i]+inp[j])
                    del_list.append(inp[i])
                    del_list.append(inp[j])
                    break
        for i in inp:
            if i in del_list:
                inp.remove(i)

        #fact listing
        self.fact=[]
        for i in inp:
            if i in self.label or i in self.prodi:
                self.fact.append(i)
        
        #chaining
        fact_temp=[]
        while fact_temp != self.fact:
            fact_temp = self.fact
            for i in self.fact:
                if i in self.prodi and i != "informatika":
                    self.fact.remove(i)
                    if "prodiLain" not in self.fact:
                        self.fact.append("prodiLain")
            if 'dpfp' in self.fact and 'spp' in self.fact and 'hargasks' in self.fact:
                if 'biaya' not in self.fact:
                    self.fact.append('biaya')
                self.fact.remove('dpfp')
                self.fact.remove('spp')
                self.fact.remove('hargasks')

        #getting response
        for i in self.fact:
            if i in self.label:
                return self.resp[self.label.index(i)]
        else:
            return "Maaf kami tidak mengetahui jawaban dari pertanyaanmu, silahkan hubungi admisi di ig:@pmbukdwjogja, atau ke kantor Admisi & Promosi di Gedung Agape UKDW"