from overlapp import *

def assign_permanent_shifts(clients, future_employees, permanent_shift_ids):
  assigned_employees = {}
  assigned_shifts = {}
  #for p_shift_ids in permanent_shift_ids:
  #  assigned_shifts[p_shift_ids] = []
  for employee in future_employees:
    id = employee['employee_id']
    assigned_employees[id]=[]
  for client in clients:
    posts = client['posts']
    for post in posts:
      shifts = post['weeks_periods'][0]['shifts']
      post_id = post['real_post_id']
      for shift in shifts:
        shift_id = shift['id']

        if shift_id in permanent_shift_ids:
          for emp in permanent_shift_ids[shift_id]:
            # First we need to check if the suitable employee from last week is even available for the future week
            # If its notm then the shift id will never be a key fo the assigned shifts dict and no employee will get that shift for now
            if emp in assigned_employees:
              #if emp == '381':
                emp_shifts = assigned_employees[emp]
                overlap_count = 0
                for emp_shift in emp_shifts:
                  overlap = check_overlapp(emp_shift, shift)
                  #print("----------------------------")
                  if overlap == True:
                    overlap_count+=1
                if overlap_count == 0:
                  assigned_employees[emp].append(shift)
                  assigned_shifts[shift_id] = emp
                  break

  return assigned_employees, assigned_shifts
