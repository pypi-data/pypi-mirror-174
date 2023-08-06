import pandas as pd


def summary_col(var, val_counts, stat_type):
    '''
    Calculate summary row for a variable.
    Use pandas value counts to get percentage of respondents in each category.
    '''
    assert len(val_counts) > 0, 'Variable passed has no values'
    df = []
    for val in range(0, len(val_counts)):
        df.append([var, val_counts.index[val],
                   stat_type, val_counts.values[val]])
    return df


def build_summary(all_data, seg_col, var_type, n_seg):
    '''
    Build summary table based on segmentation results
    '''
    summary_df = pd.DataFrame()
    for var in var_type.keys():
        if (var_type[var] == 'Multinomial') | (var_type[var] == 'Ordinal'):
            for seg in range(0, n_seg+1):
                if seg == 0:
                    cur_seg = all_data.copy()
                    cur_var = cur_seg[var].value_counts(
                        normalize=True, dropna=False).sort_index()
                    df = summary_col(var, cur_var, 'col n %')
                    seg_df = pd.DataFrame(
                        df, columns=['var', 'value', 'stat', 'total'])
                else:
                    cur_seg = all_data[all_data[seg_col] == seg].copy()
                    cur_var = cur_seg[var].value_counts(
                        normalize=True, dropna=False).sort_index()
                    df = summary_col(var, cur_var, 'col n %')
                    seg_df = seg_df.merge(pd.DataFrame(df, columns=['var', 'value', 'stat', 'segment_' + str(seg)]).
                                          drop(columns=['stat']),
                                          how='left', left_on=['var', 'value'], right_on=['var', 'value'])
            summary_df = pd.concat([summary_df, seg_df])

        elif var_type[var] == 'Gaussian':
            for seg in range(0, n_seg+1):
                df = []
                if seg == 0:
                    cur_seg = all_data.copy()
                    seg_df = pd.DataFrame([[var, '', 'mean', cur_seg[var].mean()],
                                           [var, '', 'std_dev', cur_seg[var].std()]],
                                          columns=['var', 'value', 'stat', 'total'])
                else:
                    cur_seg = all_data[all_data[seg_col] == seg].copy()
                    seg_df = seg_df.merge(pd.DataFrame([[var, '', 'mean', cur_seg[var].mean()],
                                                        [var, '', 'std_dev', cur_seg[var].std()]],
                                                       columns=[
                                                           'var', 'value', 'stat', 'segment_' + str(seg)]
                                                       ).drop(columns=['value']),
                                          how='left', left_on=['var', 'stat'], right_on=['var', 'stat']
                                          )
            summary_df = pd.concat([summary_df, seg_df])

        elif var_type[var] == 'Binary':
            for seg in range(0, n_seg+1):
                df = []
                if seg == 0:
                    cur_seg = all_data.copy()
                    seg_df = pd.DataFrame([[var, 1, 'col n %', cur_seg[var].mean()]],
                                          columns=['var', 'value', 'stat', 'total'])
                else:
                    cur_seg = all_data[all_data[seg_col] == seg].copy()
                    seg_df = seg_df.merge(pd.DataFrame([[var, '1', 'col n %', cur_seg[var].mean()]],
                                                       columns=[
                                                           'var', 'value', 'stat', 'segment_' + str(seg)]
                                                       ).drop(columns=['value']),
                                          how='left', left_on=['var', 'stat'], right_on=['var', 'stat']
                                          )
            summary_df = pd.concat([summary_df, seg_df])

    summary_df.reset_index(drop=True, inplace=True)
    summary_df['value'].fillna('N/A', inplace=True)
    summary_df.fillna(0, inplace=True)

    # add segment size rows
    seg_counts = all_data[seg_col].value_counts().sort_index().values
    seg_total = sum(seg_counts)
    seg_perc = all_data[seg_col].value_counts(
        normalize=True).sort_index().values
    row0 = ["Count", "", "N", seg_total] + list(seg_counts)
    row1 = ["Percent", "", "%", 1] + list(seg_perc)
    summary_df.loc[-2] = row0
    summary_df.loc[-1] = row1
    summary_df = summary_df.sort_index().reset_index(drop=True)

    return summary_df


def cat_color(val, dark=0.10, light=0.05):
    '''
    Shading colors for categorical variables
    '''
    if pd.isnull(val):
        attr = 'background-color: #ffffff'  # white
    elif val <= dark * -1:
        attr = 'background-color: #c0514d'  # dark red
    elif dark * -1 < val < light * -1:
        attr = 'background-color: #f2dcdb'  # light red
    elif light * -1 <= val < light:
        attr = 'background-color: #ffffff'  # white
    elif light < val < dark:
        attr = 'background-color: #d8e4bc'  # light green
    else:
        attr = 'background-color: #92d050'  # dark green
    return attr


def cont_color(val, std):
    '''
    Shading colors for continuous variables
    '''
    if pd.isnull(val):
        attr = 'background-color: #ffffff'  # white
    elif val <= -0.2*std:
        attr = 'background-color: #c0514d'  # dark red
    elif -0.2*std < val < -0.1*std:
        attr = 'background-color: #f2dcdb'  # light red
    elif -0.1*std <= val < 0.1*std:
        attr = 'background-color: #ffffff'  # white
    elif 0.1*std < val < 0.2*std:
        attr = 'background-color: #d8e4bc'  # light green
    else:
        attr = 'background-color: #92d050'  # dark green
    return attr


def shading(data, driver_list, summary_df, n_seg, dark=0.10, light=0.05):
    '''
    apply shading functions row wise to the summary table
    '''
    assert data.ndim == 1, "Shading is designed to apply row-wise, e.g. axis=1."
    stat_type = data['stat']
    if stat_type == 'col n %':
        total = data['total']
        seg_data = data[list(pd.Series(data.index).str.startswith('segment_'))]
        diff = seg_data - total
        row_shade = ['background-color: #ffffff']*6 + \
            [cat_color(val, dark=dark, light=light) for val in diff]
        if data['var'] in driver_list:
            row_shade[1] = 'background-color: #BFBFBF'
        return row_shade

    elif stat_type == 'mean':
        quest = data['var']
        total = data['total']
        seg_data = data[list(pd.Series(data.index).str.startswith('segment_'))]
        std = summary_df.loc[(summary_df['var'] == quest) & (
            summary_df['stat'] == 'std_dev'), 'total'].values
        diff = seg_data - total
        row_shade = ['background-color: #ffffff'] * \
            6 + [cont_color(val, std) for val in diff]
        if data['var'] in driver_list:
            row_shade[1] = 'background-color: #BFBFBF'
        return row_shade

    elif (stat_type == 'std_dev') | (stat_type == "N") | (stat_type == "%"):
        row_shade = ['background-color: #ffffff']*(6 + n_seg)
        if data['var'] in driver_list:
            row_shade[1] = 'background-color: #BFBFBF'
        return row_shade


def save_xls(dict_df, path):
    """
    Save a dictionary of dataframes to an excel file, with each dataframe as a separate page
    """

    with pd.ExcelWriter(path) as writer:
        for key in dict_df:
            dict_df[key].to_excel(writer, key)