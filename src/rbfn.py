import random
from math import exp


class RBFN():
    def __init__(self, J=3, input_dim=3):
        self.J = J
        self.input_dim = input_dim
        self.theta = random.uniform(-40, 40)
        self.neurals = []
        for _ in range(self.J):
            self.neurals.append({
                'sigma': random.uniform(0, 1),
                'm': [random.uniform(0, 40) for j in range(self.input_dim)],
                'weight': random.uniform(-1, 1)
            })

    def basis_func(self, X, neural):
        # Gauss
        #[X[i]-neural['m'][i] for i in range(len(X))] 
        #print(len(neural['m']), len(X))
        return exp(-(sum([(X[i]-neural['m'][i])**2 for i in range(len(X))])**0.5)/(2*neural['sigma']**2))

    def output(self, X):
        output = 1 * self.theta
        #print(self.theta, self.neurals)
        #print(len(self.neurals))
        #print(self.J,len(self.neurals),len(X))
        #print()
        for j in range(self.J):
            output += self.basis_func(X,
                                      self.neurals[j]) * self.neurals[j]['weight']
        return output

    def eval(self, dataset):
        return sum([(data['y'] - self.output(data['X']))**2 for data in dataset])/2

    def get_params(self):
        return self.theta, self.neurals

    @staticmethod
    def params2flatten(theta, neurals):
        params = [theta]
        # {weight} {mid} {sigma}
        for n in neurals:
            params.append(n['weight'])
            for m in n['m']:
                params.append(m)
            params.append(n['sigma'])
        return params

    @staticmethod
    def flatten2params(params, input_dim):
        theta = params[0]
        neurals = []
        #params.pop(0)
        J = int((len(params)-1) / (input_dim+2))
        # {weight} {mid} {sigma}
        for j in range(J):
            neurals.append({
                'sigma': params[1+(j+1)*(input_dim+2)-1],
                'm': params[1+j*(input_dim+2)+1:(j+1)*(input_dim+2)],
                'weight': params[1+j*(input_dim+2)]
            })
        return theta, neurals

    def set_params(self, theta, neurals):
        assert len(neurals) == self.J
        self.theta = theta
        self.neurals = neurals

    def load(self, path='../weights/RBFN_params.txt'):
        with open(path, 'r') as f:
            lines = f.readlines()
            lines = list(map(lambda x: x.replace('\n', '').split(' '), lines))
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    lines[i][j] = float(lines[i][j])
            theta = lines[0][0]
            neurals = []
            for i in range(1, len(lines)):
                print(lines[i][1:-1])
                neurals.append({
                    'sigma': lines[i][-1],
                    'm': lines[i][1:-1],
                    'weight': lines[i][0]
                })
            self.set_params(theta, neurals)

    def save(self, path='../weights/RBFN_params.txt'):
        theta, neurals = self.get_params()
        with open(path, 'w') as f:
            f.write('{theta}\n'.format(theta=theta))
            for n in neurals:
                f.write('{weight} {mid} {sigma}\n'.format(weight=n['weight'],
                                                          mid=' '.join(
                                                              list(map(lambda x: str(x), n['m']))),
                                                          sigma=n['sigma']))

if __name__ == "__main__":
    r = RBFN()
    theta, neurals = r.get_params()
    print((theta, neurals))
    print(RBFN.flatten2params(RBFN.params2flatten(theta, neurals), 3))