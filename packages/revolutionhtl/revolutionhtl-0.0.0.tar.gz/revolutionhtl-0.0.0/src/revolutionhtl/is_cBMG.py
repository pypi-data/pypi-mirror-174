from cBMG_tools import LRT_from_cBMG
from common_tools import norm_path


####################
#                  #
# Standalone usage #
#                  #
####################

if __name__ == "__main__":

    import argparse
    import os
    from parse_prt import parse_prt_project_bmgs

    parser = argparse.ArgumentParser(prog= 'is_cBMG',
                                     description='Determines if a directed graph is a coloured Best Match Graph (cBMG).',
                                    )
    # Parameters for input graph
    ############################

    parser.add_argument('edges_list',
                        type= str,
                        #required=False,
                        help= '.tsv file containing directed edges.'
                       )

    parser.add_argument('-F', '--edges_format',
                        type= str,
                        required=False,
                        help= 'Path to a directory containing proteinortho files. For more information see:',
                        default= 'prt',
                       )

    args= parser.parse_args()

    # Input data
    #############

    if args.edges_format=='prt':
        args.edges_list= norm_path(args.edges_list)
        G= parse_prt_project_bmgs(args.edges_list, f_value= 0.9)
    else:
        raise ValueError(f'Edges format "{args.edges_format}" not valid.')

    # Analyze
    #########
    T0= [LRT_from_cBMG(X, 'species', 'gene') for X in G]

