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

# for pr in commits_information:
#     pr['satd_commits'] = 0
#     pr['average_complexity'] = 0
#     pr['complexity'] = 0
#     pr['average_difference_complexity'] = 0
#     pr['difference_complexity'] = 0
#
# found = 0
# for pr in commits_information:
#     if commit.hash in pr['commits_list']:
#         found += 1
#         for pattern in lizardsatd.SATD_LINES:
#             if pattern in commit.msg.lower():
#                 pr['satd_commits'] += 1
#                 break
#
#         files_complexity = 0
#         difference_complexity = 0
#         modified_files_number = 0
#         files_number = 0
#         for file in commit.modified_files:
#             if not file.filename.endswith('.py'):
#                 continue
#             diff_comp = 0
#             if file.source_code:
#                 files_number += 1
#                 f = open('temp_new.py', 'w')
#                 f.write(file.source_code)
#                 analysis_result = analyze_file('temp_new.py')
#                 files_complexity += analysis_result.average_cyclomatic_complexity
#                 diff_comp = analysis_result.average_cyclomatic_complexity
#
#             if file.source_code_before and file.source_code:
#                 f = open('temp_new.py', 'w')
#                 f.write(file.source_code_before)
#                 analysis_result = analyze_file('temp_new.py')
#                 diff_comp = analysis_result.average_cyclomatic_complexity - diff_comp
#
#             if file.source_code and file.source_code_before:
#                 difference_complexity += diff_comp
#                 modified_files_number += 1
#         if files_number > 0:
#             pr['average_complexity'] += files_complexity / files_number
#         pr['complexity'] += files_complexity
#         if modified_files_number > 0:
#             pr['average_difference_complexity'] += difference_complexity / modified_files_number
#         pr['difference_complexity'] += difference_complexity
#
# for obj in data:
#     for pr in commits_information:
#         if obj['pr_number'] == pr['pr_number']:
#             obj['satd_commits'] = pr['satd_commits']
#             obj['average_complexity'] = pr['average_complexity']
#             obj['complexity'] = pr['complexity']
#             obj['average_difference_complexity'] = pr['average_difference_complexity']
#             obj['difference_complexity'] = pr['difference_complexity']
# with open("aiida_plus.json", "w") as outfile:
#     json.dump(data, outfile)
