import astropy.table as table
# from ads import SearchQuery
import ads

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
    ],
    max_pages=10000,  # retrieve all papers
    sort="pubdate",
)
papers2 = list(query2)
print()
my_name = ['Pace, A. B.', 'Pace, Andrew B.', 'Pace, Andrew', 'Pace, A.', 'Pace, Andrew B']
pub_info = table.Table.read('pub_list_info_Sheet1.csv')

major_contribution_pub = pub_info[pub_info['major_contributions']==1]
student_lead = pub_info[pub_info['student_lead']==1]
print("major contributions, student led:", len(major_contribution_pub), len(student_lead))
print("total", len(pub_info))

arXiv = []
published = []
major_contributions = []
nth_contributions = []
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
    if str(papers2[i].pub) == "arXiv e-prints":
        arXiv.append(final_str)
    else:
        published.append(final_str)
        if papers2[i].bibcode in major_contribution_pub['bibcode']:
            major_contributions.append(final_str)
        else:
            nth_contributions.append(final_str)

with open('latex/major_contributions.tex', 'w') as file:
    file.writelines(major_contributions)

with open('latex/nth_contributions.tex', 'w') as file:
    file.writelines(nth_contributions)

with open('latex/arxiv_input.tex', 'w') as file:
    file.writelines(arXiv)

print("arXiv, published, major, nth:", len(arXiv), len(published), len(major_contributions), len(nth_contributions))

# with open('latex/published.tex', 'w') as file:
#     file.writelines(published)
