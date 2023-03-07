import json

f = open('pulls.json')

data = json.load(f)


for obj in data:
    comment_list = obj['review_comments']
    for comment in comment_list:
        comment.pop('diff_hunk', None)

with open("cleaned_data.json", "w") as outfile:
    json.dump(data, outfile)

