from run_handler import *
import requests
import json

def get_pr(token,repo):
    print('Getting PR number...')
    url = (f'https://api.github.com/repos/Pay-Baymax/{repo}/pulls')
    headers = {'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    pr = requests.get(url,headers=headers)
    return pr.text

def get_issues(token,repo,page):
    url = (f'https://api.github.com/repos/Pay-Baymax/{repo}/issues?state=all&per_page=100&page={page}&labels=security-issue')
    headers = {'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    issues = requests.get(url,headers=headers)
    return issues

def create_issues(token,repo,title,body):
    url = (f'https://api.github.com/repos/Pay-Baymax/{repo}/issues')
    headers = {'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    body =  {"title":title,"body":body,"labels":["security-issue"]}
    issue = requests.post(url,json=body,headers=headers)
    return issue

def create_review(token,repo,pull,message):
    url = (f'https://api.github.com/repos/Pay-Baymax/{repo}/pulls/{pull}/reviews')
    headers = {'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    body =  {"body":f"{message}","event":"COMMENT"}
    review = requests.post(url,json=body,headers=headers)

def get_github_data(repo_owner, repo_name, label, token):
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    params = {
        'state': 'open',
        'labels': label,
    }
    headers = {
        'Authorization': f'Token {token}'
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        issues = response.json()
        return issues
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def format_issue_data(issue):
    issue_url = issue['html_url']
    issue_title = issue['title']
    issue_comments = get_issue_comments(issue['comments_url'])
    created_at = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

    return [issue_url, issue_title, issue_comments, created_at]

def get_issue_comments(comments_url):
    response = requests.get(comments_url)

    if response.status_code == 200:
        comments = response.json()
        return '\n'.join([comment['body'] for comment in comments])
    else:
        return ''

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Issue URL', 'Title', 'Comments', 'Created At'])

        for row in data:
            csv_writer.writerow(row)

def job():

    repo_owner = 'anguhari77'
    repo_name = 'Python_Semgrep_test'
    label = 'fp'
    token = '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'
    output_csv_filename = 'github_open_issues.csv'
    issues = get_github_data(repo_owner, repo_name, label, token)

    if issues:

        formatted_data = [format_issue_data(issue) for issue in issues]
        save_to_csv(formatted_data, output_csv_filename)
        print(f"Data saved to {output_csv_filename}")

