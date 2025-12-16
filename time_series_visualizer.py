import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
    'fcc-forum-pageviews.csv', 
    parse_dates = True, 
    index_col = 'date'
    )

# Clean data
df = df[
    (df['value'] > df['value'].quantile(0.025)) &
    (df['value'] < df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (15,5))

    ax.plot(df, color = 'r')
    ax.set_ylabel('Page Views')
    ax.set_xlabel('Date')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = (
        df.groupby([df.index.year,df.index.month_name()])
        .agg({'value':'mean'})
        .reset_index(names = ['Year','Month'])
    )

    months = [month.capitalize() for month in calendar.month_name if month]
    df_bar['Month'] = pd.Categorical(df_bar['Month'],months)
    df_bar = df_bar.sort_values(by = ['Year','Month'])
    df_bar = df_bar.pivot(columns = 'Month', index = 'Year').fillna(0)
    df_bar.columns = df_bar.columns.droplevel(0)
    df_bar.columns.name = 'Months'
    
    # Draw bar plot
    fig, ax = plt.subplots()
    
    df_bar.plot.bar(
        xlabel = 'Years', 
        ylabel = 'Average Page Views',
        ax = ax
    )

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    month_abbr = [i for i in calendar.month_abbr if i.strip()]
    df_box['month'] = pd.Categorical(df_box['month'], month_abbr)
    
    fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = (15,5))
    fliersize = 1
    bottom, top = 0, 200000

    sns.boxplot(data = df_box[['year','value']].set_index('year').T, ax = axs[0], fliersize = fliersize)
    axs[0].set_yticks(range(bottom, top + 1, 20000))
    axs[0].set_ylabel('Page Views')
    axs[0].set_xlabel('Year')
    axs[0].set_title('Year-wise Box Plot (Trend)')

    sns.boxplot(data = df_box[['month','value']].sort_values('month').set_index('month').T, ax = axs[1], fliersize = fliersize)
    axs[1].set_yticks(range(bottom, top + 1, 20000))
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_ylabel('Page Views')
    axs[1].set_xlabel('Month')
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
