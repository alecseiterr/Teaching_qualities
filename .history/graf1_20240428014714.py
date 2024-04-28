import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_hourly_density(file_path):
    # Load your data
    data = pd.read_csv(file_path)
    # Check the data types of all columns
    print(data.dtypes)
    # Convert 'Дата старта урока' column to datetime
    data['Дата старта урока'] = pd.to_datetime(data['Дата старта урока'])
    # Check if the conversion was successful
    print(data.dtypes)
    # Now you can use the .dt accessor
    data['Час старта урока'] = data['Дата старта урока'].dt.hour
    # Continue with your plotting code
    hourly_density = data.groupby('Час старта урока')['Плотность сообщений в минуту'].mean()
    plt.figure(figsize=(10, 6))
    hourly_density.plot(kind='bar')
    plt.title('Средняя плотность сообщений по часам')
    plt.xlabel('Час дня')
    plt.ylabel('Средняя плотность сообщений в минуту')
    plt.xticks(rotation=0)
    plt.grid(True)

    # Save the plot as a PNG file
    plt.savefig('hourly_density_plot.png', bbox_inches='tight')

    plt.show()

data_path = 'analis.csv'
plot_hourly_density(data_path)