import requests
from datetime import datetime, timedelta

def get_info_from_api(subdomain, branch, beginning, end):

        response_future_posts = requests.get(f"https://{subdomain}.staffwizarddev.com/cron/AI_api/get_schedule_data/1/{branch}/{beginning}/{end}")

        response_future_emp = requests.get(f"https://{subdomain}.staffwizarddev.com/cron/AI_api/get_schedule_data/0/{branch}/{beginning}/{end}")

        date_format = "%Y-%m-%d"

        date_beginning = datetime.strptime(beginning, date_format)

        date_end = datetime.strptime(end, date_format)

        new_beginning = date_beginning - timedelta(days=7)

        new_end = date_end - timedelta(days=7)

        new_beginning_str = new_beginning.strftime(date_format)

        new_end_str = new_end.strftime(date_format)

        response_posts = requests.get(f"https://{subdomain}.staffwizarddev.com/cron/AI_api/get_schedule_data/1/{branch}/{new_beginning_str}/{new_end_str}")

        response_emp = requests.get(f"https://{subdomain}.staffwizarddev.com/cron/AI_api/get_schedule_data/0/{branch}/{new_beginning_str}/{new_end_str}")

        emp = response_emp.json()

        future_emp = response_future_emp.json()

        posts = response_posts.json()

        future_posts = response_future_posts.json()

        return  emp,  future_emp, posts, future_posts
