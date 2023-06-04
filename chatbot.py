import json
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
        inp = str.lower().split(' ')
        for i in range(len(inp)):
            inp[i] = stemmer.stem(inp[i])

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
            if inp[i] == "mata" and inp[i+1] == "kuliah":
                inp.append(inp[i]+inp[i+1])
                del_list.append(inp[i])
                del_list.append(inp[i+1])
            if inp[i] == "seleksi" and inp[i+1] == "mandiri":
                inp.append(inp[i]+inp[i+1])
                del_list.append(inp[i])
                del_list.append(inp[i+1])
            if inp[i] == "seleksi" and inp[i+1] == "prestasi":
                inp.append(inp[i]+inp[i+1])
                del_list.append(inp[i])
                del_list.append(inp[i+1])
            if inp[i] == "harga" or inp[i] == "biaya" or inp[i] == "uang":
                for j in range(len(inp)):
                    if inp[j] == "sks":
                        inp.append("harga"+inp[j])
                        del_list.append(inp[i])
                        del_list.append(inp[j])
                        break
            if inp[i] == "harga" or inp[i] == "biaya" or inp[i] == "uang":
                for j in range(len(inp)):
                    if inp[j] == "matakuliah" or inp[j]=="matkul":
                        inp.append("harga"+"matkul")
                        del_list.append(inp[i])
                        del_list.append(inp[j])
                        break
            if inp[i] == "harga" or inp[i] == "biaya" or inp[i] == "uang":
                for j in range(len(inp)):
                    if inp[j] == "semester":
                        inp.append("harga"+inp[j])
                        del_list.append(inp[i])
                        del_list.append(inp[j])
                        break
            if inp[i] == "biaya":
                for j in range(len(inp)):
                    if inp[j] == "daftar":
                        inp.append(inp[i]+inp[j])
                        del_list.append(inp[i])
                        del_list.append(inp[j])
                        break
            if inp[i] == "potong":
                for j in range(len(inp)):
                    if inp[j] == "mandiri" or inp[j]=="seleksimandiri":
                        inp.append(inp[i]+"mandiri")
                        del_list.append(inp[i])
                        del_list.append(inp[j])
                        break
            if inp[i] == "potong":
                for j in range(len(inp)):
                    if inp[j] == "prestasi" or inp[j]=="seleksiprestasi":
                        inp.append(inp[i]+"prestasi")
                        del_list.append(inp[i])
                        del_list.append(inp[j])
                        break
        inp = [kata for kata in inp if kata not in del_list]

        #fact listing
        self.fact=[]
        for i in inp:
            for tag,alternates in self.alt.items():
                if i in alternates:
                    self.fact.append(tag)
            if i in self.label or i in self.prodi:
                self.fact.append(i)
        
        #chaining
        fact_temp=[]
        while fact_temp != self.fact:
            fact_temp = self.fact
            for i in self.fact:
                if i in self.prodi and i != "informatika":
                    self.fact.remove(i)
                    if "prodilain" not in self.fact:
                        self.fact.append("prodilain")

            if 'dpfp' in self.fact and 'spp' in self.fact and 'hargasks' in self.fact:
                if 'biaya' not in self.fact:
                    self.fact.append('biaya')
                self.fact.remove('dpfp')
                self.fact.remove('spp')
                self.fact.remove('hargasks')
            if 'syarat' in self.fact and 'waktu' in self.fact and 'biayadaftar' in self.fact:
                if 'daftar' not in self.fact:
                    self.fact.append('daftar')
                self.fact.remove('syarat')
                self.fact.remove('waktu')
                self.fact.remove('biayadaftar')
            
        #clear duplicates if any
        self.fact = list(set(self.fact))

        #getting response
        if  'prodilain' in self.fact:
            return self.resp[self.label.index('prodilain')]
        if 'potong' in self.fact:
            return self.resp[self.label.index('potongprestasi')]+"<br>"+self.resp[self.label.index('potongmandiri')]
        if 'daftar' in self.fact:
            return self.resp[self.label.index('syarat')]+"<br>"+self.resp[self.label.index('waktu')]+"<br>"+self.resp[self.label.index('biayadaftar')]
        if 'biaya' in self.fact:
            return self.resp[self.label.index('dpfp')]+"<br>"+self.resp[self.label.index('spp')]+"<br>"+self.resp[self.label.index('hargasks')]
        output=""
        for i in self.fact:
            if i in self.label:
                output += self.resp[self.label.index(i)]+"<br>"
        if len(output)!=0:
            return output
        else:
            return "Maaf kami tidak mengetahui jawaban dari pertanyaanmu, silahkan hubungi admisi di ig:@pmbukdwjogja, atau ke kantor Admisi & Promosi di Gedung Agape UKDW"

chatbot = ChatBot("informatika")
print(chatbot.get_response("pelajaran?"))