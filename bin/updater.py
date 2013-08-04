#!/usr/bin/env python

"""

ownCloud - News

@author Bernhard Posselt
@copyright 2012 Bernhard Posselt nukeawhale@gmail.com

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
License as published by the Free Software Foundation; either
version 3 of the License, or any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU AFFERO GENERAL PUBLIC LICENSE for more details.

You should have received a copy of the GNU Affero General Public
License along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""

# This script uses python 3
from sys import exit
from time import sleep
from argparse import ArgumentParser
from urllib.request import HTTPPasswordMgrWithDefaultRealm, \
    HTTPBasicAuthHandler, build_opener, install_opener, urlopen
from urllib.error import HTTPError


class Updater:

    def __init__(self, base_url, user, password, threads):

        self.threads = threads
        self.user = user
        self.password = password
        self.base_url = base_url

        if self.base_url[-1] != '/':
            self.base_url += '/'
        self.base_url += 'index.php/apps/news/api/v1-2'

        self.cleanup_url = '%s/cleanup' % self.base_url
        self.all_feeds_url = '%s/feeds/all' % self.base_url
        self.update_url = '%s/feeds/update' % self.base_url


    def run(self):
        try:
            auth = HTTPPasswordMgrWithDefaultRealm()
            auth.add_password(None, self.base_url, self.user, self.password)
            opener = build_opener( HTTPBasicAuthHandler(auth) )
            install_opener(opener)

            urlopen(self.cleanup_url)
            feeds = urlopen(self.all_feeds_url).read()

            # TODO: parse feeds and thread the requests


        # TODO: also check for the other URLErrors
        except (ValueError, HTTPError):
            print('%s is either not valid or does not exist' % self.base_url)
            exit(1)


class Daemon:

    def run(self, timeout, runner):
        """
        This is for running the updater with a certain timeout between the
        updates
        """
        runner.run()
        sleep(timeout)
        run(timeout, runner)


def main():
    parser = ArgumentParser()
    parser.add_argument('--threads',
        help='How many feeds should be fetched in paralell, defaults to 10',
        default=10)
    parser.add_argument('--interval',
        help='Update interval between fetching the next round of \
            updates in minutes, defaults to 30 minutes',
        default=30)
    parser.add_argument('--user',
        help='A username to log into ownCloud', required=True)
    parser.add_argument('--password',
        help='A password to log into ownCloud', required=True)
    parser.add_argument('url',
        help='The URL where owncloud is installed')
    args = parser.parse_args()

    updater = Updater(args.url, args.user, args.password, args.threads)
    daemon = Daemon()
    daemon.run(args.interval, updater)


if __name__ == '__main__':
    main()


