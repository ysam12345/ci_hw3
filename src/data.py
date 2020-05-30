class Data():
    def __init__(self, file_path):
        self.file_path = file_path
        self.start_point = []
        self.start_degree = 0
        self.finish_area = []
        # finish_area[0] => upper_left
        # finish_area[i] => button_right
        self.road_edges = []
        self.load_data()

    def load_data(self):
        with open(self.file_path) as f:
            data = f.readlines()
        for i in range(len(data)):
            d = list(
                map(lambda x: int(x), data[i].replace('\n', '').split(',')))
            if i == 0:
                self.start_point = d[:2]
                self.start_degree = d[2]
            elif i == 1 or i == 2:
                self.finish_area.append(d)
            else:
                self.road_edges.append(d)

    def get(self):
        return {
            "start_point": self.start_point,
            "start_degree": self.start_degree,
            "finish_area": self.finish_area,
            "road_edges": self.road_edges
        }


if __name__ == "__main__":
    d = Data('../cases/case01.txt')
    print(d.get())
