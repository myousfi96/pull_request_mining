import json
import lizardsatd
import lizard
import aiohttp
import asyncio


analyze_file = lizard.FileAnalyzer(lizard.get_extensions([lizardsatd.LizardExtension()]))


async def main():
    f = open('aiida.json')
    data = json.load(f)
    f.close()
    f = open('aiida_commits.json')
    commits_information = json.load(f)
    f.close()

    token = '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'
    owner = "aiidateam"
    repo = "aiida-core"
    headers = {'Authorization': f'token {token}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        for pr in commits_information:
            files = []
            pr['satd_commits'] = 0
            pr['average_complexity'] = 0
            pr['complexity'] = 0
            for commit in pr['commits_list']:
                query_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit}"
                async with session.get(query_url) as r:
                    commits_data = await r.json()
                if commits_data['files']:
                    for file in commits_data['files']:
                        if file['filename'].endswith('.py'):
                            files.append(file['raw_url'])
            files_complexity = 0
            for file in files:
                async with session.get(file) as r:
                    source_code = await r.text()
                    f = open('temp_new.py', 'w')
                    f.write(source_code)
                    analysis_result = analyze_file('temp_new.py')
                    files_complexity += analysis_result.average_cyclomatic_complexity
            pr['complexity'] = files_complexity
            if len(files) > 0:
                pr['average_complexity'] = files_complexity / len(files)
            for pattern in lizardsatd.SATD_LINES:
                if pattern in pr['message_list']:
                    pr['satd_commits'] += 1
                    break
            for obj in data:
                if obj['pr_number'] == pr['pr_number']:
                    obj['satd_commits'] = pr['satd_commits']
                    obj['average_complexity'] = pr['average_complexity']
                    obj['complexity'] = pr['complexity']
                    with open("aiida_plus.json", "a") as outfile:
                        json.dump(obj, outfile)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
