import calendar

import math

import datetime

from django import template

from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter

from django.utils import timezone

from django.utils.translation import gettext_lazy, ngettext_lazy, gettext

from django.utils.html import avoid_wrapping

register = template.Library()

TIME_STRINGS = {
    "year": ngettext_lazy("a year", "%d years"),
    "month": ngettext_lazy("a month", "%d months"),
    "week": ngettext_lazy("a week", "%d weeks"),
    "day": ngettext_lazy("a day", "%d days"),
    # we may not need the items below: if day <1, levelup_timesince is not called
    "hour": ngettext_lazy("%d hour", "%d hours"),
    "minute": ngettext_lazy("%d minute", "%d minutes"),
}

TIMESINCE_CHUNKS = (
    (60 * 60 * 24 * 365, "year"),
    (60 * 60 * 24 * 30, "month"),
    (60 * 60 * 24 * 7, "week"),
    (60 * 60 * 24, "day"),
    (60 * 60, "hour"),
    (60, "minute"),
)


def levelup_timesince(d, now=None, reversed=False, time_strings=None):
    """

        Take two datetime objects and return the time between d and now as a nicely

        formatted string, e.g. "10 minutes". If d occurs after now, return

        "0 minutes".

        Units used are years, months, weeks, days, hours, and minutes.

        Seconds and microseconds are ignored.  Up to two adjacent units will be

        displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are

        possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

        `time_strings` is an optional dict of strings to replace the default

        TIME_STRINGS dict.

        Adapted from
    https://web.archive.org/web/20060617175230/http://blog.natbat.co.uk/archive/2003/Jun/14/time_since

    """

    if time_strings is None:
        time_strings = TIME_STRINGS

    # Convert datetime.date to datetime.datetime for comparison.

    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)

    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    now = now if now else timezone.now()

    if reversed:
        d, now = now, d

    delta = now - d

    # Deal with leapyears by subtracing the number of leapdays

    leapdays = calendar.leapdays(d.year, now.year)

    if leapdays != 0:

        if calendar.isleap(d.year):

            leapdays -= 1

        elif calendar.isleap(now.year):

            leapdays += 1

    delta -= datetime.timedelta(leapdays)

    # ignore microseconds

    since = delta.days * 24 * 60 * 60 + delta.seconds

    if since <= 0:
        # d is in the future compared to now, stop processing.

        return avoid_wrapping(gettext("0 minutes"))

    for i, (seconds, name) in enumerate(TIMESINCE_CHUNKS):

        count = since // seconds

        if count != 0:
            break

    result = avoid_wrapping(time_strings[name] % count)

    # Not considering second item because of limited space in phone end UI

    # that means 67 days will show, 2 months ago or 2 months from now

    # if i + 1 < len(TIMESINCE_CHUNKS):

    # seconds2, name2 = TIMESINCE_CHUNKS[i + 1]

    # count2 = (since - (seconds * count)) // seconds2

    # if count2 != 0:

    #     result += gettext(', ') + avoid_wrapping(time_strings[name2] % count2)

    return result


def levelup_timeuntil(d, now=None, time_strings=None):
    """

    Like levelup_timesince, but return a string measuring the time until the given time.

    """

    return levelup_timesince(d, now, reversed=True, time_strings=time_strings)


@register.filter
def levelup_naturaltime(value):
    """

    For date and time values show how many seconds, minutes, or hours ago

    compared to current timestamp return representing string.

    """

    return LevelUpNaturalTimeFormatter.string_for(value)


class LevelUpNaturalTimeFormatter(NaturalTimeFormatter):
    time_strings = NaturalTimeFormatter.time_strings

    update_dict = {
        "now": gettext_lazy("just now"),
        "past-while": gettext_lazy("a while ago"),  # for returning "a while ago"
        # 'yesterday': gettext_lazy('yesterday'),
        # 'tomorrow': gettext_lazy('tomorrow'),
        "future-hour": ngettext_lazy("an hour", "%(count)s hours", "count"),
        "future-day": gettext_lazy("%(delta)s"),
    }

    time_strings.update(update_dict)

    @classmethod
    def string_for(cls, value):

        if not isinstance(value, datetime.date):  # datetime is a subclass of date

            return value

        now = timezone.now()

        if value < now:

            delta = now - value

            # we may need 'yesterday' rather than 'a day ago' in future

            # delta_date_days = now.date() - value.date()

            # if delta_date_days.days == 1:

            #     return cls.time_strings['yesterday']

            #

            # if delta.days == 1:

            #     return cls.time_strings['yesterday']

            if delta.days != 0:

                return cls.time_strings["past-day"] % {
                    "delta": levelup_timesince(value, now),
                }

            elif delta.seconds // 60 < 1:

                return cls.time_strings["now"]

            elif delta.seconds // 60 < 10:

                return cls.time_strings["past-while"]

            elif delta.seconds // 60 < 60:

                count = delta.seconds // 60

                return cls.time_strings["past-minute"] % {"count": count}

            else:

                count = delta.seconds // 60 // 60

                return cls.time_strings["past-hour"] % {"count": count}

        else:

            delta = value - now

            # we may need 'tomorrow' rather than 'a day' in future

            # delta_date_days = value.date() - now.date()

            # if delta_date_days.days == 1:

            #     return cls.time_strings['tomorrow']

            # if delta.days == 1:

            #     return cls.time_strings['tomorrow']

            if delta.days != 0:

                return cls.time_strings["future-day"] % {
                    "delta": levelup_timeuntil(value, now),
                }

            elif delta.seconds == 0:

                return cls.time_strings["now"]

            else:

                # considering hour as the smallest time unit

                # if value of count in hours is 1 or 0, set value of count to 1

                # so it returns "an hour from now" in both cases

                # otherwise it returns {count} hours from now

                # we have used math.ceil for nearest large integer as we have only considered hour,

                # if the count value is 1.33, it shows 2 hours from now

                count = math.ceil(
                    delta.seconds // 60 / 60
                )  # for nearest large integer hour

                # edge case: if hour is 23.343 nearest large integer is 24,

                # replacing it with 23 hour

                # ToDo: make this case "in a day"

                if count == 24:
                    count = 23

                return cls.time_strings["future-hour"] % {"count": count}
