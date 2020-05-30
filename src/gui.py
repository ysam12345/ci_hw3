#!/usr/bin/env python
# coding:utf-8
import numpy as np
from tkinter import *
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from tkinter.filedialog import askopenfilename
from data import Data
from car import Car
from road import Road
from gui_utils import add_text, add_button, add_spinbox
from enum import Enum
from time import sleep
from recorder import Recorder
from rbfn import RBFN
from ga import GA

class State(Enum):
    PLAYING = 0
    CRASH = 1
    FINISH = 2


class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.root = master
        self.grid()
        self.data = self.load_data()
        self.car, self.road = self.init_components()
        self.state = State.PLAYING
        self.dataset_path = '../data/train6dAll.txt'
        self.rbfn_weight_path = '../data/6D_RBFN_params.txt'
        self.mode = '4D'
        self.rbfn = RBFN(J=6, input_dim=3)
        self.rbfn.load(path='../weights/4D_RBFN_params.txt')
        self.set_mode('6D')
        self.ga = GA()

        self.recorder = Recorder()
        self.recorder.add(self.car)
        self.create_widgets()
        self.clean_fig()
        self.draw_road(self.road.finish_area, self.road.road_edges)
        self.draw_car(self.car.loc(), self.car.car_degree, self.car.radius)

    def set_mode(self, mode):
        assert mode=='4D' or mode=='6D'
        self.mode = mode
        if self.mode == '4D':
            self.rbfn = RBFN(J=6, input_dim=3)
            self.rbfn.load(path='../weights/4D_RBFN_params.txt')
        elif self.mode == '6D':
            self.rbfn = RBFN(J=8, input_dim=5)
            self.rbfn.load(path='../weights/6D_RBFN_params.txt')

    def change_mode(self):
        if self.mode == '4D':
            self.set_mode('6D')
            self.im['text'] = '6D'
        else:
            self.set_mode('4D')
            self.im['text'] = '4D'

    def load_data(self):
        case_file_path = '../cases/case01.txt'
        d = Data(case_file_path)
        return d.get()

    def init_components(self):
        c = Car(self.data['start_point'], self.data['start_degree'])
        c.update_sensor(self.data['road_edges'])
        r = Road(self.data['finish_area'], self.data['road_edges'])
        return c, r

    def create_widgets(self):
        # 標題
        self.winfo_toplevel().title("Yochien CI HW2")

        # 自走車位置、方向、感測器距離
        _, self.loc = add_text(self, 0, "Car Location", self.car.loc())
        _, self.fl = add_text(self,
                              1, "Car Sensor Front Left", self.car.sensor_dist['fl'])
        _, self.f = add_text(self,
                             2, "Car Sensor Front", self.car.sensor_dist['f'])
        _, self.fr = add_text(self,
                              3, "Car Sensor Front Right", self.car.sensor_dist['fr'])
        _, self.cd = add_text(self,
                              4, "Car Degree", self.car.car_degree)
        _, self.swd = add_text(self,
                               5, "Car Steering Wheel Degree", self.car.steering_wheel_degree)
        # 更新車子
        _, self.next = add_button(self,
                                  6, "Start Playing", "Run", self.run)
        # 目前狀態
        _, self.st = add_text(self,
                              7, "Status", self.state)

        # 迭代次數
        _, self.it = add_spinbox(self, 8, "Iterate Times", 10, 10000)
        # 族群大小
        _, self.ps = add_spinbox(self, 9, "Population Size", 10, 10000)
        # 突變機率
        _, self.mp = add_spinbox(self, 10, "Mutation Prob(%)", 1, 100)
        # 交配機率
        _, self.cp = add_spinbox(self, 11, "Cross Prob(%)", 1, 100)

        # 選取訓練資料集
        _, self.td = add_text(self,
                              12, "Training Dataset", self.dataset_path)
        _, self.next = add_button(self,
                                  13, "Select Dataset", "Select", self.select_dataset_file)
        # 選取RBFN weight
        _, self.rbfn_wf = add_text(self,
                              14, "RBFN weight file", self.rbfn_weight_path)
        _, self.srbfn_wf = add_button(self,
                                  15, "Select RBFN weight", "Select", self.select_rbfn_weight_file)
        # 選取Mode
        _, self.im = add_text(self,
                              16, "Input Mode (4D/6D)", self.mode)
        _, self.cm = add_button(self,
                                  17, "Change Mode", "Change", self.change_mode)
        # Train RBFN
        _, self.tb = add_button(self,
                                  18, "Train RBFN", "Train", self.train_ga)

        # 地圖與道路
        self.road_fig = Figure(figsize=(5, 5), dpi=120)
        self.road_canvas = FigureCanvasTkAgg(
            self.road_fig, self)
        self.road_canvas.draw()
        self.road_canvas.get_tk_widget().grid(row=19, column=0, columnspan=3)

    def train_ga(self):
        if self.mode == '4D':
            J = 6
            input_dim=3
        else:
            J = 8
            input_dim=5
        iteration_times = int(self.it.get())
        populations_size = int(self.ps.get())
        mutation_prob = int(self.mp.get())/100
        crossover_prob = int(self.cp.get())/100
        print(iteration_times, populations_size, mutation_prob, crossover_prob)
        self.GA = GA(iteration_times=iteration_times, populations_size=populations_size, 
                 mutation_prob=mutation_prob, crossover_prob=crossover_prob, J=J,
                 input_dim=input_dim, dataset_path=self.dataset_path)
        self.GA.train()

    def select_rbfn_weight_file(self):
        try:
            filename = askopenfilename()
            self.rbfn_wf["text"] = filename
            self.rbfn_weight_path = filename
            self.rbfn.load(path=filename)
        except Exception as e:
            print(e)
            self.rbfn_wf["text"] = ""

    def select_dataset_file(self):
        try:
            filename = askopenfilename()
            self.td["text"] = filename
            self.dataset_path = filename
            self.ga = GA(dataset_path=filename)
        except Exception as e:
            print(e)
            self.td["text"] = ""

    def turn_steering_wheel(self, degree):
        self.car.turn_steering_wheel(degree)

    def run(self):
        while self.state == State.PLAYING:
            self.update()
            sleep(0.02)

    def update(self):
        self.update_state()
        self.update_car()
        self.recorder.add(self.car)

    def update_state(self):
        if self.road.is_crash(self.car):
            self.state = State.CRASH
        elif self.road.is_finish(self.car):
            self.state = State.FINISH
            self.recorder.to_file()
            
        self.st["text"] = self.state

    def update_car(self):
        fl, f, fr = self.car.update_sensor(
            self.data['road_edges'])


        if self.mode =='4D':
            self.turn_steering_wheel(self.rbfn.output([f, fr, fl]))
        elif self.mode == '6D':
            x, y = self.car.loc()
            self.turn_steering_wheel(self.rbfn.output([x, y , f, fr, fl]))

        self.car.next()
        self.loc["text"] = self.car.loc()
        self.cd["text"] = self.car.car_degree
        self.swd["text"] = self.car.steering_wheel_degree
        self.clean_fig()
        self.draw_road(self.road.finish_area, self.road.road_edges)
        self.draw_car(self.car.loc(), self.car.car_degree, self.car.radius)
        self.draw_route()
        self.road_canvas.draw()

    def clean_fig(self):
        # 清空並初始化影像
        self.road_fig.clf()
        self.road_fig.ax = self.road_fig.add_subplot(111)
        self.road_fig.ax.set_aspect(1)
        self.road_fig.ax.set_xlim([-20, 60])
        self.road_fig.ax.set_ylim([-10, 60])

    def draw_road(self, finish_area, road_edges):
        # 車道邊界
        for i in range(len(road_edges)-1):
            self.road_fig.ax.text(road_edges[i][0], road_edges[i][1], '({},{})'.format(
                road_edges[i][0], road_edges[i][1]))
            self.road_fig.ax.plot([road_edges[i][0], road_edges[i+1][0]], [
                                  road_edges[i][1], road_edges[i+1][1]], 'k')
        # 終點區域
        a, b = finish_area[0]
        c, d = finish_area[1]
        self.road_fig.ax.plot([a, c], [b, b], 'r')
        self.road_fig.ax.plot([c, c], [b, d], 'r')
        self.road_fig.ax.plot([c, a], [d, d], 'r')
        self.road_fig.ax.plot([a, a], [d, b], 'r')

    def draw_car(self, loc, car_degree, radius):
        # 車子範圍
        self.road_fig.ax.plot(loc[0], loc[1], '.b')
        circle = plt.Circle(loc, radius, color='b', fill=False)
        self.road_fig.ax.add_artist(circle)
        # 感測器
        self.fl["text"], self.f["text"], self.fr["text"] = self.car.update_sensor(
            self.data['road_edges'])
        for s in self.car.sensor_point:
            self.road_fig.ax.plot(
                [loc[0], self.car.sensor_point[s][0]],
                [loc[1], self.car.sensor_point[s][1]], 'r')
            self.road_fig.ax.plot(
                self.car.sensor_point[s][0], self.car.sensor_point[s][1], '.b')

    def draw_route(self):
        records = self.recorder.get()
        for r in records:
            self.road_fig.ax.plot(int(float(r[0])+0.0001), int(float(r[1])+0.0001), '.y')


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
