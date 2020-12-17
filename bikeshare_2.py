import time
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = input('Which city? : ').lower()
    while city not in CITY_DATA:
        city = input('Please enter one off Chicago, New York City or Washington : ').lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Which month?: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
        month = input('Please enter "all" or a valid month e.g. "January": ').lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day?: ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Please enter "all" or a valid day e.g. "Monday": ').lower()
    # confirm data with user
    print('You selected City: {}, Month= {}, Day= {}'.format(city,month,day))
    check = input('Is this correct? Y/N').lower()
    if check == 'n':
        return get_filters()
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    months = dict(all=0, january=1, february=2, march=3, april=4, may=5, june=6, july=7, august=8, september=9, october=10, november=11, december=12)
    days = dict(all=7, monday=0, tuesday=1, wednesday=2, thursday=3, friday=4, saturday=5, sunday=6)
    #load df
    df = pd.read_csv(city.replace(' ', '_') +'.csv')
    #add month and day columns with int values
    df.insert(len(df.columns),'month',0)
    df.insert(len(df.columns),'day',0)
    df["month"] = pd.DatetimeIndex(df['Start Time']).month
    df["day"] = pd.DatetimeIndex(df['Start Time']).dayofweek
    #filter by month or day
    if month != 'all':
        df = df[df['month'] == months[month]]
    if day != 'all':
        df = df[df['day'] == days[day]]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = df.loc[:, 'month'].mode()
    print('The most common hire month is:', calendar.month_name[month_mode.iloc[0]])
    # display the most common day of week
    day_mode = df.loc[:, 'day'].mode()
    print('The most common hire day is:', calendar.day_name[day_mode.iloc[0]])

    # display the most common start hour
    df.insert(len(df.columns),'hour',0)
    df["hour"] = pd.DatetimeIndex(df['Start Time']).hour
    hour_mode = df.loc[:, 'hour'].mode()
    print('The most common hire hour is: ' + str(hour_mode.iloc[0]) + ':00')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station_start_mode = df.loc[:, 'Start Station'].mode()
    print('The most common start station is:', station_start_mode.iloc[0])

    # display most commonly used end station
    station_end_mode = df.loc[:, 'End Station'].mode()
    print('The most common end station is:', station_end_mode.iloc[0])

    # display most frequent combination of start station and end station trip
    grouped = df.groupby(['Start Station', 'End Station']).agg('count')
    a = grouped.sort_values(['Unnamed: 0'], ascending=False)
    print('The top five start and end station pairs are:')
    print(a.iloc[:, 0].head(5))
  
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    print('Total trip time in this period was:', datetime.timedelta(seconds=int(df.loc[:, 'Trip Duration'].sum())))

    # display mean travel time
    print('Mean trip time was:', datetime.timedelta(seconds=int(df.loc[:, 'Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    grouped = df.groupby(['User Type']).agg('count')
    print(grouped.iloc[:, 0].head(20))
    

    # Display counts of gender
    if 'Gender' in df.columns:
        grouped = df.groupby(['Gender']).agg('count')
        print(grouped.iloc[:, 0].head(2))
    else:
        print('No gender data is available')


    # Display earliest, most recent, and most common year of birth in histogram 
    if 'Birth Year' in df.columns:
        plt.hist(df['Birth Year'], 20)
        plt.xlabel('Year of Birth')
        plt.ylabel('Frequency')
        plt.title('User Year of Birth Histogram \n Bins=5 years \n City: {}, Month: {}, Day: {}'.format(city, month, day))
        plt.show()
    else:
        print('No date of birth data is available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    more_data = input('Would you like to see 5 lines of raw data? Y/N').lower
    while more_data not in ['y', 'n']:
        more_data = input('Please enter a valid input: Y/N').lower()
    n=0
    while more_data=='y':
        print(df.iloc[n:, :].head(5))
        n+=5
        more_data = input('Would you like to see five more lines? Y/N').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
