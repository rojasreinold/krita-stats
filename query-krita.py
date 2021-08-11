#!/usr/bin/env python

import time as real_time
from datetime import date, time, datetime, timedelta
import bugzilla

URL = "http://bugs.kde.org/rest"
bzapi = bugzilla.Bugzilla(URL)


def open_bugs_until(end_date):
    query_sum = []
    check_date = date.fromisoformat('2013-01-01')
    query = bzapi.url_to_query(("https://bugs.kde.org/"
                                "buglist.cgi?bug_severity=critical&bug_severity=grave&"
                                "bug_severity=major&bug_severity=crash&bug_severity=normal&"
                                "bug_severity=minor&bug_status=UNCONFIRMED&"
                                "bug_status=CONFIRMED&bug_status=ASSIGNED&"
                                "bug_status=REOPENED&product=krita"))
    query["include_fields"] = ["id", "summary"]
    query_sum += bzapi.query(query)
    print("total open bugs on " + end_date.strftime("%Y-%m-%d") + ": " + str(len(query_sum)))
    return query_sum


def reported_bugs_in_week(end_date):
    previous_week_date = end_date + timedelta(days=-7)
    query = bzapi.url_to_query("https://bugs.kde.org/"
                               "buglist.cgi?bug_severity=critical&bug_severity=grave&"
                                    "bug_severity=major&bug_severity=crash&bug_severity=normal&"
                                    "bug_severity=minor&"
                               "bug_status=UNCONFIRMED&bug_status=CONFIRMED&"
                               "bug_status=ASSIGNED&bug_status=REOPENED&bug_status=RESOLVED&"
                               "bug_status=NEEDSINFO&bug_status=VERIFIED&bug_status=CLOSED&"
                               "chfield=%5BBug%20creation%5D&"
                               "chfieldfrom=" + previous_week_date.strftime("%Y-%m-%d") + "&"
                               "chfieldto=" + end_date.strftime("%Y-%m-%d") + "&"
                               "list_id=1896439&order=bug_id&product=krita&query_format=advanced")
    query["include_fields"] = ["id", "summary"]
    return bzapi.query(query)


def closed_bugs_in_week(end_date):
    previous_week_date = end_date + timedelta(days=-7)
    query = bzapi.url_to_query("https://bugs.kde.org/"
                               "buglist.cgi?bug_severity=critical&bug_severity=grave&"
                                    "bug_severity=major&bug_severity=crash&bug_severity=normal&"
                                    "bug_severity=minor&"
                                "bug_status=RESOLVED&bug_status=CLOSED&"
                               "chfieldfrom=" + previous_week_date.strftime("%Y-%m-%d") + "&"
                               "chfieldto=" + end_date.strftime("%Y-%m-%d") + "&"
                               "list_id=1898207&product=krita&query_format=advanced")
    query["include_fields"] = ["id", "summary"]
    return bzapi.query(query)


def main():
    # All Reported bugs since until now
    # TODO: get all reported bugs  by slicing all requests by year and suming them up
    # Reported bugs for the last month
    today_date = date.today()
    reported_bugs = reported_bugs_in_week(today_date)

    closed_bugs = closed_bugs_in_week(today_date)
    print("Newly reported bugs: %d\nClosed bugs: %d" % (len(reported_bugs), len(closed_bugs)))

    all_open_bugs = open_bugs_until(today_date)


if __name__ == "__main__":
    main()
