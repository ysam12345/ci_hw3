class Dataset():
    def __init__(self, file_path):
        self.file_path = file_path
        self.datasets = []
        self.load_data()

    def load_data(self):
        with open(self.file_path) as f:
            data = f.readlines()
        for i in range(len(data)):
            d = list(
                map(lambda x: float(x), data[i].replace('\n', '').split(' ')))
            dataset = {
                'X': d[:-1],
                'y': d[-1]
            }
            self.datasets.append(dataset)
    def get(self):
        return self.datasets

if __name__ == "__main__":
    d = Dataset('../data/train4dAll.txt')
    print(d.get())
    d = Dataset('../data/train6dAll.txt')
    print(d.get())

