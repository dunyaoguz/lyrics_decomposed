from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, Legend, ColumnDataSource

def sentiment_plot(df):
    a = int(df['release_year'].min())
    b = int(df['release_year'].max())
    p = figure(plot_width=900, plot_height=450, x_range=(a, b), y_range=(0, 0.5), x_axis_label='Years',
               y_axis_label='Percent of sentiments expressed', toolbar_location='above')

    p.line(df['release_year'], df['disgust'], legend='disgust', color='red', line_dash="4 4", line_width=3, muted_color='red', muted_alpha=0.2)
    p.circle(df['release_year'], df['disgust'], legend='disgust', fill_color='red', size=8, color='red', muted_color='red', muted_alpha=0.2)

    p.line(df['release_year'], df['sadness'], legend='sadness', color='navy', line_dash="4 4", line_width=3, muted_color='navy', muted_alpha=0.2)
    p.circle(df['release_year'], df['sadness'], legend='sadness', fill_color='navy', size=8, color='navy', muted_color='navy', muted_alpha=0.2)

    p.line(df['release_year'], df['joy'], legend='joy', color='yellowgreen', line_dash="4 4", line_width=3, muted_color='yellowgreen', muted_alpha=0.2)
    p.circle(df['release_year'], df['joy'], legend='joy', fill_color='yellowgreen', size=8, color='yellowgreen', muted_color='yellowgreen', muted_alpha=0.2)

    p.line(df['release_year'], df['surprise'], legend='surprise', color='blueviolet', line_dash="4 4", line_width=3, muted_color='blueviolet', muted_alpha=0.2)
    p.circle(df['release_year'], df['surprise'], legend='surprise', fill_color='blueviolet', size=8, color='blueviolet', muted_color='blueviolet', muted_alpha=0.2)

    p.line(df['release_year'], df['fear'], legend='fear', color='orange', line_dash="4 4", line_width=3, muted_color='orange', muted_alpha=0.2)
    p.circle(df['release_year'], df['fear'], legend='fear', fill_color='orange', size=8, color='orange', muted_color='orange', muted_alpha=0.2)

    p.line(df['release_year'], df['anticipation'], legend='anticipation', color='hotpink', line_dash="4 4", line_width=3, muted_color='hotpink', muted_alpha=0.2)
    p.circle(df['release_year'], df['anticipation'], legend='anticipation', fill_color='hotpink', size=8, color='hotpink', muted_color='hotpink', muted_alpha=0.2)

    p.line(df['release_year'], df['anger'], legend='anger', line_dash="4 4", color='deepskyblue', line_width=3, muted_color='deepskyblue', muted_alpha=0.2)
    p.circle(df['release_year'], df['anger'], legend='anger', size=8, color='deepskyblue', fill_color='deepskyblue', muted_color='deepskyblue', muted_alpha=0.2)

    anger = p.circle(df['release_year'], df['anger'], size=30, fill_color='white', hover_fill_color='deepskyblue',
                     fill_alpha=0.02, hover_alpha=0.3, line_color=None, hover_line_color='deepskyblue')

    surprise = p.circle(df['release_year'], df['surprise'], size=30, fill_color='white', hover_fill_color='blueviolet',
                        fill_alpha=0.02, hover_alpha=0.3, line_color=None, hover_line_color='blueviolet')

    anticipation = p.circle(df['release_year'], df['anticipation'], size=30, fill_color='white', hover_fill_color='hotpink',
                            fill_alpha=0.02, hover_alpha=0.3,line_color=None, hover_line_color='hotpink')

    sadness = p.circle(df['release_year'], df['sadness'], size=30, fill_color='white', hover_fill_color='navy',
                      fill_alpha=0.02, hover_alpha=0.3,line_color=None, hover_line_color='navy')

    disgust = p.circle(df['release_year'], df['disgust'], size=30, fill_color='white', hover_fill_color='red',
                       fill_alpha=0.02, hover_alpha=0.3, line_color=None, hover_line_color='red')

    fear = p.circle(df['release_year'], df['fear'], size=30, fill_color='white', hover_fill_color='orange',
                    fill_alpha=0.02, hover_alpha=0.3, line_color=None, hover_line_color='orange')

    joy = p.circle(df['release_year'], df['joy'], size=30, fill_color='white', hover_fill_color='yellowgreen',
                   fill_alpha=0.02, hover_alpha=0.3, line_color=None, hover_line_color='yellowgreen')

    p.add_tools(HoverTool(tooltips=[("Year", "$x{0}"), ("Score", "$y{(0.000)}")],
                          renderers=[anger, sadness, surprise, fear, anticipation, disgust, joy], mode='mouse'))
    p.legend.click_policy="hide"
    p.background_fill_color = "#f2f2f2"
    p.grid.grid_line_color = "white"
    p.xaxis.major_tick_line_color = 'firebrick'
    p.xaxis.major_tick_line_width = 5
    p.xaxis.minor_tick_line_color = 'orange'
    p.axis.major_tick_out = 10
    p.axis.minor_tick_out = 8
    return p
