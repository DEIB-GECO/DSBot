from mlxtend.frequent_patterns import apriori, association_rules

class APriori:
    def __init__(self, dataset):
        self.ds = dataset

    def run(self):
        freq_items = apriori(self.ds.dataset, min_support=0.05, use_colnames=True, verbose=1)
        rules = association_rules(freq_items, metric="confidence", min_threshold=0.6)
        return rules
