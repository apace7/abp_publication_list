import astropy.table as table
# from ads import SearchQuery
import ads

import numpy as np

from pylatexenc.latexencode import unicode_to_latex

query_str_2 = (
    'docs(library/hJ77Di5nQ0qwHYNpG0yRpA)'
)
query2 = ads.SearchQuery(
    q=query_str_2,
    fl=[
        "id",
        "bibcode",
        "author",
        "title",
        "volume",
        "issue",
        "page",
        "page_range",
        "pub",
        "pubdate",
        "year",
        "citation_count"
    ],
    max_pages=10000,  # retrieve all papers
    sort="pubdate",
)
papers2 = list(query2)
print()
my_name = ['Pace, A. B.', 'Pace, Andrew B.', 'Pace, Andrew', 'Pace, A.', 'Pace, Andrew B']
pub_info = table.Table.read('pub_list_info_Sheet1.csv')

first_author_info = pub_info[pub_info['first_author']==1]
major_contribution_pub = pub_info[pub_info['major_contributions']==1]
student_lead = pub_info[pub_info['student_lead']==1]
print("major contributions, student led:", len(major_contribution_pub), len(student_lead))
print("total", len(pub_info))

arXiv = []
published = []
major_contributions = []
nth_contributions = []
first_author = []
for i in range(len(papers2)):
    if papers2[i].bibcode == "2016PhDT.......110P":
        continue
#     print(papers2[i].author)
    author_list = ""
    abp_in = False
    for kk in range(len(papers2[i].author)):
        if kk>3:
            author_list +="et al. "
            if abp_in==False:
                author_list += "including {\\bf Andrew B. Pace} "
            break
        a = papers2[i].author[kk]
#         a = a.replace("U+00E7", "")
        a = unicode_to_latex(a)
        if a in my_name:
            a = "{\\bf "+a +"}"
            abp_in= True
        if kk==0 and papers2[i].bibcode in student_lead['bibcode']:
            a = "\\underline{"+ a + "}"
        if kk<=3:
            author_list += str(a) +", "
        
    volume = papers2[i].volume
    if volume == None:
        volume = ""
    x = "; \\href{https://ui.adsabs.harvard.edu/abs/"
    x2 = "/abstract}{ADS link}"
    xf = x + str(papers2[i].bibcode) + x2
    
    title = str(papers2[i].title[0])
    title = title.replace("{\Lambda}", "Λ")
    title =title.replace("<SUP>", "")
    title = title.replace("</SUP>", "")
    title = unicode_to_latex(title)
#     print(title)
    
    
#     title = title.replace("\alpha", "$\\alpha$")
    title = "{\\it "+title +"}"
    
#     a = unicode_to_latex(a)
#     print(title)
    final_str = "\\item " + author_list+str(papers2[i].year)+", "+str(papers2[i].pub)+", "+volume+ ", "+str(papers2[i].page[0])+", "+title + xf
    if papers2[i].citation_count > 100 or papers2[i].bibcode in first_author_info['bibcode']:
        temp = " ({\\bf "+ str(papers2[i].citation_count) + " citations} on NASA ADS)"
        final_str += temp
    if papers2[i].bibcode in first_author_info['bibcode']:
        first_author.append(final_str)
    elif str(papers2[i].pub) == "arXiv e-prints":
        arXiv.append(final_str)
    else:
        published.append(final_str)
        if papers2[i].bibcode in major_contribution_pub['bibcode']:
            major_contributions.append(final_str)
        else:
            nth_contributions.append(final_str)

cit = []
for i in range(len(papers2)):
    cit.append(papers2[i].citation_count)

def compute_h_index(citations):
    ## from google
    citations.sort(reverse=True)
    h_index = 0
    for i, citation_count in enumerate(citations):
        if citation_count >= (i + 1):
            h_index = i + 1
        else:
            break
    return h_index

h_index = compute_h_index(cit)
total_citations = np.sum(cit)
total_papers = len(papers2)

extra_stat = str(len(published)) + " total publications; " + str(len(first_author)) + " first author publications; " + str(len(major_contributions)) + " student led and/or major contribution publications; " + str(len(nth_contributions)) + " nth author or builder publications; " + str(len(arXiv)) + " submitted or white papers; h-index $=$ "  + str(h_index)

with open('latex/extra_stat.tex', 'w') as file:
    file.writelines(extra_stat)

with open('latex/first_author.tex', 'w') as file:
    file.writelines(first_author)
with open('latex/major_contributions.tex', 'w') as file:
    file.writelines(major_contributions)

with open('latex/nth_contributions.tex', 'w') as file:
    file.writelines(nth_contributions)

with open('latex/arxiv_input.tex', 'w') as file:
    file.writelines(arXiv)

print("arXiv, published, major, nth, 1st author:", len(arXiv), len(published), len(major_contributions), len(nth_contributions), len(first_author))

# with open('latex/published.tex', 'w') as file:
#     file.writelines(published)
