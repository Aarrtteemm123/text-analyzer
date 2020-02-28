import os

from analyzer import Analyzer

# 49960 -> alt.atheism
if __name__ == '__main__':
    num_proc = os.cpu_count()
    path_to_data = "20_newsgroups"
    analyzer = Analyzer(os.cpu_count(), path_to_data)
    analyzer.start_process()
    print(analyzer.determine_topic('49960'))
