import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def validate_user_input(input_str, input_type):
    while True:
        input_read = input(input_str)
        try:
            if input_read.lower() in ['chicago', 'new york city', 'washington'.lower()] and input_type==1:
                break
            elif input_read.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all'.lower()] and input_type==2:
                break
            elif input_read.lower() in ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all'.lower()] and input_type==3:
                break
            
            else:
                if input_type==1:
                    print('Sorry, That was a wrong city! Please choose a valid city name from (chicago - new york city - washington)')
                if input_type==2:
                    print('Sorry, That was not a valid month input! Please choose a valid month name from january to june.')
                if input_type==3:
                    print('That\'s not a valid day input!')
        except ValueError:
            print('Sorry, INVALID INPUT!')
    return input_read.lower()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to f ilter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    #get user's input for city (chicago, new york city, washington).
    city = validate_user_input('Please type the city name! (chicago, washington, new york city)'.lower(), 1)
    
    #get user's input for month (all, january, february, ... , june)
    month = validate_user_input('Please choose a month! (all, january, february, ... , june)'.lower(), 2)

    #get user's input for day of week (all, monday, tuesday, ... sunday)
    day = validate_user_input('Which day of week? (all, monday, tuesday, ... sunday)'.lower(), 3)

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

    #loading the datafile into the data frame...
    df = pd.read_csv(CITY_DATA[city])

    #converting start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    #filtering by month if applicable...
    if month != 'all':
        months = ['january', 'fabuary', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month] #create new dataframe for months

    #filtering by day if applicable...
    if day != 'all':
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    print(df['month'].mode()[0])

    #display the most common day of week
    print(df['day_of_week'].mode()[0])

    #display the most common start hour
    print(df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    print(df['Start Station'].mode()[0])

    #display most commonly used end station
    print(df['End Station'].mode()[0])

    #display most frequent combination of start station and end station trip
    popular_combination_trip = df['Start Station'] + 'to' + df['End Station']
    print(f'The most popular trip was from: {popular_combination_trip.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print(df['Trip Duration'].sum())

    #display mean travel time
    print(df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print(df['User Type'].value_counts())

    #Display counts of gender (which is only available for new york and chicago)
    if city != 'washington':
        print(df['Gender'].value_counts())
        


        #Display earliest, most recent, and most common year of birth(Only for chicago and nyc)

         #Earliest...
        print(df['Birth Year'].max())

         #Oldest...
        print(df['Birth Year'].min())

        #Most common year of birth...
        print(df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Ask the user if he wants to show raw data in 5 rows at a time"""
    
    raw = input('\nWould you like to show the original raw data?\n')
    if raw.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count+5])
            count += 5
            ask = input('Next 5 raws?')
            if ask.lower() != 'yes':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
