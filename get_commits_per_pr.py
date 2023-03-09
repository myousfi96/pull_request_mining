import json
import aiohttp
import asyncio
import lizardsatd
import lizard
from pydriller import Repository

analyze_file = lizard.FileAnalyzer(lizard.get_extensions([lizardsatd.LizardExtension()]))
commits_information = []


async def main():
    f = open('mat.json')
    data = json.load(f)
    f.close()
    token = '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'
    owner = "matplotlib"
    repo = "matplotlib"
    headers = {'Authorization': f'token {token}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        for obj in data:
            pr_number = obj['pr_number']
            query_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/commits"
            async with session.get(query_url) as r:
                try:
                    commits_data = await r.json()
                except:
                    pass
                commits_list = [commit['sha'] for commit in commits_data]
                message_list = [commit['commit']['message'] for commit in commits_data]

                tmp = {'pr_number': pr_number, 'commits_list': commits_list, 'message_list': message_list}
                commits_information.append(tmp)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

with open("mat_commits.json", "w") as outfile:
    json.dump(commits_information, outfile)
