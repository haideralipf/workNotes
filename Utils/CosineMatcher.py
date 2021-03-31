#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 10:08:22 2021

@author: haiderali
"""
import re
import pickle
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from sklearn.feature_extraction.text import TfidfVectorizer


names_list = []
    
def get_list():
    global names_list
    #read dataset here
    with open('name_data', 'rb') as fp:
        names_list = pickle.load(fp)
        return names_list
            
def ngrams(string, n=2):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]
        
def awesome_cossim_top(A, B, ntop, lower_bound=0):
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)
    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)
    return csr_matrix((data,indices,indptr),shape=(M,N))
    
def get_matches_vals(sparse_matrix, A, B, top=100):
    non_zeros = sparse_matrix.nonzero()
    
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]
    
    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size
    
    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)
    
    for index in range(0, nr_matches):
        left_side[index] = A[sparserows[index]]
        right_side[index] = B[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]
    
    return {'left_side': left_side,
            'right_side': right_side,
             'similairity': similairity}
    
def get_matched_string(list_of_name):
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
    tf_idf_matrix_clean = vectorizer.fit_transform(names_list)
    tf_idf_matrix_dirty = vectorizer.transform(list_of_name)
    matches = awesome_cossim_top(tf_idf_matrix_dirty, tf_idf_matrix_clean.transpose(), 10, 0.85)
    matched_vals = get_matches_vals(matches, list_of_name, names_list, top = 0)
    return matched_vals
        

def get_highest_predicted_name(names):
    get_list()
    matched_dictionary = {}
    list_of_vals = []
    vals = get_matched_string(names)
    for k, v in vals.items():
        list_of_vals.append(list(v))
        
    result = [[list_of_vals[j][i] for j in range(len(list_of_vals))] for i in range(len(list_of_vals[0]))]
    for item in result:
        if not item[0] in matched_dictionary.keys():
            matched_dictionary[item[0]] = (item[1], item[2]) 
            
    return matched_dictionary
    
    
    
if __name__ == '__main__':
    vals = get_highest_predicted_name(['list', 'of', 'documents'])
    print(vals)
    