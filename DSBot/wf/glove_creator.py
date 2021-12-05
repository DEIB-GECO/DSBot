#import bcolz
import pickle
import numpy as np

# words = []
# idx = 0
# word2idx = {}
# vectors = []#bcolz.carray(np.zeros(1), rootdir=f'glove_new_300_dat.txt', mode='w')
#
# with open(f'glove_new_300.txt', 'rb') as f:
#     f.readline()
#     for l in f:
#         line = l.decode().split()
#         word = line[0]
#         words.append(word)
#         word2idx[word] = idx
#         idx += 1
#         vect = np.array(line[1:]).astype(np.float)
#         vectors.append(vect)
#
# vectors = np.asarray(vectors)
#
# #vectors = bcolz.carray(vectors[1:].reshape((idx, 300)), rootdir=f'glove_new_300.dat', mode='w')
# #vectors.flush()
# pickle.dump(vectors, open(f'./glove/glove_new_300_dat.pkl', 'wb'))
# pickle.dump(words, open(f'./glove/glove_new_300_words.pkl', 'wb'))
# pickle.dump(word2idx, open(f'./glove/glove_new_300_idx.pkl', 'wb'))

vectors = pickle.load(open(f'./glove/glove_new_300_dat.pkl', 'rb'))
words = pickle.load(open(f'./glove/glove_new_300_words.pkl', 'rb'))
word2idx = pickle.load(open(f'./glove/glove_new_300_idx.pkl', 'rb'))

glove = {w: vectors[word2idx[w]] for w in words}
with open('./glove/glove_new_300.txt', 'w') as f:
    for k,v in glove.items():
        f.write(k)
        f.write(' ')
        f.write(' '.join(map(str, v)))
        f.write('\n')
