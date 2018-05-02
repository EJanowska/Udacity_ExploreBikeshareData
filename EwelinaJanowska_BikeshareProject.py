import time
import pandas as pd
import numpy as np

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

    #get user input for city (chicago, new york city, washington)
    city = input('Would you like to see data from chicago, new york city or washington?\n')
    while city:
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print('Sorry I did not catch that.\n')
            city = input('Please enter: chicago, new york city or washington\n')
            continue
   
    #get user input for month (january, february, ... , june, all)
    month = input('Would you like to see data from january, february, march, april, may, june or all?\n')
    while month:
        if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            break
        else:
            print('Sorry I did not catch that.\n')
            month = input('Please enter: january, february, march, april, may, june or all?\n')
            continue 

    #get user input for day of week (monday, tuesday, ... sunday, all)
    day = input('Would you like to see date from monday, tuesday, wednesday, thursday, friday, saturday, sunday, or all\n')
    while day:
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            break
        else:
            print('Sorry I did not catch that.\n')
            day = input('Please enter: monday, tuesday, wednesday, thursday, friday, saturday, sunday, or all\n')
            continue

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
    #load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if applicable
    if month != 'all':
        #use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day of week if applicable  
    if day != 'all':
        #filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
      
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #display the most common month
    popular_month = df['month'].mode()[0]
    #convert name of months from numbers to text
    if popular_month == 1:
        popular_month = 'January'
    elif popular_month == 2:
        popular_month = 'Frbruary'
    elif popular_month == 3:
        popular_month = 'March'
    elif popular_month == 4:
        popular_month = 'April'
    elif popular_month == 5:
        popular_month = 'May'
    elif popular_month == 6:
        popular_month = 'June'

    #display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    #display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print('\nMost common month: %s\nMost common day of week: %s\nMost common start hour: %s\n'%(popular_month, popular_day, popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    #display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    #display most frequent combination of start station and end station trip
    popular_start_end_station = (df['Start Station'] + '-' + df['End Station']).mode()[0]
    
    print('\nMost commonly used start station: %s\nMost commonly used end station: %s\nMost frequent combination of start and end station: %s \n'%(popular_start_station, popular_end_station, popular_start_end_station))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = df['Trip Duration'].sum()

    #display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('\nTotal travel time: %s\nMean travel time: %s\n'%(total_travel_time, mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users for Chicago and New York City."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()

    #Display counts of gender
    user_gender = df['Gender'].value_counts()

    #Display earliest, most recent, and most common year of birth
    popular_year_birth = df['Birth Year'].mode()[0]
    earliest_year_birth = df['Birth Year'].min()
    recent_year_birth = df['Birth Year'].max()

    print('Counts of user types:\n%s\nCounts of gender:\n%s\n'%(user_types,user_gender))
    print('Earliest year of birth: %1.0f\nMost recent year of birth: %1.0f\nMost common year of birth: %1.0f'%(earliest_year_birth, recent_year_birth, popular_year_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats_wash(df):
    """Displays statistics on bikeshare users for Washington.
    Washington does not have gender and birth year data.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()


    print('Counts of user types:\n%s\n'%(user_types))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city == 'washington':
            user_stats_wash(df)
        else:
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
