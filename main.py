import re

import matplotlib.pyplot as plt
import networkx as nx
import nltk
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QFileDialog)
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import spacy



cumleler = []
cumleler_paragraf = []
cumle_liste = []

cumle_skor = []
baglanti_skor = []

nlp = spacy.load(r"C:\Users\Mehmet emin\AppData\Local\Programs\Python\Python310\Lib\site-packages\en_core_web_md\en_core_web_md-3.5.0")



class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        font = QtGui.QFont()
        font.setFamily("Noto Sans Armenian")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(350, 30, 350, 40))
        self.pushButton.setObjectName("pushButton")


        self.combo = QtWidgets.QComboBox(self.centralwidget)
        # self.combo.setGeometry(QtCore.QRect(50, 100, 50, 30))
        self.combo.setObjectName("combo")
        combo_list = ["-" * 90 + "Cümleler Arası Benzerlik Thresoldu" + "-" * 90, "0", "0.1", "0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
        self.combo.setEditable(True)
        self.combo.addItems(combo_list)
        line_edit = self.combo.lineEdit()
        line_edit.setAlignment(QtCore.Qt.AlignCenter)
        line_edit.setReadOnly(True)




        self.combo2 = QtWidgets.QComboBox(self.centralwidget)
        self.combo2.setObjectName("combo2")
        combo_list = ["-"*100+"Cümle Skor Thresoldu"+"-"*100, "0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6","0.7", "0.8", "0.9"]
        self.combo2.setEditable(True)
        self.combo2.addItems(combo_list)
        line_edit2 = self.combo2.lineEdit()
        line_edit2.setAlignment(QtCore.Qt.AlignCenter)
        line_edit2.setReadOnly(True)

        self.combo.currentIndexChanged.connect(lambda : self.get_combobox_value())


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)

        font2 = QFont()
        font2.setFamily("Arial")
        font2.setPointSize(11)

        self.textbox_metin = QtWidgets.QTextEdit(self.centralwidget)
        self.textbox_metin.setObjectName("textbox_metin")
        # self.textbox_metin.setStyleSheet("background-color: white;")
        self.textbox_metin.setFont(font2)

        self.label_text_rogue = QtWidgets.QLabel(self.centralwidget)
        self.label_text_rogue.setObjectName("label_text_rogue")
        self.label_text_rogue.setStyleSheet("background-color: white;")
        self.label_text_rogue.setFont(font2)

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.addWidget(self.pushButton)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.combo2)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textbox_metin)
        self.layout.addWidget(self.label_text_rogue)
        MainWindow.setLayout(self.layout)


        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.get_text_file)


    def get_text_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)

        if dialog.exec_():
            file_name = dialog.selectedFiles()

            if file_name[0].endswith('.txt'):
                with open(file_name[0], 'r', encoding="utf-8") as f:

                    for satir in f:
                        cumleler.append(satir.strip())

                    f.seek(0)
                    data = f.read()
                    self.ilk_paragraf = data
                    data = data.strip()
                    cumleler_paragraf = data.split(".")


                    for cumle in cumleler_paragraf:
                        cumle_liste.append(cumle)


                    # print(cumleler_paragraf)
                    # print(cumleler_paragraf[1])

                    f.close()
            else:
                pass

        self.kontrol_noktasi(cumle_liste)
        self.makeGraph()

    def yazdir_ilkskor(self):

        print("Cümle Skorları(Nümerik ve Özel isim kontrollü):")
        print(cumle_skor)
        print("-"*150)


    def kontrol_noktasi(self,cumle_liste):

        print("-"*150)
        print('Özel isimler:')

        for cumle in cumle_liste:
            sentences = nltk.sent_tokenize(cumle)
            for sentence in sentences:

                print("Sentence:"+sentence)
                regex = '\d+'
                match = re.findall(regex, sentence)
                numeric_counter = len(match)


                words = nltk.word_tokenize(sentence)
                words_count = len(words)
                propernoun_counter = 0   #Özel isim sayacı

                words = [word for word in words if word not in set(stopwords.words('english'))]
                tagged = nltk.pos_tag(words)
                for (word, tag) in tagged:
                    if tag == 'NNP':  #kelime özel isim mi?
                        propernoun_counter += 1
                        print(word)

                ozel_isim_skor = round(propernoun_counter/words_count, 2)
                numerik_skor = round(numeric_counter / words_count, 2)
                cumle_skor.append(round(ozel_isim_skor+numerik_skor, 2))
                print(ozel_isim_skor+numerik_skor)
                print("-" * 100)

        self.yazdir_ilkskor()

    def makeGraph(self):

        # print("Cümleler")
        # print(cumleler)
        # print("-" * 150)
        #
        # print("Cümleler Paragraf-Noktaya göre ayrılmış")
        # print(cumleler_paragraf)
        # print("-" * 150)
        #
        # print("Cümleler Liste")
        # print(cumle_liste)
        # print("-" * 150)


        # Stop-words ve Lemmatizer kullanarak cümleleri temizle
        stop_words = stopwords.words('english')
        lemmatizer = WordNetLemmatizer()
        clean_sentences = []

        for sentence in cumle_liste:

            sentence = sentence.lower()

            # Kelimeleri tokenize etme
            words = word_tokenize(sentence)

            # Stop-wordsleri kaldırma işlemi
            words = [word for word in words if word not in stop_words]

            # Lemmatize et
            words = [lemmatizer.lemmatize(word) for word in words]

            #Kökleri çıkarma işlemi
            # stemmer = PorterStemmer()
            # stemmed_words = [stemmer.stem(word) for word in words]

            # Temizlenmiş cümleyi listeye ekleme işlemi
            clean_sentences.append(' '.join(words))


        # TfidfVectorizer kullanarak cümleleri vektörlere dönüştür
        # vectorizer = TfidfVectorizer()
        # sentence_vectors = vectorizer.fit_transform(clean_sentences)

        #cümleleri vektörlere ayırıp benzerliğinin NLP ile tespiti
        sentence_vectors = []
        for sentence in clean_sentences:
            doc = nlp(sentence)
            vector = doc.vector
            sentence_vectors.append(vector)

        similarity_matrix = cosine_similarity(sentence_vectors)


        thresold_skor1 = float(self.secilen_deger1)
        thresold2 = self.combo2.currentText()
        thresold_skor2 = float(thresold2)
        print("Thresold 1")
        print(thresold_skor1)
        print("Thresold 2")
        print(thresold_skor2)



        # Graf oluşturma  ve gösterme
        plt.figure(figsize=(12, 6))
        G = nx.Graph()
        for i in range(len(clean_sentences)):  # daha önce bu 2 clean sentence yerinde cumle_liste yazıyodu
            for j in range(i + 1, len(clean_sentences)):
                similarity = similarity_matrix[i][j]

                # similarity benzerliği ifade eder.Arayüzden seçilen thresold değer buraya gelicek
                print(similarity)
                if similarity > thresold_skor1:
                    G.add_edge(i, j, weight=similarity,skor=round(similarity,2))

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
        nx.draw_networkx_edges(G, pos, width=3, alpha=0.5)

        # Çizgilerin üzerindeki benzerlikleri yazdırma
        labels = nx.get_edge_attributes(G, 'skor')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')
        plt.axis('off')

        #Toplam bağlantı sayısını hesaplar
        toplam_baglanti_sayisi = G.number_of_edges()
        print("Toplam bağlantı sayısı:", toplam_baglanti_sayisi)

        # Her bir düğümün bağlantı sayısını hesaplamak için
        node_baglanti_sayisi = G.degree()

        # Her bir düğümün bağlantı sayısını ekrana yazdırmak için
        for node, baglanti in node_baglanti_sayisi:
            print("Düğüm:", node, "Bağlantı Sayısı:", baglanti)
            baglanti_skor.append(round(baglanti / toplam_baglanti_sayisi, 2) / 2)

        print("Bağlanti Skorlari: " + "-" * 100)
        print(baglanti_skor)

        # Sozlüğe skor bilgilerini ekleme
        skorlar = {}
        for i in range(0, len(cumle_skor)):
            skorlar[i] = cumle_skor[i] + baglanti_skor[i]


        #Skorları düğümlere yazdırma
        i = 0
        for node, score in skorlar.items():
            x, y = pos[node]
            plt.text(x, y, f"{i+1}.Cümle Skor: {round(score,2)}", ha='center', va='center',bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
            i+=1

        plt.savefig("graf.png")

        self.pixmap = QPixmap('graf.png')
        self.label.setPixmap(self.pixmap)

        self.yazdir_cumleler(cumle_liste)


        del cumleler[0:]
        del cumle_liste[0:]
        del cumle_skor[0:]
        del baglanti_skor[0:]

    def yazdir_cumleler(self,cumleler):

        self.textbox_metin.setText(self.ilk_paragraf)

        print("-"*50+"Cümleleri Yazdırma"+"-"*100)
        for i in range(0,len(cumleler)):
            print(f"{i}"+cumleler[i])



    def get_combobox_value(self):
        self.secilen_deger1 = self.combo.currentText()
        print(self.secilen_deger1)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graf Uygulamam"))
        self.pushButton.setText(_translate("MainWindow", "Dosya Yükle"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())