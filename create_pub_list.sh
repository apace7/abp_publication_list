#!/bin/zsh

source ~/.zshrc

python create_latex_files.py

# print 'creating latex tables'

# python scripts/create_latex_table.py

# python scripts/unit_tests.py

# read -s -k '?Press any key to create summary plots.'

# python scripts/create_summary_plots.py

read -s -k '?Press any key to compile latex and create pdf.'

cd latex/

latex publication_list.tex
# bibtex main
# latex main.tex
# latex main.tex
pdflatex publication_list.tex