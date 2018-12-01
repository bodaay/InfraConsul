import os


class cluster:
    def __init__(self):
        self.ClusterName = None
        self.OrganizationDomainName = None

    def SelfCheck(self):
        if self.ClusterName is None or self.ClusterName == "":
            return False, "Cluster Name is Empty or not set"
        if self.OrganizationDomainName is None:
            return False, "Organization Domain Name is Empty or not set"
        return True

    def InitNewCluster(self):
        if os.path.exists(self.OrganizationDomainName):
            return False, "Cluster Working Folder \"%s\" Already Exists" % self.OrganizationDomainName
        return True
