import conllu
from collections import defaultdict as dd
numb_dict = {}

def number_of_word(sent):
    for word in sent:
        numb_dict[word['form']] = word['id']

def read(data):
    with open(data, encoding='utf-8') as f:
        sentence = f.read()
    sentence = conllu.parse(sentence)
    return sentence[0]

def dfs_verb(word, verb_groups, verb_child):
    cur_group = []
    if word.token['upos'] == 'VERB':
        cur_group.append(word.token['form'])

    for child in word.children:
        cur_child = []
        dfs_verb(child, verb_groups,cur_child)
        verb_child.extend(cur_child)
        if word.token['upos'] == 'VERB' and child.token['deprel'] != 'nsubj':
            cur_group.extend(cur_child)

    if len(cur_group) >=2:
        verb_groups.append(cur_group)

    if word.token['upos'] != 'PUNCT':
        verb_child.append(word.token['form'])

def dfs_noun(word, noun_groups, noun_child):
    cur_group = []
    if word.token['upos'] == 'NOUN' or word.token['upos'] == 'PRON':
        cur_group.append(word.token['form'])

    for child in word.children:
        cur_child = []
        dfs_noun(child, noun_groups,cur_child)
        noun_child.extend(cur_child)
        if (word.token['upos'] == 'NOUN' or word.token['upos'] == 'PRON') and child.token['deprel'] != 'nsubj':
            cur_group.extend(cur_child)

    if len(cur_group) >=2:
        noun_groups.append(cur_group)

    if word.token['upos'] != 'PUNCT':
        noun_child.append(word.token['form'])



def main():
    sent = read('input.txt')
    number_of_word(sent)
    sent = sent.to_tree()
    v_g = []
    dfs_verb(sent,v_g, [])
    n_g = []
    dfs_noun(sent, n_g,[])
    for li in v_g:
        li.sort(key = lambda word: numb_dict[word])
    for li in n_g:
        li.sort(key = lambda word: numb_dict[word])
    print('Глагольные группы:')
    for li in v_g:
        print(' '.join(li))
    print('Именные группы:')
    for li in n_g:
        print(' '.join(li))
       

if __name__ == '__main__':
    main()


