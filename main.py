import requests
from pprint import pprint
import json
import aiohttp
import asyncio


async def main():
    token = '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'
    owner = "ansible"
    repo = "ansible"
    query_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    for i in range(1):
        complete_data = []
        params = {
            "per_page": 1,
            "page": 100,
            'state': 'closed'
        }
        headers = {'Authorization': f'token {token}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(query_url, params=params) as r:
                data = await r.json()
                print(data)
                for j in range(len(data)):
                    pr = data[j]
                    pull_request_json = {'merged_at': pr['merged_at'], 'author_followers': pr['user']['followers_url'],
                                         'author_site_admin':
                                             pr['user']['site_admin'],
                                         'updated_at': pr['updated_at'], 'created_at': pr['created_at'],
                                         'requested_reviewers': pr['requested_reviewers'],
                                         'repo_size': pr['base']['repo']['size'],
                                         'repo_open_issues_count': pr['base']['repo']['open_issues_count'],
                                         'repo_watchers': pr['base']['repo']['watchers'],
                                         'author_association': pr['author_association']}
                    if 'merged' in pr:
                        pull_request_json['merged'] = pr['merged']
                    if 'commits' in pr:
                        pull_request_json['commits'] = pr['commits']
                    if 'additions' in pr:
                        pull_request_json['additions'] = pr['additions']
                    if 'deletions' in pr:
                        pull_request_json['deletions'] = pr['deletions']
                    if 'changed_files' in pr:
                        pull_request_json['changed_files'] = pr['changed_files']
                    if 'body' in pr and pr['body']:
                        pull_request_json['body_length'] = len(pr['body'])

                    followers_url = pull_request_json['author_followers']
                    pull_request_json['author_followers'] = 0

                    for index in range(10):
                        params = {
                            "per_page": 100,
                            "page": index
                        }
                        async with aiohttp.ClientSession(headers=headers) as session:
                            async with session.get(followers_url, params=params) as followers:
                                followers_count = len(await followers.json())
                                pull_request_json['author_followers'] += followers_count
                        if followers_count < 100:
                            break

                    review_comments_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{data[j]['number']}/comments"
                    headers = {'Authorization': f'token {token}'}
                    params = {
                        "per_page": 100,
                        "page": 1
                    }
                    pull_request_json['review_comments'] = []
                    pull_request_json['comments'] = []
                    async with aiohttp.ClientSession(headers=headers) as session:
                        async with session.get(review_comments_url, params=params) as review_comments:
                            review_comments_data = await review_comments.json()
                            for k in range(len(review_comments_data)):
                                if review_comments_data:
                                    rv = review_comments_data[k]
                                    review_comment_json = {'body': rv['body'], 'diff_hunk': rv['diff_hunk'], 'user': rv['user']['login'],
                                                           'path': rv['path']}
                                    pull_request_json['review_comments'].append(review_comment_json)

                    pull_request_json['review_comments_count'] = len(review_comments_data)
                    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{data[j]['number']}/comments"
                    headers = {'Authorization': f'token {token}'}
                    params = {
                        "per_page": 100,
                        "page": 1
                    }
                    async with aiohttp.ClientSession(headers=headers) as session:
                        async with session.get(comments_url, params=params) as comments:
                            comments_data = await comments.json()
                    for k in range(len(comments_data)):
                        comment = comments_data[k]
                        comment_json = {'body': comment['body'], 'user': comment['user']['login']}
                        pull_request_json['comments'].append(comment_json)
                    pull_request_json['comments_count'] = len(comments_data)
                    complete_data.append(pull_request_json)
        print(i)
        with open("pulls.json", "a") as outfile:
            json.dump(complete_data, outfile)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
