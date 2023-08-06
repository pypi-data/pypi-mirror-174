import pandas as pd
import os
import numpy as np
import networkx as nx
from itertools import chain
from tqdm import tqdm
tqdm.pandas()
from .common_tools import norm_path

_df_matches_cols= ['Query_accession',
                  'Target_accession',
                        'Sequence_identity',
                        'Length',
                        'Mismatches',
                        'Gap_openings',
                        'Query_start',
                        'Query_end',
                        'Target_start',
                        'Target_end',
                        'E_value',
                        'Bit_score',
                       ]
_default_f= 0.9

def parse_prt_hits(path, f_value):
    prt_path= _check_files(path)
    # Load orthogroups
    df_prt= read_prt_orthogroups(prt_path)
    projectname= _get_prt_projectname(prt_path)
    # Load hits
    df= read_BHGs(path, df_prt, best_hit_dir= f'proteinortho_cache_{projectname}')
    # Select best hits
    matx_bs= df.groupby('Query_accession').Bit_score.apply(max)
    F= lambda row: row.Bit_score >= f_value*matx_bs[ row.Query_accession ]
    return df[ df.apply(F, axis= 1) ]

def parse_prt_project_bmgs(path, f_value= 0.9):
    df= parse_prt_hits(path, f_value)
    # Create graphs
    X= df.groupby('OG').apply(create_cBMG)
    return X

def get_best_hits_prt(prt_files_path,
                      best_hit_dir= '',
                      best_hit_file_ext= '.diamond',
                      Query_accession= 'Query_accession',
                      pd_params= {}):

    prt_files_path= norm_path(prt_files_path)
    best_hit_dir= norm_path(prt_files_path+best_hit_dir)

    df= pd.concat((_read_bh_table(f'{best_hit_dir}/{file}',
                                 pd_params,
                                 Query_accession= Query_accession
                                 )
                   for file in os.listdir(best_hit_dir) if file.endswith(best_hit_file_ext)
                  ))
    return df

def _read_bh_table(file, pd_params, Query_accession):
    """
    Para que funcione, el archivo debe ser llamado algo así como: 
    H0.fa.vs.H10.fa.diamond
    """
    species= file.split('/')[-1].split('.')
    species= species[0], species[3]
    df= pd.read_csv(file, **pd_params)
    columns= list(df.columns)
    df['Query_species']= species[0]
    df['Target_species']= species[1]
    return df[ ['Query_species', 'Target_species']+columns ]

def read_prt_orthogroups(orthogroups_file):
    df_prt= pd.read_csv(orthogroups_file, sep= '\t')
    species_cols= list(map(lambda x: x.split('.')[0], df_prt.columns[3:]))
    df_prt.columns= ['Species', 'Genes', 'Alg.-Conn.']+species_cols
    df_prt[species_cols]= df_prt[species_cols].apply(lambda X: X.apply(lambda x: set(x.split(','))))
    df_prt.index.name= 'OG'
    return df_prt

def _clean_prt(df_prt):
    mask= df_prt.Species > 1
    species= list(df_prt.columns[3:])
    return df_prt.loc[mask, species]

def _clean_BHs(df_prt, df_BHs):
    species= list(df_prt.columns[3:])
    F= lambda X: '*' not in X and not X.isdisjoint(df_BHs.Query_accession)
    mask= np.array([list(df_prt[X].apply(F)) for X in species])
    mask= mask.sum(axis=0) > 1
    return df_prt.loc[mask, species]

def create_cBMG(df):
    og= df.index[0]
    cBMG= nx.DiGraph()
    cBMG.og= og

    """
    add_nodes= lambda species: cBMG.add_nodes_from(df.loc[og, species].Query_accession,
                                                   species= species)
    map(add_nodes, df.columns)
    """
    genes= set(df.Query_accession).union(df.Target_accession)
    DD= {x:i for i,x in enumerate(genes)}

    aux= chain.from_iterable((df[['Query_accession', 'Query_species']].drop_duplicates().values,
                              df[['Target_accession', 'Target_species']].drop_duplicates().values
                             ))
    aux= pd.DataFrame(aux).drop_duplicates().values

    for gene,species in aux:
        cBMG.add_node(DD[gene],
                      species= species,
                      gene= gene,
                     )
       

    df.apply(lambda row: cBMG.add_node(DD[row.Target_accession],
                                       species= row.Target_species,
                                       gene= row.Target_accession,
                                      ),
             axis= 1)


    edges= df.apply(lambda row: (DD[row.Query_accession], DD[row.Target_accession], row.Bit_score),
                    axis= 1
                   )

    cBMG.add_weighted_edges_from( edges )

    return cBMG

def read_BHGs(hits_path,
              df_prt,
              best_hit_dir= '',
              pd_params= dict(names= _df_matches_cols, sep= '\t'),
             ):
    # Loads best hits (diamond or blast output for pairs of species)
    df_BHs= get_best_hits_prt(hits_path,
                              best_hit_dir= best_hit_dir,
                              pd_params= pd_params,
                             )

    """
    # Loads proteiortho table containng orthogroups
    df_prt= _clean_BHs(read_prt_orthogroups(prt_path),
                   df_BHs)
    """
    df_prt= _clean_BHs(df_prt, df_BHs)

    # For each ortogroup obtain the best matches of all the genes in such orthogroup
    F= lambda x: _get_best_macthes(x, df_BHs)
    print('Grouping best matches...')
    df_best_matches= pd.concat( df_prt.progress_apply(F, axis= 1).values )

    return df_best_matches

def _get_prt_projectname(prt_file):
    return prt_file.split('/')[-1].split('.')[0]

def read_symBets(prt_graph_path, prt_path):
    # Loads symBets (proteinortho-graph)
    symBets= pd.read_csv(prt_graph_path, sep='\t', comment= '#', names= ['a',
                                                                         'b',
                                                                         'evalue_ab',
                                                                         'bitscore_ab',
                                                                         'evalue_ba',
                                                                         'bitscore_ba',
                                                                        ])

    # Loads proteiortho table containng orthogroups
    df_prt= _clean_prt( read_prt_orthogroups(prt_path) )

    # For each ortogroup obtain the orthology relations of all the genes in such orthogroup
    F= lambda x: _get_orthos(x, symBets)
    df_edges= pd.concat( list(df_prt.apply(F, axis= 1)) )

    return df_edges


def _search_matches(row, species, df_BHs):
    return pd.concat((df_BHs[df_BHs.Query_accession==x]
                      for x in row[species]))

def _get_best_macthes(row, df_BHs):
    #best_matches= pd.concat((search_matches(row, S0), search_matches(row, S1)))
    best_matches= pd.concat((_search_matches(row, X, df_BHs) for X in row.index))
    best_matches['OG']= row.name
    #best_matches.index.name= 'Query_species'
    return best_matches.set_index('OG').sort_index()

def _get_orthos(row, symBets):
    orths= pd.concat((_search_orths(row, X, symBets) for X in row.index))
    orths['OG']= row.name
    return orths.set_index('OG').sort_index()

def _search_orths(row, species, symBets):
    mask= lambda x: symBets[ (symBets.a==x) | (symBets.b==x) ]
    return pd.concat(map(mask, row[species]))

def _check_files(path):
    prt_path= [x for x in os.listdir(path) if x.endswith('.proteinortho.tsv')]
    if len(prt_path)==1:
        prt_path= path + prt_path[0]
    else:
        raise ValueError(f'There is more than one ".proteinortho.tsv" file at {path}')
    return prt_path


####################
#                  #
# Standalone usage #
#                  #
####################


def _parse(path, f_value, opath):
    df= parse_prt_hits(path, f_value)
    df.reset_index().to_csv(opath, sep='\t', index= False)
    print(f'Parsed file successfully writen to {opath}')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog= 'parse_prt',
                                     description='Converts proteinortho outputs to edges list of best hits.',
                                    )
    # Parameters for input graph
    ############################

    parser.add_argument('prt_path',
                        type= str,
                        help= 'Path to a directory containing proteinortho files. For more information see:'
                       )

    parser.add_argument('-o', '--output_prefix',
                        type= str,
                        required=False,
                        help= 'prefix used for output files (default "prt_revolutionhtl").',
                        default= 'prt_revolutionhtl',
                       )

    parser.add_argument('-f', '--f_value',
                        type= float,
                        required=False,
                        help= f'Number between 0 and 1 (default {_default_f}), defines the adaptative threshhold for best matches: f*max_bit_score. (see proteinortho paper for a deep explanation)',
                        default= _default_f,
                       )

    args= parser.parse_args()

    # Process data
    ##############
    args.prt_path= norm_path(args.prt_path)
    opath= args.prt_path+args.output_prefix+'.best_hits.tsv'
    _parse(args.prt_path, args.f_value, opath)


