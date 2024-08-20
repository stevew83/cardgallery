project description:
I intend to use a website to store and display some cards. It will be deployed on streamlit.io
Cards are grouped in to 9 card groups and displayed in 3x3 grids.
For example, my first group is vintage hockey. My second is late 19th early 20th
century Non Sports. But card categories can have any number of cards. If a category has 50
cards, there are 6 pages: 5 full ones (45), and a 6th with 5 cards for a total of 50.

I may try to create a dropdown that would allow you to move between different csv files.
I may try to make PSA and other graded cards contain relevant information.  
Right now, card grades are estimated and of course, there is no way of knowing a raw
card's actual grade.

for deployment on streamlit, ensure paths are absolute. For example:
/cardgallery/sportscards.csv
/trading_card_gallery.py
