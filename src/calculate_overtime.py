from duplicates import *
from shift_times import *

def calculate_final_overtime(employees):
  employee_shift_time = {}
  for employee_id in employees:
    employee_shift_time[employee_id] = {"shift_times": [], "days": []}
  for employee_id in employees:
    employee_shift_time[employee_id]["shift_times"] = []
    employee_shift_time[employee_id]["days"] = []
    employee = employees[employee_id]
    for shift in employee:
      day = shift["day_of_week"]
      t = calculate_shift_time(shift)
      employee_shift_time[employee_id]["shift_times"].append(t)
      employee_shift_time[employee_id]["days"].append(int(day))
    dupes = find_duplicates(employee_shift_time[employee_id]["days"])
    if len(dupes) >0:
      for day in dupes:
        employee_shift_time[employee_id]["daily_OT"] = {day: 0}
        i = 0
        day_list= employee_shift_time[employee_id]["days"]
        while i < len(day_list):
          if day_list[i] == day:
            employee_shift_time[employee_id]["daily_OT"][day] += employee_shift_time[employee_id]["shift_times"][i]
          i+=1
    employee_shift_time[employee_id]["total_shift_time"] = sum(employee_shift_time[employee_id]["shift_times"])

  return employee_shift_time
