from .cBMG_tools import LRT_from_cBMG
from .common_tools import norm_path
import pandas as pd

####################
#                  #
# Standalone usage #
#                  #
####################

if __name__ == "__main__":

    import argparse
    import os
    from .parse_prt import parse_prt_project_bmgs, create_cBMG

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
                        help= 'Format of the edges list (default "prt"). For more information see:...',
                        choices= ['prt', 'tl'], # 'prt_pre_parse'
                        default= 'prt',
                       )

    parser.add_argument('-o', '--output_prefix',
                        type= str,
                        required=False,
                        help= 'prefix used for output files (default "tl_iscBMG").',
                        default= 'tl_iscBMG',
                       )

    args= parser.parse_args()

    # Input data
    #############

    if args.edges_format=='prt':
        args.edges_list= norm_path(args.edges_list)
        #> Añadir opción para guardar o no tabla parseada
        G= parse_prt_project_bmgs(args.edges_list, f_value= 0.9)
    elif args.edges_format=='tl':
        df= pd.read_csv(args.edges_list, sep= '\t').set_index('OG')
        G= df.groupby('OG').apply(create_cBMG)
    else:
        #> Leer tabla de aristas parseada
        raise ValueError(f'Edges format "{args.edges_format}" not valid.')

    # Analyze
    #########
    #> Ver todos los posibles 'no es cBMG', y en lugar de retornar error, retornar texto
    def take_result(X):
        try:
            Y= LRT_from_cBMG(X, 'species', 'gene')
        except Exception as ex:
            Y= 'NO'
        return Y

    T0= [take_result(X) for X in G]
    df= pd.DataFrame(dict(OG= list(G.index),
                          is_cBMG= T0
                         ))
    opath= args.output_prefix + '.csv'
    df.to_csv(opath, sep='\t', index= False)

