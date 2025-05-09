from datetime import datetime


def calculate_shift_time(shift):
  time_format = '%H:%M:%S'
  start_str = shift['shift_start_time']
  end_str = shift['shift_end_time']
  hour_str = '23:59:59'
  start = datetime.strptime(start_str, time_format)
  start_float = start.hour + start.minute / 60 + start.second / 3600
  end = datetime.strptime(end_str, time_format)
  end_float = end.hour + end.minute / 60 + end.second / 3600
  hour = datetime.strptime(hour_str, time_format)
  hour_float = hour.hour + hour.minute / 60 + hour.second / 3600
  if end < start:
    t = end_float -start_float + hour_float
  else:
    t = end_float - start_float
  return t

def calculate_shifttime(assigned, potential, id, score):
  day = potential['day_of_week']
  potential_time = calculate_shift_time(potential)
  daily_time = potential_time
  weekly_time = potential_time
  for assigned_shift in assigned:
    a_day = assigned_shift['day_of_week']
    assigned_time = calculate_shift_time(assigned_shift)
    weekly_time += assigned_time
    if a_day == day :
      daily_time += assigned_time

  #We add the emp od to the dict so we can refernce it later in the main code

  return {"id": id, "weekly_time": weekly_time, "daily_time": daily_time, "score": score}


def order_employees_on_overtime(shift, assigned):
  shift_employees = shift['Employees']
  shift_info = shift["Shift_info"][0]
  employee_list=[]
  for employee in shift_employees:
    id = employee['employee_id']
    assigned_shifts = assigned[id]
    score = employee['Score']
    shifttime = calculate_shifttime(assigned=assigned_shifts, potential=shift_info, id=id, score=score)
    employee_list.append(shifttime)
  #Order the list with respect to weekly time
  sorted_employee_list = sorted(employee_list, key=lambda x: x["weekly_time"])
  #Now we construct the dict using the ordered list
  # This way we can reference each employee and overtime by its ID but it goes in order when you loop through it
  #employee_dict={}
  #for emp in sorted_employee_list:
  #  id = emp['employee_id']
  #  employee_dict[id] = emp
  return sorted_employee_list
