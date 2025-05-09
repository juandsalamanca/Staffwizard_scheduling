from shift_times import *
from rate_and_distance import *
from overlapp import *

def assign_shifts(posts, employees, permanent_shifts_by_employee, permanent_shift_ids):
  #Create the employee dictionary:
  #permanent
  empty_shifts = {}
  assigned_employees = {}
  for employee in employees:
    id = employee['employee_id']
    assigned_employees[id]=[]
    if id in permanent_shifts_by_employee:
      for shift in permanent_shifts_by_employee[id]:
        assigned_employees[id].append(shift)
  for post_id in posts:
    empty_shifts[post_id] = []
    shifts = posts[post_id]
    for shift_id in shifts:
      shift = shifts[shift_id]
      # Create new key for the shift dict to keep track of the assigned employee
      shift["Assigned_to"]=[]
      shift_info = shift["Shift_info"][0]
      #If the shift is permanent we assign it as is:
      if shift_id in permanent_shift_ids:
        shift["Assigned_to"].append(permanent_shift_ids[shift_id])
      # Get the potential employees for the shift and sort them according to daily overtime, this returns a list of dicts with id, score, daily and weekly OT
      sorted_employees = order_employees_on_overtime(shift=shift, assigned=assigned_employees)
      # Now we order the employees with same OT by the payrate/distance score
      sorted_employees = order_rate_and_distance(sorted_employees)
      # Initialize variable to save the first employee with no overlaps
      save_emp = True
      justin_case = None
      for idx, employee in enumerate(sorted_employees):
        if len(shift["Assigned_to"]) > 0:
          break
        id = employee['id']
        assigned_shifts = assigned_employees[id]
        # We initialize the overlap and weekly ot count
        overlap_count=0
        weekly_overtime_count=0
        alt_shift_info = []
        for assigned_shift in assigned_shifts:
          #Check if there's any overlap between shifts
          overlap = check_overlapp(emp_shift=assigned_shift, post_shift=shift_info)
          alt_shift_info.append([assigned_shift["id"], assigned_shift["day_of_week"], assigned_shift["shift_start_time"], assigned_shift["shift_end_time"]])
          if overlap == True :
            overlap_count+=1
          if employee["weekly_time"] >= 40:
            weekly_overtime_count+=1
        #print(alt_shift_info)
        # Save the first employee with no overlaps, set save_emp to False so that no other emp gets saved
        if overlap_count == 0 and save_emp == True:
          justin_case = idx
          save_emp = False
        #If no overlap or wekly OT was found, assign shift to current employee
        if (weekly_overtime_count +  overlap_count) == 0:
          assigned_employees[id].append(shift_info)
          shift_info["employee_id"] = id
          shift["Assigned_to"].append(id)
          #print(f"Assigned employee {id} to shift {shift_id}")
          break
      #If no employee was suitable then assign the first one with no overlaps
      if len(shift['Assigned_to']) == 0:
        if justin_case != None:
          employee = sorted_employees[justin_case]
          id = employee['id']
          shift_info["employee_id"] = id
          shift["Assigned_to"].append(id)
          assigned_employees[id].append(shift_info)
        else:
          empty_shifts[post_id].append(shift_info)

  return posts, assigned_employees, empty_shifts
