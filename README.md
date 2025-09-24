# abp_publication_list

This package semi-automates the creation of my publication list: with a NASA/ADS libraty (for example [my ads library](https://ui.adsabs.harvard.edu/public-libraries/hJ77Di5nQ0qwHYNpG0yRpA)), the [ads](https://github.com/andycasey/ads) python package, and a csv file containing the following columbs: bibcode (ads bibcode), major_contributions (0/1; sorts publications into two groups), student_lead (0/1; underlines student lead work).

The script will run the python code (which makes the latex input) and run the latex to create a publication list.

If others want to use this they will need to update to their own ADS library, change the name and some text, and create the input csv file.  Some special characters might need to be dealt with.

