from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

path_to_df = r'data/zigbee_спальня.csv'
start = r'2022-10-26 00:00:00'
end = r'2022-10-26 23:59:59'


def draw_graph(path_to_df, start, end):
    df = pd.read_csv(path_to_df, parse_dates=['datetime'])
    df['humidity_shift'] = df.humidity.shift(-1)
    df = df.drop_duplicates(subset='datetime')
    df = df[(df.datetime >= start) & (df.datetime <= end)]

    # Creating plot
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_ylabel('Температура', color=color)
    ax1.plot(df['datetime'], df['temperature'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Влажность', color=color)
    ax2.plot(df['datetime'], df['humidity_shift'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
    # ax1.xaxis.set_minor_locator(ticker.MaxNLocator(40))
    time_elapsed = df.datetime.iloc[len(df) - 1] - df.datetime.iloc[0]

    if time_elapsed >= timedelta(hours=1) and time_elapsed <= timedelta(hours=24):
        ax1.xaxis.set_major_locator(mdates.HourLocator(byhour=None, interval=1, tz=None))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

    elif time_elapsed > timedelta(hours=24):
        ax1.xaxis.set_major_locator(mdates.HourLocator(byhour=None, interval=6, tz=None))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%D %H:%M'))

    else:
        ax1.xaxis.set_major_locator(mdates.MinuteLocator(byminute=None, interval=10, tz=None))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%D %H:%M'))

    # for tick in ax1.get_xticklabels():
    #     tick.set_rotation(30)

    ax1.xaxis.grid()

    # Adding title
    plt.title('Спальня')

    # Show plot
    plt.show()


def main():
    draw_graph(path_to_df, start, end)


if __name__ == '__main__':
    main()
