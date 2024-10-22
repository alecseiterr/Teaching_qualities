import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_hourly_density(file_path):

    data = pd.read_csv(file_path)
    print(data.dtypes)
    data['Дата старта урока'] = pd.to_datetime(data['Дата старта урока'])
    print(data.dtypes)
    data['Час старта урока'] = data['Дата старта урока'].dt.hour

    hourly_density = data.groupby('Час старта урока')['Плотность сообщений в минуту'].mean()
    plt.figure(figsize=(10, 6))
    hourly_density.plot(kind='bar')
    plt.title('Средняя плотность сообщений по часам')
    plt.xlabel('Час дня')
    plt.ylabel('Средняя плотность сообщений в минуту')
    plt.xticks(rotation=0)
    plt.grid(True)
    plt.savefig('hourly_plot.png', bbox_inches='tight')
    plt.show()

# data_path = 'analis.csv'
# plot_hourly_density(data_path)
