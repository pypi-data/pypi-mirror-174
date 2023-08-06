import copy

log_dict = {}
hyperparam_dict = {}


def login():
    print("login success")
    return True


def init(project, config=None):
    print(project)
    global hyperparam_dict
    if config is not None:
        hyperparam_dict = config.copy()


def log(data_dict):
    # for key in data_dict:
    #    log_dict[key] = data_dict[key]
    #    print(data_dict[key])
    global log_dict
    for key in data_dict:
        if key in log_dict:
            log_dict[key] = log_dict[key] + [round(data_dict[key], 1)]
        else:
            log_dict[key] = [data_dict[key]]


def result():
    print("show result...")
    print("\t hyper param")
    for key in hyperparam_dict:
        print("\t\t", key, hyperparam_dict[key])
    print("\t train log")
    for key in log_dict:
        print("\t\t", key, log_dict[key])
    print("\t cost")
    print("\t\t{:<10} {:<10} {:<10} {:<10}".format('time', 'gpu type', 'gpu count', 'cost'))
    print("\t\t{:<10} {:<10} {:<10} {:<10}".format('1.2 hour', 'T4', '2', '0.24 USD'))
    print("\t dashboad link")
    print("\t\t", "https://deepdriver.bokchi.com/my-bokchi-project/0")

    return True


def finish():
    print("finish logging...")
    return True

