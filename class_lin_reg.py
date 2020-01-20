"""
This program will convert PDFs into images and read text from those images
and print the text over the screen.
This can also extract text directly from images and print it out.
"""


import pandas
import matplotlib.pyplot as plt
import numpy as np


class LinearRegression:

    """
    Performs linear regression on the given data.
    """

    def __init__(self, filename):

        """
        Initializes the memory of the object as the object is created using the parent class.
        :param filename: string parameter to save the path and name of the file.
        """

        self.filename = filename

    def read_data(self):
        """

        :return:
        """

        column_names = ['area', 'price']
        # To read columns
        io = pandas.read_csv(self.filename, names=column_names, header=None)
        x_val = (io.values[1:, 0])
        y_val = (io.values[1:, 1])
        size_array = len(y_val)
        for i in range(size_array):
            x_val[i] = float(x_val[i])
            y_val[i] = float(y_val[i])
        return x_val, y_val

    @staticmethod
    def feature_normalize(train_x):
        mean = np.mean(train_x, axis=0)
        std = np.std(train_x, axis=0)
        print(mean, std)
        return (train_x - mean) / std

    @staticmethod
    def numpy_reg(x_input, y_input):
        """

        :param x_input:
        :param y_input:
        :return:
        """
        # Call the method for a specific file

        # Modeling
        w, b = 0.0, 0.0
        num_epoch = 100
        converge_rate = np.zeros([num_epoch, 1], dtype=float)
        learning_rate = 1e-3

        for e in range(num_epoch):
            # Calculate the gradient of the loss function with respect to arguments (model parameters) manually.
            y_predicted = w * x_input + b
            grad_w, grad_b = (y_predicted - y_input).dot(x_input), (y_predicted - y_input).sum()

            # Update parameters.
            w, b = w - learning_rate * grad_w, b - learning_rate * grad_b
            converge_rate[e] = np.mean(np.square(y_predicted - y_input))

        return w, b

    @staticmethod
    def plot_data(x_input, y_input, w, b):
        """

        :return:
        """

        y_estimated = w * x_input + b

        plt.rcParams.update({'font.size': 20})
        fig = plt.figure()
        fig.set_size_inches(15, 12)
        ax = fig.add_subplot(111)

        ax.scatter(x_input, y_input, color='green', s=70)
        ax.set_xlabel('Number of iterations')
        ax.set_ylabel('Error')
        ax.set_title('Apartment price vs area in Berlin')
        ax.plot(x_input, y_estimated, linewidth=4.0, color='red')

        ax.spines['bottom'].set_color('orange')
        ax.spines['bottom'].set_linewidth(3.0)
        ax.spines['top'].set_color('orange')
        ax.spines['top'].set_linewidth(3.0)
        ax.spines['right'].set_color('orange')
        ax.spines['right'].set_linewidth(3.0)
        ax.spines['left'].set_color('orange')
        ax.spines['left'].set_linewidth(3.0)

        ax.tick_params(axis='x', colors='orange')
        ax.tick_params(axis='y', colors='orange')

        ax.yaxis.label.set_color('orange')
        ax.xaxis.label.set_color('orange')
        ax.title.set_color('orange')
        plt.savefig('numpy_regression_points_norm.png', transparent=True)
        plt.show()


# processing an individual data
full_path = "area_price.csv"

# create an object of the OCR class
lin_reg = LinearRegression(full_path)
x_raw, y_raw = lin_reg.read_data()
x = lin_reg.feature_normalize(x_raw)
y = y_raw
weight, bias = lin_reg.numpy_reg(x, y)
lin_reg.plot_data(x, y, weight, bias)
