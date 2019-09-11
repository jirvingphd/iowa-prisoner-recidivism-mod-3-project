# functions_for_project.py
import bs_ds as bs


def evaluate_catboost_model(model,  X_train,X_test,y_train,y_test,test_pool=None, train_pool=None,
                             binary_classes=True, conf_matrix_classes= ['Decrease','Increase'],
                            normalize_conf_matrix=True,conf_matrix_figsize=(8,4),cmap=None, barcolor='blue',
                            save_conf_matrix_png=False, conf_mat_filename= 'results/confusion_matrix.png',
                             auto_unique_filenames=True):

    """Evaluates kera's model's performance, plots model's history,displays classification report,
    and plots a confusion matrix.
    conf_matrix_classes are the labels for the matrix. [negative, positive]
    Returns df of classification report and fig object for  confusion matrix's plot."""

    from sklearn.metrics import roc_auc_score, roc_curve, classification_report,confusion_matrix
    import bs_ds as bs
    from catboost.utils import get_roc_curve
    from sklearn.metrics import auc,accuracy_score, recall_score, balanced_accuracy_score, classification_report, roc_auc_score, precision_score

    from IPython.display import display
    import pandas as pd
    import matplotlib as mpl
    numFmt = '.4f'
    num_dashes = 30

    # results_list=[['Metric','Value']]
    # metric_list = ['accuracy','precision','recall','f1']
   
    print('\n')
    print('---'*num_dashes)
    print('\tCLASSIFICATION REPORT:')
    print('---'*num_dashes)
    # print('---'*num_dashes)
    # print('\tEVALUATE MODEL:')
    # print('---'*num_dashes)

    ## Get model predictions
    y_hat_train = model.predict(X_train)
    y_hat_test_prob = model.predict_proba(X_test)
    y_hat_test = model.predict(X_test)

    if y_test.ndim>1 or binary_classes==False:
        if binary_classes==False: 
            pass
        else:
            binary_classes = False
            print(f"[!] y_test was >1 dim, setting binary_classes to False")
        
        ## reduce dimensions of y_train and y_test
        y_train = y_train.argmax(axis=1)
        y_test = y_test.argmax(axis=1)


    # Print catboost accuracy report
    print(f'Accuracy:{accuracy_score(y_test, y_hat_test):.2f}')
    print(f'Recall:{recall_score(y_test, y_hat_test):.2f}')
    print(f'Precision:{precision_score(y_test, y_hat_test):.2f}')
    # Get roc-auc curve from catboost
    fpr, tpr, thresholds = get_roc_curve(model, test_pool, thread_count=-1)
    print(f'AUC:{auc(fpr,tpr):.2f}')




    ## Get sklearn classification report 
    report_str = classification_report(y_test,y_hat_test)
    report_dict = classification_report(y_test,y_hat_test,output_dict=True)
    
    
    try:
        ## Create and display classification report
        # df_report =pd.DataFrame.from_dict(report_dict,orient='columns')#'index')#class_rows,orient='index')
        df_report_temp = pd.DataFrame(report_dict)
        df_report_temp = df_report_temp.T#reset_index(inplace=True)

        df_report = df_report_temp[['precision','recall','f1-score','support']]
        display(df_report.round(4).style.set_caption('Classification Report'))
        # print('\n')
    
    except:
        print(report_str)
        # print(report_dict)
        df_report = pd.DataFrame()


        


    # print('---'*num_dashes)
    # print('\tCLASSIFICATION REPORT:')
    # print('---'*num_dashes)
    
    ## Create and plot confusion_matrix
    import matplotlib.pyplot as plt
    conf_mat = confusion_matrix(y_test, y_hat_test)

    # with plt.rc_context(rc={'figure.figsize':conf_matrix_figsize}): # rcParams['figure.figsize']
    fig,ax = plot_confusion_matrix(conf_mat,classes=conf_matrix_classes, cmap=cmap,
                                normalize=normalize_conf_matrix, figsize=conf_matrix_figsize)

    if save_conf_matrix_png:
        fig.savefig(conf_mat_filename,facecolor='white', format='png', frameon=True)


    ## roc_auc curve
    print("\n")
    fig_auc = plot_auc_roc_curve(y_test,y_hat_test_prob)
    print("\n")

    
    print('---'*num_dashes)
    print('\tFEATURE IMPORTANCE:')
    print('---'*num_dashes)

    ## feature_importance 
    fig, ax = plot_feature_importance(model.feature_names_, model.feature_importances_,barcolor=barcolor)
    plt.show()

    return df_report




def plot_auc_roc_curve(y_test, y_test_pred,figsize=(8,4)):
    """ Takes y_test and y_test_pred from a ML model and plots the AUC-ROC curve."""
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_auc_score, roc_curve

    auc = roc_auc_score(y_test, y_test_pred[:,1])
    FPr, TPr, thresh  = roc_curve(y_test, y_test_pred[:,1])
    
    # set font style dicts
    tick_font_dict = {"size":14,"family":"serif"}
    xy_title_dict={"size":20,"family":"serif"}
    title_fontdict={"size":20,"family":"serif"}
    
    
    
    fig,ax=plt.subplots(figsize=figsize)
    ax.plot(FPr, TPr,label=f"AUC for Classifier:\n{round(auc,2)}" )
    ax.plot([0, 1], [0, 1],  lw=2,linestyle='--')
    
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.05])


    # # set axes ticks
    # ax.set_xticks(ticks=tick_marks)
    # ax.set_yticks(ticks=tick_marks)

    # # set axes tick labels
    # ax.set_xticklabels(tick_labels,fontdict=tick_font_dict)
    # ax.set_yticklabels(tick_labels,fontdict=tick_font_dict)

    # set axes labels
    ax.set_xlabel('False Positive Rate',fontdict=xy_title_dict,labelpad=10)
    ax.set_ylabel('True Positive Rate',fontdict=xy_title_dict,labelpad=10)
    ax.set_title('Receiver operating characteristic (ROC) Curve',fontdict=title_fontdict)


    ax.legend(loc="lower right")


    plt.show()
    return fig,ax


def plot_feature_importance(feature_names,feature_importance,fgisize=(6,3),barcolor='blue'):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    fig,ax = plt.subplots(figsize=(10,6))
    important_features = pd.DataFrame({'Features':feature_names,
                                    'Importance':feature_importance})

    important_features.sort_values(by='Importance',inplace=True,ascending=False)
    ax = sns.barplot(y='Features',x='Importance',data=important_features,color=barcolor)

    ytitle = ax.get_ylabel()
    ax.set_ylabel(ytitle,**{'size':14,'family':'serif'})
    
    xtitle = ax.get_xlabel()
    ax.set_xlabel(xtitle,**{'size':14,'family':'serif'})

    labels = ax.get_ymajorticklabels()
    ax.yaxis.set_ticklabels(labels,**{'size':12,'family':'serif'});

    return fig,ax



def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=None, figsize=(5,5),verbose=0):
    """Check if Normalization Option is Set to True. If so, normalize the raw confusion matrix before visualizing
    #Other code should be equivalent to your previous function."""
    import warnings
    warnings.warn('Future versions will be moving plot_confusion_matrix to bs_ds.glassboxes module.')
    import numpy as np
    import itertools
    import matplotlib.pyplot as plt

    if cmap is None:
        cmap ="Blues"
    cmap = plt.get_cmap(cmap)
    


    ## Normalize cm along the y-axis 
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        if verbose>0:
            print("Normalized confusion matrix")
    else:
        if verbose>0:
            print('Confusion matrix, without normalization')

    if verbose>0:
        print(cm)

    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(visible=False)

    # set tick properties
    tick_marks = np.arange(2)
    tick_labels = ['Non-Recidivist','Recidivist']

    # set font style dicts
    tick_font_dict = {"size":14,"family":"serif"}
    xy_title_dict={"size":20,"family":"serif"}
    cm_labels_fontdict={'size':16,'family':'serif'}
    title_fontdict = {'size':18,'family':'serif'}

    # set axes ticks
    ax.set_xticks(ticks=tick_marks)
    ax.set_yticks(ticks=tick_marks)

    # set axes tick labels
    ax.set_xticklabels(tick_labels,fontdict=tick_font_dict)
    ax.set_yticklabels(tick_labels,fontdict=tick_font_dict)

    # set axes labels
    ax.set_xlabel('Predicted Class',fontdict=xy_title_dict,labelpad=10)
    ax.set_ylabel('True Class',fontdict=xy_title_dict,labelpad=10)

    # show cmrix
    ax.imshow(cm, interpolation='nearest',cmap=cmap)

    # set number format and threshold for font color
    fmt = ".2f" 
    threshold = cm.max()/2

    for i,j in itertools.product(range(cm.shape[0]),
                                range(cm.shape[1])):
        
        plt.text(j,i, format(cm[i,j],fmt),
                horizontalalignment='center', fontdict=cm_labels_fontdict,
                color="white" if cm[i,j]>threshold else "black")

    plt.title(title,fontdict=title_fontdict)
    return fig, ax



def plot_hist_by_group(df, groupby_col='age_code',plot_col='recidivist',
                    barh=False, stacked=False, figsize=(8,6),label_map=None,title='Recidivism by Age',
                      xlabel='Group',rot=45):
    import pandas as pd
    import matplotlib.pyplot as plt
    
    font_dict= {}
    font_dict['title'] = {'size':18, 'family':'serif'}
    font_dict['ax_labels'] = {'size':16,'family':'serif'}
    font_dict['ticks'] = {'size':14,'family':'serif'}
    
    ## Get value counts as a dataframe
    counts = df.groupby(groupby_col)[plot_col].value_counts().unstack()
    counts.name='counts'
    counts = pd.DataFrame(counts)
    
    ## Map labels onto value_counts index
    if label_map is not None:
        counts[xlabel] = counts.index.to_series().apply(lambda x: label_map[x])
        counts.set_index(xlabel,inplace=True,drop=False)

    else:
        counts[xlabel] = counts.index.to_series()
        counts.set_index(xlabel,inplace=True,drop=True)        
    
    
    fig,ax=plt.subplots(figsize=figsize)
    ax.set_title(title,fontdict=font_dict['title'])

    if barh==False:
        counts.plot(kind='bar',stacked=stacked,ax=ax,rot=45)
        ax.set_ylabel('# of Prisoners', fontdict=font_dict['ax_labels'])
        ax.set_xlabel(xlabel,fontdict=font_dict['ax_labels'])
    else:
        counts.plot(kind='barh',stacked=stacked,ax=ax,rot=rot)
        ax.set_xlabel('# of Prisoners', fontdict=font_dict['ax_labels'])
        ax.set_ylabel(xlabel,fontdict=font_dict['ax_labels'])

    # ax.set_ylabel('# of Prisoners', fontdict=font_dict['ax_labels'])
    # ax.set_xlabel(xlabel,fontdict=font_dict['ax_labels'])
    ax.tick_params(labelsize= font_dict['ticks']['size'])

    plt.tight_layout()
    plt.show()
    return fig,ax