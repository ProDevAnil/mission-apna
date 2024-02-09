
!pip install PyGithub

from github import Github
import time

# GitHub credentials
github_username = "your user name"
github_token = "your github token"  # Generate a token from GitHub Developer Settings

# Repository details
repo_url = "https://github.com/expressjs/express"
username = "expressjs"
pr_content = "#apana collage"

# Initialize PyGithub
g = Github(github_token)

# Get the repository
repo = g.get_repo(repo_url.split("/")[-2] + "/" + repo_url.split("/")[-1])

# Function to create pull request
def create_pull_request(repo, branch, title, body):
    try:
        return repo.create_pull(title=title, body=body, base="master", head=branch)
    except Exception as e:
        print(f"Error creating pull request: {e}")
        return None

# Main loop
while True:
    # Get the README file
    readme = repo.get_readme()
    
    # Get current content of README
    current_content = readme.decoded_content.decode()
    
    # Replace the content of README with the specified message
    new_content = pr_content
    
    # Commit the changes
    branch = f"update-readme-{int(time.time())}"
    repo.create_git_ref(ref=f"refs/heads/{branch}", sha=repo.get_branch("master").commit.sha)
    repo.update_file(readme.path, f"Updated README.md - {time.strftime('%Y-%m-%d %H:%M:%S')}", new_content, readme.sha, branch=branch)
    
    # Create pull request
    title = f"Update README with '{pr_content}'"
    body = f"This PR updates the README file with the content '{pr_content}'."
    pr = create_pull_request(repo, branch, title, body)
    
    if pr:
        print(f"Pull request created: {pr.html_url}")
    else:
        print("Failed to create pull request")

    # Wait for some time before creating the next PR
    time.sleep(3600)  # Adjust the time interval as needed (in seconds)
