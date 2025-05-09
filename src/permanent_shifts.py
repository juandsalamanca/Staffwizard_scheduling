

def scan_permanent_shifts(employees):
  perma_shifts={}
  for employee in employees:
    perma_shifts[employee['employee_id']] = []
    if len(employee['weeks_periods']) == 0:
      raise Exception(f"No weeks_periods inside employee {employee['employee_id']}")
    shifts = employee['weeks_periods'][0]['shifts']
    for shift in shifts:
      if shift['is_permanent'] == True:
        perma_shifts[employee['employee_id']].append(shift)
  return perma_shifts


#Using the permanent shifts of the employees of previous week we get the shifts that should be assigned to them for the next week

def map_permanent_shifts(permanent_shifts, future_clients):

  future_permanent_shifts = {}
  permanent_shift_ids = {}

  for emp_id in permanent_shifts:
    shifts = permanent_shifts[emp_id]
    for shift in shifts:
      day = shift['day_of_week']
      start_time = shift['shift_start_time']
      end_time = shift['shift_end_time']
      post_id = shift['post_location_id']
      for client in future_clients:
        posts = client['posts']
        for post in posts:
          period = post['weeks_periods'][0]
          future_shifts = period['shifts']
          for future_shift in future_shifts:
            future_day = future_shift['day_of_week']
            future_start_time = future_shift['shift_start_time']
            future_end_time = future_shift['shift_end_time']
            future_post_id = future_shift['post_location_id']
            future_shift_id = future_shift['id']
            if day == future_day and start_time == future_start_time and end_time == future_end_time and post_id == future_post_id:
              if emp_id not in future_permanent_shifts:
                future_permanent_shifts[emp_id] = []
              if future_shift not in future_permanent_shifts[emp_id]:
                future_permanent_shifts[emp_id].append(future_shift)
              if future_shift_id not in permanent_shift_ids:
                permanent_shift_ids[future_shift_id] = []
              permanent_shift_ids[future_shift_id].append(emp_id)

  return future_permanent_shifts, permanent_shift_ids

