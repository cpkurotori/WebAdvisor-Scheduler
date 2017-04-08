import scraper
import pickle

# Searches fo MATH 101A, which has 7 sections in 1 page
# query_1 = {'term': '2017SP', 'subject': 'MATH', 'course_number': '101A', 'section': ''}
# calc1 = scraper.scrape_courses(**query_1)
# print(len(calc1))

# # Searches for ENGL 101A, which has 26 sections over 2 pages
query_2 = {'term': '2017SP', 'subject': 'ENGL', 'course_number': '101A', 'section': ''}
engl1 = scraper.scrape_courses(**query_2)
with open('query2.pickle', 'wb') as f:
    pickle.dump(engl1, f)
print(len(engl1))
