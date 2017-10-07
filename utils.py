from pandas import *
import matplotlib.pyplot as plt
import os



def get_csv_data(symbols,base_dir="C:/"):
    
    """Read stock data (close) for given symbols from CSV files."""
    
    for symbol in symbols:
        #Read the data (Date, Close)
        df_temp = pandas.read_csv(symbol_to_path(symbol,base_dir),index_col='date',
                                  parse_dates = True, usecols = ['date','close','open'],
                                  na_values = ['-'])
        df_temp.index = pandas.to_datetime(df_temp.index)

    return df_temp


def symbol_to_path(symbol, base_dir="C:/"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def csv_to_df(symbols, base_dir="C:/"):
    """Read .csv file and returns pandas dataframe."""
    df = get_csv_data(symbols,base_dir)
    return df

def plot_selected(df, indicators, plot_id = 100):
    plt.figure(plot_id)
    i=1
    horiz_line_data = np.array([0 for j in xrange(len(df))])
     
    for indicator in indicators:
        plt.subplot(2, 1, i)
        plt.plot(df.index,df[indicator].values,label = indicator)
        if i == 2:
            plt.plot(df.index, horiz_line_data, 'r--')
        plt.legend(loc='best')
        i = i + 1
        
    plt.show()

def df_to_array(df,column):
    return df[column].values