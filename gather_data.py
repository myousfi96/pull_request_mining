import json
import aiohttp
import asyncio


async def main():
    token = ''  # put Your own token here
    owner = "scikit-learn"
    repo = "scikit-learn"
    query_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    for i in range(0, 10):
        complete_data = []
        params = {
            "per_page": 100,
            "page": i,
            'state': 'closed',
            'sort': 'popularity',
            'direction': 'dec'
        }
        headers = {'Authorization': f'token {token}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(query_url, params=params) as r:
                data = await r.json()
                for j in range(len(data)):
                    pr = data[j]
                    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr['number']}"
                    async with session.get(pr_url) as d:
                        pr = await d.json()
                        pull_request_json = {'author_followers': pr['user']['followers_url'],
                                             'updated_at': pr['updated_at'], 'created_at': pr['created_at'],
                                             'requested_reviewers': len(pr['requested_reviewers']),
                                             'repo_size': pr['base']['repo']['size'],
                                             'repo_open_issues_count': pr['base']['repo']['open_issues_count'],
                                             'repo_watchers': pr['base']['repo']['watchers'],
                                             'author_association': pr['author_association'],
                                             'comments_count': pr['comments'],
                                             'review_comments_count': pr['review_comments'],
                                             'pr_number': pr['number'], 'mergeable_state': pr['mergeable_state']
                                             }
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
                            async with session.get(followers_url, params=params) as followers:
                                followers_count = len(await followers.json())
                                pull_request_json['author_followers'] += followers_count
                            if followers_count < 100:
                                break

                        complete_data.append(pull_request_json)

        with open("data/gym.json", "a") as outfile:
            json.dump(complete_data, outfile)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
