import pandas as pd
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import string #Opérations courantes sur les chaînes
import re   # pour utiliser  des expressions régulières ex:$
import nltk 
import joblib
#Importer le fichier excel
#fil='F:\\my_work\\Mini_projet\\data.xlsx'
data=pd.read_excel('data.xlsx')
def process(text):
# la normalisation
    regex = re.compile(r'[إأٱآا]') #sauvegarder l'expression réguliere (r=expression reguliere)
    text = re.sub(regex, 'ا', text) #remblacer des expressions par d'autres dans varia texte
    regex = re.compile(r'[ى]')
    text = re.sub(regex, 'ي', text)
    regex = re.compile(r'[ؤئ]')
    text = re.sub(regex, 'ء', text)
#supprimer les diacritiques
    arabic_diacritics = re.compile("""
                             ّ    | # Shadda
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)   #verbose: séparer visuellement les expre et ajouter des commentaires
    text = re.sub(arabic_diacritics, '', text)
    

#supprimer les ponctuations
    #liste des ponctuations arabe et anglais qu'on veut supprimer
    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''    # utiliser ''' :multiples caractére de chaine
    english_punctuations = string.punctuation              #(!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
    punctuations_list = arabic_punctuations + english_punctuations
    #table de mappage
    translator = str.maketrans('','', punctuations_list) # le 1er elem a remplacer/le 2eme le remplacement,3eme=supprimer
    text= text.translate(translator) #chaine ou les caractere sont remplacé par d'autres dns table de mappage

#supprimer les chaines répétés
    text=re.sub(r'(.)\1+', r'\1', text) 

#supprimer les mots vides
    stopwords=nltk.corpus.stopwords.words('arabic') #les mots vides en arabe
    text=[word for word in text if word not in stopwords]
    
    
    return text

data['Text'] = data['Text'].apply(process) 
#Encodage des mots dans chaque phrase sous une forme numérique
CV=CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)
text_train=CV.fit_transform(data.Text)
""" # Naive Bayes classifier                    
nb=MultinomialNB()
nb.fit(text_train,data.Tag)
joblib.dump(nb,"NB.pkl") """
"""SVM=svm.SVC()
SVM.fit(text_train,data.Tag)
joblib.dump(SVM,"svm.pkl")
rf=RandomForestClassifier()
rf.fit(text_train,data.Tag)
joblib.dump(rf,"rf.pkl")
LR=LogisticRegression(class_weight='balanced')
LR.fit(text_train,data.Tag)
joblib.dump(LR,"LR.pkl") """
with open('Files_pkl/NB.pkl','rb') as nb_cat:
    NB=joblib.load(nb_cat)
with open('Files_pkl/svm.pkl','rb') as svm_cat:
    svm=joblib.load(svm_cat)
with open('Files_pkl/rf.pkl','rb') as rf_cat:
    rf=joblib.load(rf_cat)
with open('Files_pkl/LR.pkl','rb') as lr_cat:
    LR=joblib.load(lr_cat)
""" comment=" المباحثات تحديد مجموعة من القطاعات توفر مؤهلات هامة"
print(nb.predict(CV.transform([comment]))[0]) """


def reponse(comment):
    comment=process(comment)
    methode_nb=NB.predict(CV.transform([comment]))[0]
    methode_svm=svm.predict(CV.transform([comment]))[0]
    methode_rf=rf.predict(CV.transform([comment]))[0]
    methode_lr=LR.predict(CV.transform([comment]))[0]
    return (methode_nb,methode_svm,methode_rf,methode_lr) 