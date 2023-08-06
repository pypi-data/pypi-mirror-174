import os
import git


class GitRepo:

    def __init__(self, name, url, remote_conn_name='origin'):
        self.name = name
        self.url = url
        self.remote_conn_name = remote_conn_name
        self.repo = None

    def init(self, repo_local_dir, auto_clone=True):
        # if already have directory
        if os.path.exists(repo_local_dir):
            repo = git.Repo(repo_local_dir)
        elif auto_clone:
            repo = git.Repo.clone_from(url=self.url, to_path=repo_local_dir)
        else:
            raise RuntimeError("local directory {} not found for repo {}".format(repo_local_dir, self.name))
        self.repo = repo

    def get_last_commit(self):
        if not self.repo:
            raise RuntimeError("repo {} haven't been initialized".format(self.name))
        commits = list(self.repo.iter_commits())
        if len(commits) > 0:
            last_commit = commits[0]
            return {"datetime": last_commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "committer": last_commit.committer,
                    "message": last_commit.message,
                    "hexsha": last_commit.hexsha}

    def get_remote_branch(self, branch_name):
        # get remote connection, raise IndexError: No item found with id '...' if failed
        remote = self.repo.remotes[self.remote_conn_name]
        found_refs = list(filter(lambda x: x.name == '{}/{}'.format(self.remote_conn_name, branch_name), remote.refs))
        if len(found_refs) > 0:
            return found_refs[0]

    def create_remote_branch(self, new_branch_name, base_branch_name):
        remote = self.repo.remotes[self.remote_conn_name]
        # create local branch from remote base branch
        head = self.repo.create_head(new_branch_name, base_branch_name)
        return remote.push(head)

    def checkout_remote_branch(self, branch_name):
        remote = self.repo.remotes[self.remote_conn_name]
        ref = self.get_remote_branch(branch_name)
        if not ref:
            raise RuntimeError("remote branch {} not found".format(branch_name))
        self.repo.create_head(branch_name, ref).set_tracking_branch(ref).checkout()
        remote.pull()
