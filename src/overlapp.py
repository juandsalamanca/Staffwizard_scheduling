from datetime import datetime, timedelta


def check_overlapp(emp_shift, post_shift):

  time_format = '%H:%M:%S'
  emp_day_of_the_week = emp_shift['day_of_week']
  emp_start = datetime.strptime(emp_shift['shift_start_time'], time_format)
  emp_start_time = emp_start.hour + emp_start.minute / 60 + emp_start.second / 3600
  emp_end = datetime.strptime(emp_shift['shift_end_time'], time_format)
  emp_end_time = emp_end.hour + emp_end.minute / 60 + emp_end.second / 3600

  post_day_of_the_week = post_shift['day_of_week']
  post_start = datetime.strptime(post_shift['shift_start_time'], time_format)
  post_start_time = post_start.hour + post_start.minute / 60 + post_start.second / 3600
  post_end = datetime.strptime(post_shift['shift_end_time'], time_format)
  post_end_time = post_end.hour + post_end.minute / 60 + post_end.second / 3600

  if emp_start_time > emp_end_time:
    emp_start_time = emp_start_time - 24.0

  if post_start_time > post_end_time:
    post_start_time = post_start_time - 24.0


  if emp_day_of_the_week == post_day_of_the_week:
    #print("Same Day")
    if (emp_end_time >= post_start_time) and (emp_start_time <= post_end_time):
      overlapp = True
      #print("Found overlap")
      #print(f"Employee shift info: day: {emp_day_of_the_week}, start time: {emp_start_time}, stop time: {emp_end_time}")
      #print(f"Post shift info: day: {post_day_of_the_week}, start time: {post_start_time}, stop time: {post_end_time}")
    else:
      overlapp = False
  else:
    overlapp = False

  return overlapp
