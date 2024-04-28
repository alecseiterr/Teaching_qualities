import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_hourly_density(data):
    # Assuming 'Дата старта урока' is a datetime column
    data['Час старта урока'] = data['Дата старта урока'].dt.hour

    # Group data by hour and calculate the mean density
    hourly_density = data.groupby('Час старта урока')['Плотность сообщений в минуту'].mean()

    # Plot the data
    hourly_density.plot(kind='bar', figsize=(10, 6))
    plt.title('Средняя плотность сообщений по часам')
    plt.xlabel('Час дня')
    plt.ylabel('Средняя плотность сообщений в минуту')
    plt.xticks(rotation=0)
    plt.grid(True)
    plt.show()

def main():
    data_path = '/content/data.csv'  # Specify the correct path to your data file
    data = pd.read_csv(data_path)  # Load the data

    plot_hourly_density(data)

if __name__ == "__main__":
    main()