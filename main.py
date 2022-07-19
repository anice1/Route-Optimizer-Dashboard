from click import edit
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from import_data import load_data
import numpy as np

# Import data
df = load_data()

with st.sidebar:
    selectbox = st.selectbox('Operation', ['Dashboard','Tabular Data'])


if selectbox == 'Dashboard':
    from dashboard import load_dashobard
    load_dashobard()

# display data
if selectbox == 'Tabular Data':
    st.title('🗃 Delivery Request Database')
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_default_column(groupable=False, editable=True)
    gd.configure_selection(selection_mode='multiple',use_checkbox=True)
    gd.configure_side_bar()
    
    st.download_button(
     label="Download data as CSV",
     data=df.to_csv().encode('utf-8'),
     file_name='large_df.csv',
     mime='text/csv'
     )

    df_grid = AgGrid(df, height=400, gridOptions=gd.build(),update_mode=GridUpdateMode.SELECTION_CHANGED, theme='light')
    if df_grid['selected_rows']:
        st.dataframe(pd.DataFrame(df_grid['selected_rows'][0], index=np.arange(len(df_grid['selected_rows'][0]))))
    

    # st.write('### Data Summary')
    # AgGrid(df.describe(), fit_columns_on_grid_load=False)
