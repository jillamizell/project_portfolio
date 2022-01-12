import pandas as pd
import numpy as np
import statsmodels.stats.api as sms
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap


colors_2 = ["#4096E6", "#40E6DD"]
colors_3 = ["#4096E6", "#53D8FC", "#40E6DD"]
colors_4 = ["#4776FE", "#4096E6", "#40E6DD", "#47FEC1"]
colors_5 = ["#4776FE", "#4096E6", "#53D8FC", "#40E6DD", "#47FEC1"]

# univariate frequency and proportions table
def univar_table(df, w, x, resp):
    """Get table of labeled weighted results (frequencies, proportions, and 95% confidence interval) for a
    single variable.

    Keyword arguments:
    df -- the name of the dataframe or subset
    w -- the name of the survey weight column
    x -- the variable name
    resp -- the dictionary containing the response codes and labels
    """
    #n = round(df[w].sum()) # calculate total n
    freq = df[[x,w]].groupby(x).sum()[w] # get frequency table by summing weight for each group
    labs = freq.index.map(resp[x]) # map response labels to frequency table
    #prop = freq/n # get proportions

    # use stats models to get weighted means and CIs
    temp_df = pd.get_dummies(df[[x,w]], columns = [x]) # dummy the column
    calc_vars = list(temp_df.columns[1:]) # save the names of the dummy variables to a list

    # set up empty lists to save weighted mean and CI info from loop
    mean_list = []
    ci_lo_list = []
    ci_up_list = []

    # for loop that loops through each dummy column to calculate mean (proportion) and CI
    for v in calc_vars:
        temp_mod = sms.DescrStatsW(temp_df[v], weights = temp_df[w]) # create stats model
        mean_list.append(round(temp_mod.mean, 3)) # calculate mean and add to list
        temp_ci = temp_mod.tconfint_mean() # calculate confidence interval
        ci_lo_list.append(round(temp_ci[0], 3)) # save lower CI to list
        ci_up_list.append(round(temp_ci[1], 3)) # save upper CI to list

    # save table as dataframe
    table = pd.DataFrame({'Labels': labs,
                          #'Prop': round(prop, ndigits = 3)*100,
                          'Freq': round(freq).astype('int'),
                          'Prop': [x*100 for x in mean_list],
                          #'Mean': [x*100 for x in mean_list],
                          'CI_lo': [x*100 for x in ci_lo_list],
                          'CI_up': [x*100 for x in ci_up_list]})
    return table

# bivariate frequency, proportions, and confidence interval tables
def bivar_table(df, w, x, y, resp):
    """Returns three tables (proportions, frequencies, and confidence intervals) for weighted crosstabs
    Proportions and means are normalized along the column (y) variable.

    Keyword arguments:
    df -- the dataframe or subset
    w -- the name of the weight column
    x -- the 'row' variable
    y -- the 'column' variable (proportions will sum to 100 for each column)
    resp -- the dictionary containing the response codes and labels
    """
    # get response labels for x and y
    x_labs = resp[x]
    y_labs = resp[y]

    # get weighted column (y) proportions by summing the weights across subgroups and normalizing by column
    tab_prop = pd.crosstab(index = df[x].map(x_labs),
                           columns = df[y].map(y_labs),
                           values = df[w],
                           aggfunc = sum,
                           normalize = 'columns')

    # map x labels to rows and y labels to columns
    tab_prop = tab_prop.loc[x_labs.values()].loc[:,y_labs.values()]

    # round the proportions to 3 digits
    tab_prop = round(tab_prop, ndigits = 3) * 100

    # get weighted frequency table
    tab_freq = pd.crosstab(index = df[x].map(x_labs),
                           columns = df[y].map(y_labs),
                           values = df[w],
                           aggfunc = sum,
                           margins = True)

    # map x labels to rows and y labels to columns
    tab_freq = tab_freq.loc[x_labs.values()].loc[:,y_labs.values()]

    # round frequencies and convert to integer type
    tab_freq = round(tab_freq).astype('int')

    # use stats models to get weighted means and CIs
    temp_df = pd.get_dummies(df[[x,y,w]], columns = [x,y]) # dummy the columns

    # save the names of the dummy variables to a list
    x_vars = temp_df.columns[temp_df.columns.str.startswith(f"{x}_")]
    y_vars = temp_df.columns[temp_df.columns.str.startswith(f"{y}_")]

    # for loop that loops through each dummy column to calculate mean (proportion) and CI
    temp_dict_all = {} # set up the first level dictionary; will contain nested dicts w/ means and cis for eacy y by x

    # loop through each category in the y variable
    for y_var in y_vars:

        # filter where that y category is 1
        temp_subset = temp_df[temp_df[y_var] == 1]

        # set up second level dictionary
        temp_dict_x = {}

        # loop through each category in the x variable
        for x_var in x_vars:
            temp_dict_xy = {} # set up third level dictionary
            temp_mod = sms.DescrStatsW(temp_subset[x_var], weights = temp_subset[w]) # create stats model
            temp_dict_xy['Prop'] = round(temp_mod.mean, 3) # calculate mean
            temp_dict_xy['CI_lo'] = round(temp_mod.tconfint_mean()[0], 3) # calculate confidence interval lower
            temp_dict_xy['CI_up'] = round(temp_mod.tconfint_mean()[1], 3) # calculate confidence interval upper
            temp_dict_x[x_var] = temp_dict_xy # save mean and ci for the x category to the 2nd level dictionary
        temp_dict_all[y_var] = temp_dict_x # save the means and cis for all x categories at each level of y
    tab_ci = pd.DataFrame(temp_dict_all) # convert first level dictionary to dataframe
    tab_ci.columns = resp[y].values() #
    tab_ci.index = resp[x].values()

    return tab_prop, tab_freq, tab_ci

# univariate proportion bar chart
def univar_bar(df, w, x, resp, word, figw=8, figh=8, nudge_dlab=0.5, color=colors_5[2]):
    """Basic bar chart of proportions for single variable.

    Keyword arguments:
    df -- the name of the dataframe or subset
    w -- the name of the survey weight column
    x -- the variable name
    resp -- the dictionary containing the response codes and labels
    word -- the dictionary containing the column name and question wording
    figw -- width of figure (default 8)
    figh -- figure height (default 8)
    nudge_dlab -- amount to nudge data label (default 0.5)
    color -- bar color (default seagreen)
    """
    tab = univar_table(df, w, x, resp)

    fig = plt.figure(figsize = (figw, figh))
    ax = fig.add_axes([1, 1, 1, 1])
    ax.barh(y = tab['Labels'], width = tab['Prop'], color = color)
    ax.set_title(textwrap.fill(word[x], 50), fontsize = 14)
    ax.set_xticks([])
    ax.set_xlim(right = tab['Prop'].max()+nudge_dlab)
    ax.set_yticks(tab['Labels'])
    ax.tick_params(axis='y', length=0)
    ax.set_yticklabels(labels = tab['Labels'].apply(lambda x: textwrap.fill(x, 50)), fontsize=16)

    for x,y in zip(tab['Prop'], tab['Labels']):
        label = f"{round(x, ndigits = 2)}%"
        ax.annotate(label,
                    (x+nudge_dlab,y),
                    ha='center',
                    va='center',
                    fontsize = 14,
                    weight = 'bold')
    sns.despine(bottom=True, left=True)
    return plt.show();

# bivariate proportion bar chart
def bivar_bar(df, w, x, y, resp, word, figw=12, figh=8):
    """Bivariate 100% stacked horizontal bar chart.

    Keyword arguments:
    df - the dataframe or subset
    w -- the name of the weight column
    x -- the 'row' variable
    y -- the 'column' variable (proportions will sum to 100 for each column)
    resp -- the dictionary containing the response codes and labels
    word -- the dictionary containing the column name and question wording
    figw -- width of figure (default 12)
    figh -- figure height (default 8)
    """
    prop, freq, ci = bivar_table(df, w, x, y, resp)
    if len(resp[x]) == 2:
        c = colors_2
    elif len(resp[x]) == 3:
        c = colors_3
    elif len(resp[x]) == 4:
        c = colors_4
    else:
        c = colors_5
    fig, ax = plt.subplots(figsize = (figw,figh))
    ax.set_xticks([])
    ax.invert_yaxis()
    plt.yticks(fontsize = 16)
    ax.tick_params(axis='y', length=0)
    left = [0] * len(resp[y])
    for i in range(0, len(resp[x])):
        r = prop.iloc[i]
        ax.barh(prop.columns, r.values, label=r.name, left = left, color = c[i])
        for a,b,l in zip(r.values, prop.columns, left):
            label = f"{round(a)}%"
            ax.annotate(label, ((a/2)+l,b), ha='center', va='bottom', fontsize = 14, weight = "semibold")
        for a,b,l,z in zip(freq.iloc[i].values, prop.columns, left, r.values):
            label = f"({round(a)})"
            ax.annotate(label, ((z/2)+l,b), ha='center', va='top', fontsize = 14)
        left += r.values

    plt.title(textwrap.fill(word[x], 50) + "\n" + textwrap.fill(word[y], 50), fontsize = 20)
    plt.legend(loc = 'upper left', bbox_to_anchor = (1,1), frameon = False, fontsize = 14)
    sns.despine(left = True, bottom = True)

    return plt.show();

# bivariate bubble chart with confidence interval bar
def bivar_ci(df, w, x, y, resp, word, figw = 12, figh = 4):
    """Bivariate bubble chart with confidence interval.

    Keyword arguments:
    df - the dataframe or subset
    w -- the name of the weight column
    x -- the 'row' variable
    y -- the 'column' variable (proportions will sum to 100 for each column)
    resp -- the dictionary containing the response codes and labels
    word -- the dictionary containing the column name and question wording
    figw -- width of figure (default 12)
    figh -- figure height (default 4)
    """
    prop, freq, ci = bivar_table(df, w, x, y, resp)
    tab = ci.T
    if len(tab.columns) == 2:
        c = colors_2
    elif len(tab.columns) == 3:
        c = colors_3
    elif len(tab.columns) == 4:
        c = colors_4
    else:
        c = colors_5
    fig, ax = plt.subplots(figsize = (figw,figh))
    y_ax = list(range(len(tab.index)))
    ax.set_yticks(ticks = y_ax, labels = tab.index, fontsize = 14)
    ax.set_xlim(0, 1)
    for x_cat in list(range(len(tab.columns))):
        col = tab.columns[x_cat]
        x_ax = [x['Prop'] for x in tab[col]]
        xmin = [x['CI_lo'] for x in tab[col]]
        xmax = [x['CI_up'] for x in tab[col]]
        ax.scatter(x = x_ax, y = y_ax, s = 200, color = c[x_cat], label = col)
        ax.hlines(y = y_ax, xmin = xmin, xmax = xmax, color = c[x_cat], linewidth = 5)

    ax.legend(fontsize = 12, frameon = False)
    sns.despine()
    fig.tight_layout(rect = [0, 0, 1, 0.9])
    #fig.suptitle(f"{word[x]}", fontsize = 16, ha = 'center', va = 'bottom')
    fig.suptitle(textwrap.fill(word[x], 50) + "\n" + textwrap.fill(word[y], 50), fontsize = 16, ha = 'center', va = 'bottom')
    return plt.show();

# heatmap of cluster averages for each of the variables in the cluster model
def cluster_heatmap(df, w, clust_vars, clust_col, resp, word, feature_labels, figw=12, figh=16):
    """Heatmap for cluster averages.

    Keyword arguments:
    df - the dataframe or subset
    w -- the name of the weight column
    clust_vars -- the subset of variables in the cluster model
    clust_col -- the column containing the clusters to analyze
    resp -- the dictionary containing the response codes and labels
    word -- the dictionary containing the column name and question wording
    feature_labels -- dictionary mapping y index values to labels
    figw -- width of figure (default 12)
    figh -- figure height (default 16)
    """

    # set up empty dataframe
    mean_df = pd.DataFrame(index = clust_vars)

    # for loop goes through each cluster
    for cluster in np.sort(df[clust_col].unique()):

        # filtering the data to the cluster of focus in the loop
        sub_df = df.loc[df[df[clust_col] == cluster].index, : ]

        # set up empty list to hold the averages
        mean_list = []

        # loop within loop - captures variable weighted averages for cluster of focus
        for var in clust_vars:
            mean_list.append(np.average(sub_df[var], weights = sub_df[w]))

        # saves weighted averages to dataframe
        #colname = f"cluster{cluster}"
        temp_ser = pd.Series(mean_list, index = clust_vars, name = resp[clust_col][cluster])
        mean_df = mean_df.join(temp_ser)

    # normalizes averages by row - for color formatting the heatmap
    # each row represents one of the variables in the clustering model
    # set up empty list
    tmp_array = []

    # loop through each row of cluster averages to create embedded array of averages normalized by row
    for row in mean_df.index:
        tmp_min = mean_df.loc[row].min() # obtain the minimum for that row
        tmp_max = mean_df.loc[row].max() # obtain the maximum for that row

        # normalizes each average in a row based on that row's min and max
        tmp_array.append([(x-tmp_min)/(tmp_max-tmp_min) for x in mean_df.loc[row]])

    # save normalized averages to dataframe
    norm_df = pd.DataFrame(tmp_array, index = clust_vars, columns = mean_df.columns)

    # generate heatmap
    # set figure size
    plt.figure(figsize = (figw,figh))

    # create heatmap
    sns.heatmap(norm_df, # uses the dataframe of averages normalized by row min/max
                annot = round(mean_df, 2), # add data labels - uses the original dataframe of averages
                cmap = 'mako', # add color
                cbar = True, # add color bar legend
                square = True, # format heatmap cells to be square shaped
                annot_kws = {'fontsize': 12, 'weight': 'bold'}, # format data label font size and appearance
                cbar_kws = {'label': "<<< Less Agreement....................More Agreement >>>", # add label to color bar
                            'ticks': [], # remove ticks from color bar legend
                            'orientation': 'horizontal', # change color bar appearance from vertical to horizontal
                            'shrink': 0.4, # reduce size of color bar
                            'pad': 0.1}, # reduce padding between axis title and color bar
                yticklabels = norm_df.index.map(feature_labels))
    plt.tight_layout(rect = [0,0,1,1])
    plt.title(f"Cluster Averages for Features in the Cluster Model\n{word[clust_col]}", fontsize = 20,
              pad = 50,
              ha = 'center', va = 'center', x = 0)
    plt.xlabel(f"{word[clust_col]}", fontsize = 20, labelpad = 20)
    plt.ylabel('Features Included in Cluster Model', fontsize = 20)
    plt.xticks(rotation = 90, fontsize = 14)
    plt.yticks(fontsize = 14);
