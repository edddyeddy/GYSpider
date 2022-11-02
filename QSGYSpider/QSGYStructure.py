def createFunding():
    funding = {
        "targetMoney": None,
        "receivedMoney": None,
        "backerCount": None,
        "shareCnt": None,
    }
    return funding


def createOrganization():
    organization = {
        "executionOrg": None,
        "publishOrg": {
            "name": None,
            "socialCreditNo": None
        },
        "publisher": None,
        "receiver": None,
    }
    return organization


def createDescription():
    description = {
        "title": None,
        "rowDesc": None,
        "feedBackCount": None,
        "cate": None,
    }
    return description
