import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

AVAILABLE_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter city name: Chicago, New York City, Washington\n").lower()
        if city in CITY_DATA:
            break
        else:
            print('You enterd wrong name')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('To filter the data by month enter: January, February, March, April, May, June; otherwise enter: all\n').lower()
        if month in AVAILABLE_MONTHS:
            break
        else:
            print('You enterd wrong month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("If you would like to filter the data by day of week enter a day (e.g. Monday, Tuesday, etc); otherwise enter: all\n").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('You enterd wrong day of week. The valid values are: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, all')

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
    file_name = CITY_DATA[city]
    # load data file into a dataframe
    df = pd.read_csv(file_name)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the AVAILABLE_MONTHS list to get the corresponding int
        month_num = AVAILABLE_MONTHS.index(month)    # january index is 1 in the list 
    
        # filter by month to create the new dataframe
        df = df[df['Month'] == month_num]       # df = df.loc[df['month'] == month_num]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['Day of Week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month  
    no_month_filter = len(df['Month'].unique()) > 1
    if no_month_filter:                # display only if if no month filter applied
        month_num = df['Month'].mode()[0]
        print('The most common month is:', AVAILABLE_MONTHS[month_num].title())

    # display the most common day of week
    no_day_filter = len(df['Day of Week'].unique()) > 1
    if no_day_filter:                  # display only if no day filter applied
        day_of_week = df['Day of Week'].mode()[0]
        print('The most common day of week is:', day_of_week)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    hour = df['Hour'].mode()[0]
    print('The most common start hour is:', hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', end_station)

    # display most frequent combination of start station and end station trip
    df['Start End Combination'] = 'Start: ' + df['Start Station'] + '; End: ' + df['End Station']
    start_end_combination_value = df['Start End Combination'].value_counts().index[0]
    start_end_combination_counts = df['Start End Combination'].value_counts()[0]
    print('\nThe most frequent combination of start station and end station trip:')
    print(start_end_combination_value)
    print('Number of trips:', start_end_combination_counts)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    def seconds_to_days(sec_count):
        sec_count = int(sec_count)
        days = sec_count // (60 * 60 * 24)
        sec_count = sec_count % (60 * 60 * 24)
        hours = sec_count // (60 * 60)
        sec_count = sec_count % (60 * 60)
        minutes = sec_count // 60
        sec_count = sec_count % 60
        
        result = []
        if days > 0:
            result.append('{} days'.format(days))
        if hours > 0:
            result.append('{} hours'.format(hours))
        if minutes > 0:
            result.append('{} minutes'.format(minutes))
        if sec_count > 0:
            result.append('{} seconds'.format(sec_count))
        return ', '.join(result)
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    formatted_travel_time = seconds_to_days(total_travel_time)
    print('Total travel time (seconds): ', total_travel_time)
    print('Total travel time (days): ', formatted_travel_time)

    # display mean travel time
    number_of_values = df['Trip Duration'].count()
    mean_travel_time = total_travel_time / number_of_values
    print('Mean travel time:', seconds_to_days(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types    
    user_type_counts = df['User Type'].value_counts()
    print('Counts of user types:')
    print(user_type_counts)

    # Display counts of gender    
    try:
        counts_of_gender = df['Gender'].value_counts()
        print('\nCounts of gender:')
        print(counts_of_gender)
    except:
        print('\nGender information is not available')
    

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe earliest year of birth:', int(df['Birth Year'].min()))
        print('The most recent year of birth:', int(df['Birth Year'].max()))
        print('The most common year of birth:', int(df['Birth Year'].mode()[0]))
    else:
        print('\nBirth year information is not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data_display = input('\nWould you like to view raw data? Enter yes or no.\n')
        if raw_data_display.lower() == 'yes':
            print(df.head(5))
            start_row = 5
            while True:
                raw_data_display = input('\nWould you like to view the next portion? Enter yes or no.\n')
                if raw_data_display.lower() == 'yes':
                    print(df[start_row: start_row + 5])
                    start_row += 5
                else:
                    break                          
            
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
