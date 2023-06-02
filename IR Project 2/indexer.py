from linkedlist import LinkedList
from collections import OrderedDict

class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self,doc_id,tokenized_document):
        tf_val = {}
        length = len(tokenized_document)
        for term in tokenized_document:
            if (term not in tf_val):
                tf_val[term] = 1
            else:
                tf_val[term] += 1
        for term in tf_val:
            self.add_to_index(term, doc_id, tf_val[term]/length)

    def add_to_index(self,term_,doc_id_,tf_):
        term = term_
        docid = doc_id_
        tf = tf_
        if (term not in self.inverted_index):
            self.inverted_index[term] = LinkedList()
            self.inverted_index[term].insert_at_end(tf,docid)
        else:
            current_docids = self.inverted_index[term].traverse_list()
            if(docid not in current_docids):
                self.inverted_index[term].insert_at_end(tf,docid)
        return

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for key in sorted(self.inverted_index.keys()):
            sorted_index[key] = self.inverted_index[key]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for key in self.inverted_index:
            self.inverted_index[key].add_skip_connections()

    def calculate_tf_idf(self):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        total_docs_length = 12
        for term in self.inverted_index:
            postings_list_length = self.inverted_index[term].length
            idf_ = (total_docs_length/postings_list_length)
            self.inverted_index[term].idf= idf_
            p_list = self.inverted_index[term]
            if(p_list is not None):
                x = p_list.start_node
                while x:
                    current_tf = x.tf_idf
                    x.tf_idf = idf_ * current_tf
                    x=x.next
        return