from provider.synchronizer.synchronize import Synchronize


def synchronize_github(user):
    g = Synchronize(user)
    g.run()
