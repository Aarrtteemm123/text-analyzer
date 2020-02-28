import os, re
from multiprocessing import Process, Manager


class Analyzer(object):
    def __init__(self, num_proc, path_to_data):
        self.num_proc = num_proc
        self.path_to_data = path_to_data
        self.global_lst = Manager().list()
        self.topic_lst = os.listdir(path_to_data)
        if ((len(self.topic_lst) / num_proc) -
                (len(self.topic_lst) // num_proc) != 0):
            self.size_group = (len(os.listdir(path_to_data)) // num_proc) + 1
        else:
            self.size_group = (len(os.listdir(path_to_data)) // num_proc)
        for i in range(len(self.topic_lst)): self.global_lst.append([10])

    def analyzer(self, index_process):
        for i in range(self.size_group * index_process,
                       self.size_group * (index_process + 1)):
            buffer_str = ""
            if i < len(self.topic_lst):
                filename_lst = os.listdir(self.path_to_data + '/' + self.topic_lst[i])
                for text in filename_lst:
                    with open(self.path_to_data + '/' + self.topic_lst[i] + '/' + text, 'r') as file:
                        buffer_str += file.read().lower()
                words_lst = re.split(r'\W| ', buffer_str)
                words_lst = list(set(words_lst))
                words_lst = list(filter(None, words_lst))
                self.global_lst[i] = words_lst

    def determine_topic(self, filename):
        buffer_str = ""
        with open(filename, 'r') as file:
            buffer_str = file.read().lower()
        words_lst = re.split(r'\W| ', buffer_str)
        words_lst = list(set(words_lst))
        words_lst = list(filter(None, words_lst))
        result_lst = [0 for i in range(len(self.topic_lst))]
        for index_topic in range(len(self.topic_lst)):
            result_lst[index_topic] = len(self.global_lst[index_topic]) - \
                                      len(set(self.global_lst[index_topic]) - set(words_lst))
        return self.topic_lst[result_lst.index(max(result_lst))]

    def start_process(self):
        proc_lst = [Process(target=self.analyzer, args=(i,)) for i in range(self.num_proc)]
        for i in proc_lst: i.start()
        for i in proc_lst: i.join()
