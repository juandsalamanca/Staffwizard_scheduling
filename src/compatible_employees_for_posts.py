from overlapp import *

def get_compatibile_employees_for_posts(employees, clients, permanent, beta):
  checked_posts={}
  #print("Number of employees:", len(employees))
  for client in clients:
    posts = client['posts']
    for post in posts:
      shifts = post['weeks_periods'][0]['shifts']
      post_id = post['real_post_id']
      if post_id not in checked_posts:
        checked_posts[post_id]={}
      #print("Post ID:", post_id)
      #print("Checked posts:", checked_posts.keys())
      #print("Number fo shifts in this post:", len(shifts))

      for shift in shifts:
        shift_id = shift['id']
        #print("Shift ID:", shift_id)
        checked_posts[post_id][shift_id]={"Shift_info":[], "Employees":[]}
        checked_posts[post_id][shift_id]["Shift_info"].append(shift)
        for employee in employees:
          posts_can_be_work = employee['posts_can_be_work']
          emp_id = employee['employee_id']
          #print("Employee ID:", emp_id)
          for potential_post in posts_can_be_work:
            p_post_id = potential_post['post_id']
            if post_id == p_post_id and potential_post['can_work_on_this_post'] == True:
              #print("Found compatible post:", post_id)
              distance = float(potential_post['distance'])
              overlap_count = 0
              for perm in permanent[emp_id]:
                overlap = check_overlapp(emp_shift=perm, post_shift=shift)
                if overlap == True:
                  overlap_count +=1
              if overlap_count == 0:
                #print(f"No overlaps, assigning shift {shift_id} in post {post_id} to employee {emp_id}")
                try:
                  pay_rate = float(employee['pay_rate'])
                except:
                  pay_rate = 1000000.0
                checked_posts[post_id][shift_id]["Employees"].append(employee)
                checked_posts[post_id][shift_id]["Employees"][-1]['distance']= distance
                score = pay_rate + beta*distance
                checked_posts[post_id][shift_id]["Employees"][-1]['Score']= score
                break
          #print("Employee end -------------------------------------")
        #print("Shift end  -------------------------------------------")
      #print("Post end  -------------------------------------------")

      #print(f"Number of shifts for post {post_id}: {len(checked_posts[post_id])}")
  return checked_posts
