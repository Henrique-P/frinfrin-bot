import git

def getHeadCommit():
    repo = git.Repo('./')
    head_commit = repo.head.commit
    return f"Head commit: {head_commit.hexsha}\nAuthor: {head_commit.author.name} <{head_commit.author.email}>\nDate: {head_commit.authored_datetime}\nMessage: {head_commit.message}"
