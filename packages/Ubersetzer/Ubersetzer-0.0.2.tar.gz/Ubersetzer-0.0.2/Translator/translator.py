from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import os
import string
from pathlib import Path
class eng_deu:
    BASE_DIR = Path(__file__).resolve().parent
    def __init__(self) -> None:
        self.model = load_model(os.path.join(self.BASE_DIR,'arpanKaModel'))

        with open(os.path.join(self.BASE_DIR,'deu_tokenizer.pickle'), 'rb') as handle:
            self.deu_tokenizer = pickle.load(handle)

        with open(os.path.join(self.BASE_DIR,'eng_tokenizer.pickle'), 'rb') as handle:
            self.eng_tokenizer = pickle.load(handle)

    def encode_sequences(self,tokenizer, length, lines):
        seq = tokenizer.texts_to_sequences(lines)
        seq = pad_sequences(seq, maxlen=length, padding='post')
        return seq

    def translate(self, sentence):
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = sentence.lower()
        sentence = np.array([sentence])
        testX = self.encode_sequences(self.deu_tokenizer, 8, sentence)
        preds = np.argmax(self.model.predict(testX), axis=-1)
        preds_text = []
        for i in preds:
            temp = []
            for j in range(len(i)):
                t = self.get_word(i[j], self.eng_tokenizer)
                if j > 0:
                    if (t == self.get_word(i[j-1], self.eng_tokenizer)) or (t == None):
                        temp.append('')
                    else:
                        temp.append(t)
                else:
                    if(t == None):
                        temp.append('')
                    else:
                        temp.append(t)
            preds_text.append(' '.join(temp))
        return preds_text[0]


    def get_word(self,n, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == n:
                return word
        return None

    
