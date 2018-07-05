from IPython.display import clear_output, display, HTML
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, VBox, HBox

def df_view(df, columns=None, drop_columns=None, where=None, chunksize=15):
    """
    (general) Show data viewer widget with a slider widget.
    Kwargs:
        df -- dataframe to browse
        columns(optional) -- columns to view
        drop_columns(optional) -- columns to exclude in the widget
        where(optional) -- query string
    """
    def f(x):
        clear_output(wait=True)
        print("Searching from "+str(x)+'...')
        if where!=None:
            ret=df.query(where)
        else:
            ret=df
        if drop_columns!=None:
            ret=ret.drop(drop_columns, axis=1)
        if columns!=None:
            ret=ret[columns]
        ret=ret.ix[x:x+chunksize]
        clear_output(wait=True)
        if len(ret)==0: print("No Results.")
        return ret
    
    nrows=len(df)
    return interact(f, x=widgets.IntSlider(min=0, max=(nrows-1), step=1, value=0, continuous_update=False))
    

def hdf_view(hdf_path, table_name, columns=None, drop_columns=None, where=None, chunksize=15):
    """Show data viewer widget for a hdf table

    Keyword arguments:
    hdf_path -- file name of a hdf file
    table_name -- name of a hdf table
    columns(optional) -- columns to view
    drop_columns(optional) -- columns to exclude in the widget
    where(optional) -- query string
    """
    def f(x):
        clear_output(wait=True)
        print("Searching from "+str(x)+'...')
        ret=None
        with store(hdf_path,'r') as s:
            for r in s.select(table_name, columns=columns, where=where, start=x, chunksize=chunksize):
                ret=r
                if drop_columns!=None:
                    ret=ret.drop(drop_columns, axis=1)
                break
        clear_output(wait=True)
        if len(ret)==0: print("No Results.")
        return ret
    with store(hdf_path) as s:
        nrows=s.get_node(table_name).table.nrows
    return interact(f, x=widgets.IntSlider(min=0, max=(nrows-1), step=1, value=0, continuous_update=False))