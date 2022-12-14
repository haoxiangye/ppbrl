import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os

from ByrdLab.library.cache_io import load_file_in_cache
from matplotlib import rcParams

import argparse
parser = argparse.ArgumentParser(description='Plotter for robust TD')

parser.add_argument('--task', type=str, default='SR_mnist',
    help='task performed (LR_ijcnn1, SR_mnist, etc)')
parser.add_argument('--graph', type=str, default='ER',
    help='name of the graph (ER, TwoCastle)')
parser.add_argument('--partition', type=str, default='iid',
    help='name of the partition (TrivalDist)')
parser.add_argument('--workspace', type=str, nargs='+', default=[],
    help='workspace')
parser.add_argument('--mark_on_title', type=str, default='',
    help='mark_on_title')
parser.add_argument('--portrait', action='store_true',
    help='use portrait layout or landscape layout')

args = parser.parse_args()

task_name = args.task
partition_name = args.partition
graph_name = args.graph
workspace = args.workspace
mark_on_title = args.mark_on_title
if mark_on_title != '':
    mark_on_title = '_' + mark_on_title

__FILE_DIR__ = os.path.dirname(os.path.abspath(__file__))
__CACHE_DIR__ = 'record'
__CATCH_PATH__ = os.path.join(__FILE_DIR__, os.path.pardir, __CACHE_DIR__)

def optimal_gap(path, Fmin):
    return [p-Fmin for p in path]

SCALE = 2.0
FONT_SIZE = 20
#LINE_STYLE = '-'
#LINE_STYLE = 'v-'

pic_name = 'dec_' + task_name + '_' + graph_name + '_' + partition_name

colors = ['red', 'red', 'blue', 'blue', 'green', 'green']
linestyles = ['-', '--', '-', '--', '-', '--']

# aggregations = [
#     # ('mean', 'mean', 'royalblue'), 
#     ('meanW', 'meanW', 'pink'), 
#     ('geometric_median', 'geometric median', 'darkorange'), 
#     ('Krum', 'Krum', 'olivedrab'), 
#     ('median', 'median', 'darkmagenta'),
#     ('trimmed_mean', 'trimmed mean', 'peru'),
#     ('remove_outliers', 'remove outliers', 'skyblue'),
#     ('FABA', 'FABA', 'royalblue'), 
#     ('RSA', 'RSA', 'slategrey'),
# ]

aggregations = [
    # ('mean', 'mean'), 
    #('meanW', 'mean'),
    #('geometric_median', 'geometric median'),
    #('median', 'median'),
    #('Krum', 'Krum'),
    #('noisyKrum', 'noisyKrum'),
    ('trimmed_mean', 'trimmed mean'),
    ('noisytrimmed_mean', 'trimmed mean+noise'),
    ('SCC', 'SCC'),
    ('noisySCC', 'SCC+noise'),
    ('ios', 'IOS'),
    ('noisyios', 'IOS+noise'),
    # ('remove_outliers', 'remove outliers'),
    # ('bulyan', 'Bulyan'),
    #('RSA', 'RSA'),
    #('noisyRSA', 'noisyRSA'),
    #('FABA', 'FABA'),
]
attackNames = [
    ('no attack', 'without attack'),
    ('Gaussian', 'Gaussian attack'),
    ('sign-flipping', 'sign flipping attack'),
    ('isolating', 'isolation attack'),
]

if args.portrait:
    fig, axColumn = plt.subplots(len(attackNames), 2)
    if len(attackNames) == 1:
        axColumn = [axColumn]

    for axes_list, (attackName, title) in zip(axColumn, attackNames):
        axes_loss, axes_ce = axes_list
        for agg_index, (aggregation, show_name) in enumerate(aggregations):
            color = colors[agg_index]
            linestyle = linestyles[agg_index]
            file_name = 'DSGD' + '_' + attackName + '_' + aggregation \
                + '_invSqrtLR' + mark_on_title
            file_path = [task_name, graph_name, partition_name] + workspace
            record = load_file_in_cache(file_name, path_list=file_path)
            loss_path = record['loss_path']
            # loss_path = optimal_gap(loss_path, Fmin)
            consensus_error_path = record['consensus_error_path']
            
            x_axis = x_axis = [r*record['display_interval']
                            for r in range(record['rounds']+1)]
            axes_loss.plot(x_axis, loss_path, color=color, label=show_name, linestyle=linestyle)
            axes_ce.plot(x_axis, consensus_error_path, color=color, label=show_name, linestyle=linestyle)
            # ce_x_sqrt_k = [ce * k**2 for k, ce in enumerate(consensus_error_path)]
            # axes_ce.plot(x_axis[1:], ce_x_sqrt_k, LINE_STYLE, color=color, label=show_name)

        for axes in axes_list:
            # axes.xaxis.set_ticks(fontsize = FONT_SIZE)
            # axes.yaxis.set_ticks(fontsize = FONT_SIZE)
            axes.tick_params(axis='both', which='major', labelsize=FONT_SIZE)
            axes.set_yscale('log')
            # axes.legend(fontsize=FONT_SIZE)

        # loss
        axes_loss.set_title(f'loss-vs-iteration ({attackName})')
        axes_loss.set_ylabel(r'$f(x^k)$', fontsize=FONT_SIZE)
        # consensus error
        axes_ce.set_title(f'ce-vs-iteration ({attackName})')
        axes_ce.set_ylabel(r'consensus error', fontsize=FONT_SIZE)

    axColumn[-1][0].set_xlabel(r'iteration k', fontsize=FONT_SIZE)
    axColumn[-1][1].set_xlabel(r'iteration k', fontsize=FONT_SIZE)
    axColumn[-1][0].legend(loc='lower left', bbox_to_anchor=(0.2,-0.7),
            borderaxespad=0., ncol=3, fontsize=FONT_SIZE)
    fig.suptitle(pic_name)

    fig.set_size_inches((SCALE*3.5, SCALE*(1*len(attackNames)+1)))
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.35, wspace=0.38)
else:
    fig, axColumn = plt.subplots(3, len(attackNames))
    for i, (attackName, title) in enumerate(attackNames):
        axes_acc = axColumn[0][i]
        axes_loss = axColumn[1][i]
        axes_ce = axColumn[2][i]
        if attackName != 'no attack':
            axColumn[2][i].set_yticks([])
            axColumn[1][i].set_yticks([])
            axColumn[0][i].set_yticks([])
        if i != -1:
            #axColumn[-1][i].set_xticklabels([])
            axColumn[0][i].set_xticklabels([])
            axColumn[1][i].set_xticklabels([])
            #axColumn[2][i].set_xticklabels([])
        for agg_index, (aggregation, show_name) in enumerate(aggregations):
            color = colors[agg_index]
            linestyle = linestyles[agg_index]
            file_name = 'DSGD' + '_' + attackName + '_' + aggregation \
                + '_invSqrtLR' + mark_on_title
            file_path = [task_name, graph_name, partition_name] + workspace
            record = load_file_in_cache(file_name, path_list=file_path)
            acc_path = record['acc_path']
            loss_path = record['loss_path']
            # loss_path = optimal_gap(loss_path, Fmin)
            consensus_error_path = record['consensus_error_path']
            x_axis = x_axis = [r*record['display_interval']
                            for r in range(record['rounds']+1)]
            axes_loss.plot(x_axis, loss_path, color=color, label=show_name, linestyle=linestyle)
            axes_acc.plot(x_axis, acc_path, color=color, label=show_name, linestyle=linestyle)
            axes_acc.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
            axes_ce.plot(x_axis, consensus_error_path, color=color, label=show_name, linestyle=linestyle)
            axes_ce.set_ylim((1e-9,1e+4))
            # ce_x_sqrt_k = [ce * k**2 for k, ce in enumerate(consensus_error_path)]
            # axes_ce.plot(x_axis[1:], ce_x_sqrt_k, LINE_STYLE, color=color, label=show_name)

        # for axes in axes_list:
        #     # axes.xaxis.set_ticks(fontsize = FONT_SIZE)
        #     # axes.yaxis.set_ticks(fontsize = FONT_SIZE)
        #     axes.tick_params(axis='both', which='major', labelsize=FONT_SIZE)
        #     axes.set_yscale('log')
        #     # axes.legend(fontsize=FONT_SIZE)
        # axes_loss.tick_params(axis='both', which='major', labelsize=FONT_SIZE)
        axes_loss.set_yscale('log')
        # axes_acc.tick_params(axis='both', which='major', labelsize=FONT_SIZE)
        # axes_ce.tick_params(axis='both', which='major', labelsize=FONT_SIZE)
        axes_ce.set_yscale('log')

        # loss
        axes_acc.set_title(attackName, fontsize=FONT_SIZE)
        axes_ce.set_xlabel(r'iteration $k$', fontsize=FONT_SIZE)

    axColumn[0][0].set_ylabel(r'accuracy', fontsize=FONT_SIZE)
    axColumn[1][0].set_ylabel(r'loss', fontsize=FONT_SIZE)
    axColumn[2][0].set_ylabel(r'consensus error', fontsize=FONT_SIZE)
    axColumn[0][0].set_ylabel(r'accuracy', fontsize=FONT_SIZE)
    axColumn[1][0].set_ylabel(r'loss', fontsize=FONT_SIZE)
    axColumn[2][0].set_ylabel(r'consensus error', fontsize=FONT_SIZE)
    axColumn[0][1].set_yticklabels([])
    axColumn[0][2].set_yticklabels([])
    axColumn[1][1].set_yticklabels([])
    axColumn[1][2].set_yticklabels([])
    axColumn[1][3].set_yticklabels([])
    axColumn[2][1].set_yticklabels([])
    axColumn[2][2].set_yticklabels([])
    axColumn[2][3].set_yticklabels([])
    axColumn[2][0].legend(loc='lower left', bbox_to_anchor=(0.1,-0.65),
                           borderaxespad=0., ncol=3, fontsize=FONT_SIZE)
    # fig.suptitle(pic_name)

    fig.set_size_inches((SCALE*(1.4*len(attackNames)+1), SCALE*4.7))
    # fig.set_size_inches((SCALE*(1.4*len(attackNames)+1), SCALE*2.9))
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.05, wspace=0.05)

pic_path = os.path.join('pic', pic_name + '.pdf')
plt.savefig(pic_path, format='pdf', bbox_inches='tight')
plt.show()