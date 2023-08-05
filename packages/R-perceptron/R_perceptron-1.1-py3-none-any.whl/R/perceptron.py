import matplotlib.pyplot as plt
import random
import math

data1_training = [0]
data2_training = [0]
data1_validation = [0]
data2_validation = [0]
layer_cnt = []
son_tmp = 0
layer = [0] * son_tmp


class Layer:
    def __init__(self, n, next):
        self.n = n
        self.next = next
        self.w = []
        for i in range(n):
            w_tmp = []
            for j in range(next):
                w_tmp.append(random.uniform(-1, 1) / pow(10, 1))
                self.w.append(w_tmp)

    def output(self, input):
        value = [0] * self.next
        for i in range(self.n):
            for j in range(self.next):
                value[j] += input[i] * self.w[i][j]
        return value

    def here(self, best):
        for i in range(self.n):
            for j in range(self.next):
                self.w[i][j] = best.w[i][j] + random.uniform(-1, 1) / pow(10, 3)


def help():
    print("먼저 데이터를 입력해야 합니다. 이는 리스트 data1_training, data2_training에 학습 데이터를, data1_validation, data2_validation에 검증 데이터를 넣으면 됩니다.")
    print("두 번째로는 함수 create_model을 사용하여 모델을 만들어야 합니다.")
    print("마지막으로는 함수 training_model을 사용하여 모델을 훈련시킵니다.")
    print("")


def create_model(layer_number, son):
    global layer_cnt
    global son_tmp
    layer_cnt = layer_number
    son_tmp = son
    for i in range(son_tmp):
        layer[i] = []
    for i in range(len(layer_cnt) - 1):
        for j in range(son_tmp):
            layer[j].append(Layer(layer_cnt[i], layer_cnt[i + 1]))


def sigmoid(x):
    return 1 / (math.exp(-x) + 1)


def calculate(initial_value, layer_n):
    tmp = initial_value
    for i in range(len(initial_value)):
        tmp[i] = sigmoid(tmp[i])
    for i in range(len(layer_cnt) - 1):
        tmp = layer[layer_n][i].output(tmp)
    return sigmoid(tmp[0])


def cost(layer_n, type):
    tmp = []
    if type == 'test':
        for i in range(len(data1_training)):
            tmp.append(abs(1 - calculate(data1_training[i], layer_n)))
            tmp.append(abs(calculate(data2_training[i], layer_n)))
    if type == 'validation':
        for i in range(len(data1_validation)):
            tmp.append(abs(1 - calculate(data1_validation[i], layer_n)))
            tmp.append(abs(calculate(data2_validation[i], layer_n)))
    value = 0
    for i in range(len(data1_training) * 2):
        value += tmp[i]**2
    return value


def shaking(layer_n):
    layer[0] = layer[layer_n]
    for i in range(1, son_tmp):
        for j in range(len(layer_cnt) - 1):
            layer[i][j].here(layer[layer_n][j])


def process():
    global epoch
    global Cost_test
    global Cost_validation
    epoch += 1

    cost_list = []
    for i in range(son_tmp):
        cost_list.append(cost(i, 'test'))
    tmp = min(cost_list)
    Cost_test.append(tmp)
    index = cost_list.index(tmp)

    cost_list = []
    for i in range(son_tmp):
        cost_list.append(cost(i, 'validation'))
    tmp = min(cost_list)
    Cost_validation.append(tmp)

    print("epoch : ", epoch, "cost = ", tmp)

    shaking(index)


def training_model(number):
    for i in range(number):
        process()
    plt.plot(Cost_test, label = 'test')
    plt.plot(Cost_validation, label = 'validation')
    plt.legend()
    plt.show()

def change_w(i, j, w):
    layer[i][j] = w