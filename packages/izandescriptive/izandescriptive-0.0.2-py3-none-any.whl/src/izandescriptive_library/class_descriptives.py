from turtle import title
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid",font_scale=2)
import ptitprince as pt

class desc_analysis:

    # Constructor with parameters
    def __init__(self, data) :
        self.data = data
    
    def graphic(self):
        df_in = pd.read_csv(self.data).select_dtypes(include='number') 
        print('\n' + '\033[1m' + "DESCRIPTIVE ANALYSIS" + '\033[0m')
       
        df_in.hist(bins=25,figsize=(18,20),color='#86bf91',zorder=2, rwidth=0.9)

        
        for i in df_in.columns:
            pal = "Set2"
            f, ax = plt.subplots(figsize=(7, 5))
            ax=pt.half_violinplot( x = i,  data = df_in, palette = pal, bw = .2, cut = 0., scale = "area", width = .6, inner = None, orient = 'h')
            ax=sns.stripplot( x = i,  data = df_in, palette = pal, edgecolor = "white", size = 3, jitter = 1, zorder = 0, orient = 'h')
            ax=sns.boxplot( x = i, data = df_in, color = "black", width = .15, zorder = 10,\
            showcaps = True, boxprops = {'facecolor':'none', "zorder":10},\
            showfliers=True, whiskerprops = {'linewidth':2, "zorder":10},\
            saturation = 1, orient = 'h')

        
        sns.heatmap(df_in.corr(), cmap = 'Greens',xticklabels=df_in.columns, yticklabels=df_in.columns).set_title('Heatmap')
            