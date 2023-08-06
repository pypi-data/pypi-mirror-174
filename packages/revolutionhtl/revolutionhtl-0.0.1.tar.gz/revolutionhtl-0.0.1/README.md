# ![REvolutionH-tl logo.](docs/images/Logo_horizontal.png)

Bioinformatics tool for the inference of event-labeled gene trees from orthology relationships, and for the reconciliation of gene trees and species trees describing the evolutionary history of large gene families. 

---

Bioinformatics team:

Tool development:

- J. Antonio R. R. [jose.ramirezra@cinvestav.mx]
- Maribel Hernandez Rosales [maribel.hr@cinvestav.mx ]

Data sets and testing:

- Dulce I. Valdivia [dulce.i.valdivia@gmail.com ]
- Katia Aviña-Padilla [katia.avinap@cinvestav.mx ]
- Gabriel Emilio Herrera [gabriel.herrera_oropeza@kcl.ac.uk]


****

# Install

pip install -i https://test.pypi.org/simple/ --upgrade revolutionhtl

## Usage

1. Determine if a directed graph is a cBMG

`python -m revolutionhtl.is_cBMG [edges table]`


