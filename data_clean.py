import json

f = open('pulls.json')

data = json.load(f)


for obj in data:
    reviewers = obj['requested_reviewers']
    reviewers_list_name = []
    for reviewer in reviewers:
        tmp = reviewer['login']
        reviewers_list_name.append(tmp)
    obj['requested_reviewers'] = reviewers_list_name
    comment_list = obj['review_comments']
    for comment in comment_list:
        if comment['user'] in obj['requested_reviewers']:
            comment['user'] = 'reviewer'
        else:
            comment['user'] = 'not a reviewer'
    comment_list = obj['comments']
    for comment in comment_list:
        if comment['user'] in obj['requested_reviewers']:
            comment['user'] = 'reviewer'
        else:
            comment['user'] = 'not a reviewer'


with open("cleaned_data_reviewers.json", "w") as outfile:
    json.dump(data, outfile)

