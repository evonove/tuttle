from provider.synchronizer.synchronize import GithubSyn


def synchronize_github(user):
    g = GithubSyn(user)
    g.run()
