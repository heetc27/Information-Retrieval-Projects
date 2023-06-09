from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)

class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self, postlist1, postlist2, skip):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        comp = 0
        posting_list1 = postlist1
        posting_list2 = postlist2
        pl1 = posting_list1.start_node
        pl2 = posting_list2.start_node
        if skip==0:
            merged_list = LinkedList()
            if posting_list1 is not None and posting_list2 is not None:
                while pl1 and pl2:
                    if pl1.value == pl2.value:
                        idf = max(pl1.tf_idf, pl2.tf_idf)
                        merged_list.insert_at_end(idf,pl1.value)
                        pl1 = pl1.next
                        pl2 = pl2.next
                    elif pl1.value < pl2.value:
                        pl1 = pl1.next
                    else:
                        pl2 = pl2.next
                    comp += 1
        else:
            merged_list = LinkedList()
            if (posting_list1 is not None and posting_list2 is not None):
                while pl1 and pl2:
                    comp += 1
                    if pl1.value == pl2.value:
                        idf = max(pl1.tf_idf, pl2.tf_idf)
                        merged_list.insert_at_end(idf,pl1.value)
                        pl1 = pl1.next
                        pl2 = pl2.next
                    elif pl1.value < pl2.value:
                        if pl1.skip and (pl1.skip.value <= pl2.value):
                            while pl1.skip and (pl1.skip.value <= pl2.value):
                                pl1 = pl1.skip
                        else:
                            pl1 = pl1.next
                    elif pl2.skip and (pl2.skip.value <= pl1.value):
                        while pl2.skip and (pl2.skip.value <= pl1.value):
                            pl2 = pl2.skip
                    else:
                        pl2 = pl2.next
        merged_list.add_skip_connections()
        return merged_list, comp

    def _daat_and(self, qlist, skip, addSort):
        merged_list = None
        query_dict={}
        query_list = []
        for q in qlist:
            query_dict[q]= self.indexer.inverted_index[q].length
        for k,v in sorted(query_dict.items(), key=lambda item: item[1]):
            query_list.append(k)
        nt = len(query_list)
        tot_comp = 0
        if nt==1:
            pl = self._get_postings(query_list[0])
            return pl
        else:
            for i in range(1, nt):
                if (merged_list):
                    merged_list, comp = self._merge(merged_list, self.indexer.inverted_index[query_list[i]], skip)
                    tot_comp = comp + tot_comp
                else:
                    merged_list, comp = self._merge(self.indexer.inverted_index[query_list[i-1]],self.indexer.inverted_index[query_list[i]], skip)
                    tot_comp = comp + tot_comp
        term_dict = {}
        tt = merged_list.start_node
        while tt:
            term_dict[tt.value] = tt.tf_idf
            tt=tt.next
        if (addSort):
            m_res = []
            for k,v in sorted(term_dict.items(), key=lambda item: item[1], reverse=True):
                m_res.append(k)
            return m_res,tot_comp
        return merged_list.traverse_list(), tot_comp

    def _get_postings(self,term,skippoint):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        postings_list = []
        if (term in self.indexer.inverted_index):
            if not skippoint:
                postings_list=self.indexer.inverted_index[term].traverse_list()
            else:
                postings_list=self.indexer.inverted_index[term].traverse_skips()
        return postings_list

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)

        self.indexer.sort_terms()
        print("inverted indices: ")
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf()

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers,
                    along with sorting by tf-idf scores."""
            input_term_arr = self.preprocessor.tokenizer(query)

            for term in input_term_arr:
                postings = self._get_postings(term, False)
                skip_postings = self._get_postings(term, True)

                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""
                postings = self._get_postings(term, False)
                skip_postings = self._get_postings(term, True)

                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            and_op_no_skip, and_comparisons_no_skip = self._daat_and(input_term_arr, False, False)
            and_op_skip,and_comparisons_skip        = self._daat_and(input_term_arr, True, False)
            and_op_no_skip_sorted, and_comparisons_no_skip_sorted = self._daat_and(input_term_arr, False, True)
            and_op_skip_sorted, and_comparisons_skip_sorted =  self._daat_and(input_term_arr, True, True)

            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)

if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--queries", type=str, help="Queries File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")
    argv = parser.parse_args()

    corpus = argv.corpus
    queries = argv.queries
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)