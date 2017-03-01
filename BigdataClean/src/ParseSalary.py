import re

def ParseSalary(salary):
    
    salary = "        " + salary
    p_salary = salary
    p_salary = re.sub(r',000', 'K', p_salary)
    p_salary = re.sub(r'0000', '0K', p_salary)
    p_salary = re.sub(r'000', 'K', p_salary)
    
    pre_salary = later_salary = 0
    for salary_index in range(len(p_salary)-1,0,-1):
        if p_salary[salary_index] == 'K' and p_salary[salary_index-1].isdigit():
            for salary_index_r in range(salary_index-1,-1,-1):
                if not p_salary[salary_index_r].isdigit() and p_salary[salary_index_r] != '.':
                    break
            later_salary = float(p_salary[salary_index_r+1:salary_index])
            # get the lower bound salary
            for salary_index_l in range(salary_index-3,0,-1):
                if salary_index_l <= salary_index-10:
                    break
                if p_salary[salary_index_l].isdigit() and \
                    (p_salary[salary_index_l-1].isdigit() or p_salary[salary_index_l-1] == ' '):
                    pre_salary = float(p_salary[salary_index_l-1:salary_index_l+1])
                    break
            break
    if pre_salary > later_salary:
        later_salary = later_salary * 10
        
    return str(pre_salary)+" | "+str(later_salary)

