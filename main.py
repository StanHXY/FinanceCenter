import warnings
warnings.filterwarnings("ignore")

# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler

from findy import findy_config
from findy.interface import Region
from findy.interface.fetch import fetching

# sched = BackgroundScheduler()


def arg_parsing():
    import argparse

    # parse cli args
    parser = argparse.ArgumentParser()

    parser.add_argument("-debug",
                        action='store_true',
                        help="Debug message output")

    parser.add_argument("-fetch",
                        choices=[e.value for e in Region],
                        help=f"fetch stock market data. support: {[e.value for e in Region]}")

    parser.add_argument("-v", action="version",
                        version="Financial-Dynamics v%s" % findy_config['version'],
                        help="prints version and exits")

    return parser.parse_args()


# @sched.scheduled_job('interval', days=1)
def fetch(args):
    if args.fetch is not None:
        fetching(Region(args.fetch))


if __name__ == '__main__':
    args = arg_parsing()
    print(args)

    findy_config['debug'] = args.debug

    fetch(args)

    # print("scheduling in processing...")
    # print("next triggering time will be at: {}".format(next_date(datetime.now(), days=1)))
    # print("good day...")
    # print("")
    # sched.start()
    # sched._thread.join()
