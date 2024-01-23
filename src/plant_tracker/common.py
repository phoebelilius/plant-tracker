from datetime import datetime


def format_time_difference(last_watered):
    if not last_watered:
        return "Never"

    time_difference = datetime.now() - last_watered

    if time_difference.days > 0:
        return f"{time_difference.days} {'day' if time_difference.days == 1 else 'days'} ago"
    elif time_difference.seconds // 3600 > 0:
        return f"{time_difference.seconds // 3600} {'hour' if time_difference.seconds // 3600 == 1 else 'hours'} ago"
    else:
        return "Less than an hour ago"
