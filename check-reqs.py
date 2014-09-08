import os
import sys
from itertools import chain
from pip.req import parse_requirements


def get_req_files(path):
    if path.endswith('.txt'):
        return [path]
    return [os.path.join(path, fn) for fn in os.listdir(req_path)]


def get_reqs(req_files):
    return list(chain(*(parse_requirements(path)
                        for path in req_files)))


def main():
    req_path = os.environ.get('REQ_PATH')
    if not req_path:
        raise Exception('REQ_PATH not defined!')

    req_files = get_req_files(req_path)
    reqs = get_reqs(req_files)

    unsatisfied_reqs = []
    unsatisfyable_reqs = []
    for req in reqs:
        if req.url and 'github.com' in req.url:
            print url
            unsatisfyable_reqs.append(req)
            continue
        req.check_if_exists()
        if not req.satisfied_by:
            unsatisfied_reqs.append(req)
    if unsatisfyable_reqs:
        print 'There are %d requirements that cannot be checked.' % (
                len(unsatisfyable_reqs))
    if unsatisfied_reqs:
        print 'The following requirements are not satsifed:'
        print ''
        for req in unsatisfied_reqs:
            print 'UNSATISFIED:', req.req
            print ''
            print 'Update your virtual environment by doing:'
            print ''
            print ' ./peep install -r requirements/requirements.txt'
            print ''
            print 'or run with SKIP_CHECK=1 .'
            sys.exit(1)


if __name__ == '__main__':
    main()
