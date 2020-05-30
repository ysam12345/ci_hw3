

class Recorder():
    def __init__(self):
        self.records = []

    def to_file(self):
        with open("../outputs/train4D.txt", "w") as f4d, open("../outputs/train6D.txt", "w") as f6d:
            for r in self.records:
                f4d.write(" ".join(r[2:]) + "\n")
                f6d.write(" ".join(r) + "\n")
        #print("Records Wrote to file.")

    def add(self, car):
        r = list(map(lambda x: str(x), [car.loc()[0], car.loc()[1], car.sensor_dist['f'],
                                        car.sensor_dist['fr'], car.sensor_dist['fl'], car.steering_wheel_degree]))
        self.records.append(r)
        #print("Records Added {}".format(self.records[-1]))

    def get(self):
        return self.records

    def clean(self):
        self.records = []
