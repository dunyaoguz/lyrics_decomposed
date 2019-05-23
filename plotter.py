from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, Legend, ColumnDataSource, Panel, Tabs, ColumnDataSource, LabelSet

def sentiment_plot(df):
    a = int(df['release_year'].min())
    b = int(df['release_year'].max())
    p = figure(plot_width=1000, plot_height=450, x_range=(a, b), y_range=(0, 0.5), x_axis_label='Years',
               y_axis_label='Percent of sentiments expressed', toolbar_location='above')

    r0 = p.line(df['release_year'], df['disgust'], color='red', line_dash="4 4", line_width=3)
    r1 = p.circle(df['release_year'], df['disgust'], fill_color='red', size=8, color='red')

    r2 = p.line(df['release_year'], df['sadness'], color='navy', line_dash="4 4", line_width=3)
    r3 = p.circle(df['release_year'], df['sadness'], fill_color='navy', size=8, color='navy')

    r4 = p.line(df['release_year'], df['joy'], color='yellowgreen', line_dash="4 4", line_width=3)
    r5 = p.circle(df['release_year'], df['joy'], fill_color='yellowgreen', size=8, color='yellowgreen')

    r6 = p.line(df['release_year'], df['surprise'], color='blueviolet', line_dash="4 4", line_width=3)
    r7 = p.circle(df['release_year'], df['surprise'], fill_color='blueviolet', size=8, color='blueviolet')

    r8 = p.line(df['release_year'], df['fear'], color='orange', line_dash="4 4", line_width=3)
    r9 = p.circle(df['release_year'], df['fear'], fill_color='orange', size=8, color='orange')

    r10 = p.line(df['release_year'], df['anticipation'], color='hotpink', line_dash="4 4", line_width=3)
    r11 = p.circle(df['release_year'], df['anticipation'], fill_color='hotpink', size=8, color='hotpink')

    r12 = p.line(df['release_year'], df['anger'], line_dash="4 4", color='deepskyblue', line_width=3)
    r13 = p.circle(df['release_year'], df['anger'], size=8, color='deepskyblue', fill_color='deepskyblue')

    p.circle(df['release_year'], df['anger'], size=20, fill_color='white', hover_fill_color='deepskyblue',
                     fill_alpha=0.02, hover_alpha=0.2, line_color=None, hover_line_color='deepskyblue')

    p.circle(df['release_year'], df['surprise'], size=20, fill_color='white', hover_fill_color='blueviolet',
                        fill_alpha=0.02, hover_alpha=0.2, line_color=None, hover_line_color='blueviolet')

    p.circle(df['release_year'], df['anticipation'], size=20, fill_color='white', hover_fill_color='hotpink',
                            fill_alpha=0.02, hover_alpha=0.2,line_color=None, hover_line_color='hotpink')

    p.circle(df['release_year'], df['sadness'], size=20, fill_color='white', hover_fill_color='navy',
                      fill_alpha=0.02, hover_alpha=0.2,line_color=None, hover_line_color='navy')

    p.circle(df['release_year'], df['disgust'], size=20, fill_color='white', hover_fill_color='red',
                       fill_alpha=0.02, hover_alpha=0.2, line_color=None, hover_line_color='red')

    p.circle(df['release_year'], df['fear'], size=20, fill_color='white', hover_fill_color='orange',
                    fill_alpha=0.02, hover_alpha=0.2, line_color=None, hover_line_color='orange')

    p.circle(df['release_year'], df['joy'], size=20, fill_color='white', hover_fill_color='yellowgreen',
                   fill_alpha=0.02, hover_alpha=0.2, line_color=None, hover_line_color='yellowgreen')

    legend = Legend(items=[
    ("disgust", [r0, r1]),
    ("sadness", [r2, r3]),
    ("joy", [r4, r5]),
    ("surprise", [r6, r7]),
    ("fear", [r8, r9]),
    ("anticipation", [r10, r11]),
    ("anger", [r12, r13])
    ], location="center")

    TOOLTIPS = """
    <div>
        <div>
            <span style="font-size: 15px;">Year: </span>
            <span style="font-size: 17px; font-weight: bold;">$x{0}</span>
        </div>
        <div>
            <span style="font-size: 15px;">Score: </span>
            <span style="font-size: 17px; color: gray;">$y{(0.000)}</span>
        </div>
    </div>
    """
    p.add_tools(HoverTool(tooltips=TOOLTIPS, mode='mouse'))
    p.add_layout(legend, 'right')
    p.legend.click_policy="hide"
    p.legend.border_line_color = None
    p.background_fill_color = "#f2f2f2"
    p.grid.grid_line_color = "white"
    p.xaxis.major_tick_line_color = 'firebrick'
    p.xaxis.major_tick_line_width = 5
    p.xaxis.minor_tick_line_color = 'orange'
    p.axis.major_tick_out = 10
    p.axis.minor_tick_out = 8
    return p

def view_albums(df):
    a = int(df['release_year'].min())
    b = int(df['release_year'].max())
    source = ColumnDataSource(df)
    p = figure(plot_width=950, plot_height=180, x_range=(a-1, b+1), y_range=(0, 0.5), toolbar_location='above',
    title='View a random sample of max. 5 songs from each album', tools='pan,box_zoom,reset,save')

    p.scatter(df['release_year'], 0.25, marker='square_cross', fill_color='#D3D3D3', line_color='#696969', line_width=1.5, size=15)
    h = p.scatter('release_year', 0.25, marker='square', source=df, size=35, fill_color='white', hover_fill_color='#DCDCDC', fill_alpha=0,
    hover_alpha=0.2, line_color=None, hover_line_color='#DCDCDC')
    TOOLTIPS = """
    <div>
        <div width="10px">
            <span style="font-size: 15px;">Album: </span>
            <span style="font-size: 17px; font-weight: bold;">@album</span>
        </div>
        <div width="10px">
            <span style="font-size: 15px;">Songs: </span>
            <span style="font-size: 17px; color: gray;">@songs</span>
        </div>
    </div>
    """
    p.add_tools(HoverTool(tooltips=TOOLTIPS, renderers=[h], mode='mouse'))
    p.xaxis.major_tick_line_color = 'firebrick'
    p.xaxis.major_tick_line_width = 5
    p.xaxis.minor_tick_line_color = 'orange'
    p.axis.major_tick_out = 10
    p.axis.minor_tick_out = 8
    p.yaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.ygrid.grid_line_color = None
    p.xgrid.grid_line_color = None
    p.outline_line_color = None
    # p.xgrid[0].ticker.desired_num_ticks = 10
    p.yaxis.visible = False
    return p

def cluster_plot(df):
    source = ColumnDataSource(df)
    TOOLTIPS = """
    <div>
        <div>
            <span style="font-size: 15px;">Album: </span>
            <span style="font-size: 17px; font-weight: bold;">@album</span>
        </div>
        <div>
            <span style="font-size: 15px;">Song: </span>
            <span style="font-size: 17px; color: gray;">@title</span>
        </div>
    </div>
    """
    # 3 neighbors
    p1 = figure(toolbar_location="above", plot_width=900, plot_height=450, tools='pan,box_zoom,reset,save',
                x_axis_label='Principal Component 1', y_axis_label='Principal Component 2')
    p1.circle('Component1', 'Component2', size=15, source=df, color='color_3', line_color="black", fill_alpha=0.8, hover_fill_color="black", hover_line_color=None)
    p1.background_fill_color = "#f2f2f2"
    p1.grid.grid_line_color = "white"
    p1.add_tools(HoverTool(tooltips=TOOLTIPS, mode='mouse'))

    # 4 neighbors
    p2 = figure(toolbar_location="above", plot_width=900, plot_height=450, tools='pan,box_zoom,reset,save',
                x_axis_label='Principal Component 1', y_axis_label='Principal Component 2')
    p2.circle('Component1', 'Component2', size=15, source=df, color='color_4', line_color="black", fill_alpha=0.8, hover_fill_color="black", hover_line_color=None)
    p2.background_fill_color = "#f2f2f2"
    p2.grid.grid_line_color = "white"
    p2.add_tools(HoverTool(tooltips=TOOLTIPS, mode='mouse'))

    # 5 neighbors
    p3 = figure(toolbar_location="above", plot_width=900, plot_height=450, tools='pan,box_zoom,reset,save',
                x_axis_label='Principal Component 1', y_axis_label='Principal Component 2')
    p3.circle('Component1', 'Component2', size=15, source=df, color='color_5', line_color="black", fill_alpha=0.8, hover_fill_color="black", hover_line_color=None)
    p3.background_fill_color = "#f2f2f2"
    p3.grid.grid_line_color = "white"
    p3.add_tools(HoverTool(tooltips=TOOLTIPS, mode='mouse'))

    tab1 = Panel(child=p1, title="3 clusters")
    tab2 = Panel(child=p2, title="4 clusters")
    tab3 = Panel(child=p3, title="5 clusters")
    tabs = Tabs(tabs=[tab1, tab2, tab3])
    return tabs
