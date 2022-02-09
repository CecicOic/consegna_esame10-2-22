# Imports:
from datetime import datetime as dt # Needed to check the format of the dates

# ===================== #
#  EXAMEXCEPTION CLASS  #
# ===================== #
class ExamException(Exception):
    pass

# ========================= #
#  CSVTIMESERIESFILE CLASS  #
# ========================= #
class CSVTimeSeriesFile():

# =============== #
#  INIT FUNCTION  #
# =============== #
    def __init__(self, name):
        self.name = name

        # Name is ALWAYS a str:
        if not isinstance(name, str):
            print('W A R N I N G: the name of the file is not a string! I\'ll try to correct it. . .')

            # Trying to convert the name to a string. We'll check if the file exists later:
            try:
                self.name = str(name)
            except Exception:
                raise ExamException('E R R O R: couldn\'t convert self.name into a string!')

# =================== #
#  GET_DATA FUNCTION  #
# =================== #
    def get_data(self): 

        # Creating the two lists I will need in the function:
        two_element_list = [] # The two-element lists will be previously stored here
        final_list = [] # The two-element list above will be appended as element inside this list, then the first list will be substitute with the next couple

        # Checking if the file exists by opening it:
        try:
            file = open(self.name, 'r')

        # If the file does not exist, an exception must be raised:
        except Exception:
            raise ExamException('E R R O R: file couldn\'t be opened, maybe it doesn\'t exist! ')

        # The script will now run through every single line of the file and will store them one at the time in the two-element list:
        for line in file:

            # Here the script divides the line in two separate objects, dividing it when it encounters a specific char (,):
            list_element = line.split(',')
            
            # Here is where it's checked that we are not processing the title of the csv file:
            if list_element[0] != 'date':
            
                # First element will be the date, second will be the number of passengers:
                
                date = list_element[0]

                # Date must be of the %Y-%m format:
                try:
                    date = dt.strptime(date, "%Y-%m")
                except Exception:
                    continue

                date = list_element[0]    
                
                # Raising exception in case the value does not exist storing 0 in the passengers variable so the function can run anyways:
                try:
                    passengers = int(list_element[1])

                except IndexError:
                    passengers = 0
                
                # If the number is negative or float, we just skip it:
                except ValueError:
                    continue # float

                if passengers < 0:
                    continue # negative



                
                # Now it's needed to check if there are some duplicates in the timestamps:
                
                # The final list needs obviously to be already filled:
                if len(final_list) > 0:

                    # If it's not empty, the script will cycle trough it:
                    for item in final_list:

                        # The data of the item will be temporary saved in a variable:
                        prev_date = item[0] # item is still a list so we need to take into consideration only its first element

                        # Check for duplicates:
                        if prev_date == date: 
                            raise ExamException('E R R O R: timestamp "{}" is a duplicate.'.format(date))

                    # If there aren't duplicates, a check will be made for the order of the timestamps:
                    # The data of the item will be temporary saved in a variable:
                    prev_date == final_list[-1][0]

                    # Check for errors in the order:
                    if prev_date > date:
                        raise ExamException('E R R O R: timestamp "{}" is in the wrong order.'.format(date))


                # The two-element list now takes shape:
                two_element_list = [date, passengers]

                # And finally we add it to the final list:
                final_list.append(two_element_list)

                # Now the cycle will be run again.
                
        # If the file is empty 
        if not final_list:
            raise ExamException('E R R O R: file is empty! ')

        # Final output.
        return  final_list

# ================================ #
#  COMPUTE AVG MONTHLY DIFFERENCE  #
# ================================ #
def compute_avg_monthly_difference(time_series, first_year, last_year): 

    # Check if time_series is a list
    if not isinstance(time_series, list):
        raise ExamException('E R R O R: time_series is NOT a list of lists. ')

    elif not isinstance(time_series[0], list):
        raise ExamException('E R R O R: time_series is NOT a list of lists. ')

    # first_year and last_year MUST be type str:
    if not isinstance(first_year, str):
        raise ExamException('E R R O R: first_year MUST be a string! Your first year is a(n) {}.'.format(type(first_year)))
    
    if not isinstance(last_year, str):
        raise ExamException('E R R O R: first_year MUST be a string! Your first year is a(n) {}.'.format(type(last_year)))

    # First year MUST be lower than last_year, obviously:
    if first_year > last_year:
        print('W A R N I N G: first_year and last_year are in the wrong order! Trying to fix it by inverting them!')
        tmp = first_year
        first_year = last_year
        last_year = tmp
        if first_year < last_year:
            print('S U C C E S S! first_year and last_year have been inverted successfully!')
        else: 
            raise ExamException('E R R O R: Impossible to invert first_year and last_year.')

    # First and last year can't be the same:
    elif first_year == last_year:
        raise ExamException('E R R O R: first and last must be different! ')




    # In order for first_year to be in data.csv, it must not be less than the first year present in the file:
    if first_year < time_series[0][0][:4]:
        raise ExamException('E R R O R: first_year is not present in data.csv!')

    # Same for last_year but now it's the last year of the list the one to be checked:
    if last_year > time_series[-1][0][:4]:
        raise ExamException('E R R O R: last_year is not present in data.csv!')


    # Creating variables:
    dictionary = {}
    
    # Creating dictionary:

    for i in range(len(time_series)):
        # If the key is already present in dictionary, then append the value to the list of values - this is needed in case of duplicates
        if time_series[i][0] in dictionary:
            dictionary[time_series[i][0]].append(time_series[i][1])
        
        # If the key is not present in the dictionary then add the key-value pair
        else:
            dictionary[time_series[i][0]] = []
            dictionary[time_series[i][0]].append(time_series[i][1])

    # Creating a storage for the keys that are needed:
    keys = []

    # Storing first_year value in another variable:
    storage_first_year = first_year

    # Storing all needed keys in a separate list:
    while int(first_year) <= int(last_year):

        # Running through the keys in the dictionary:
        for key in dictionary:
            
            # Taking just the first four digits (the year):
            key_year = key[0:4] 

            # This is needed to exit the for loop when it has processed every key for the current year:
            if int(key_year) > int(first_year):
                break
 
            # Every key for the year gets stored in the previous created list:
            if key_year == first_year:
                keys.append(key)
                        
        # When the cycle is done processing a year, it increases so it can pass on to the next one:
        first_year = str(int(first_year) + 1)

    # Restoring first_year to its initial value:
    first_year = storage_first_year

    # Defining variables: 
    final_list = []
    month_list = []

    # Now the script will loook for every valid value for one month at the time, and will do the maths:
    for month in range(1, 13): # range(x, y) starts at x and ends at (y - 1); there are 12 months
        
        # Going trough every element in the key list:
        for key in keys:

            # If the script finds a key for the month it's processing, it adds it to the list:
            if month == int(key[-2:]): # [-2:] takes the last two digits of the string
                month_list.append(int(dictionary[key][0]))

        # Now the monthly average difference will be calculated:

        # Defining variables:
        avg = 0
        sum = 0

        for i in range(len(month_list) - 1): # range(len(month_list) - 1) cause i starts from 0

            # Caclulating difference:
            sum += month_list[i + 1] - month_list[i]
        
        # if there are more than two variations...
        if len(month_list) >= 2:

            # ...Calculate the average:
            avg = sum/(len(month_list) - 1) # avg = sum / n° of values for that month - 1 

        # Adding the average to the output list:
        final_list.append(avg)

        # Resetting the holding list so it becomes available for the next month
        month_list = [] 

    # Returning the final result:
    return final_list

# ====== #
#  MAIN  #
# ====== #

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(compute_avg_monthly_difference(time_series, '1949', '1953'))