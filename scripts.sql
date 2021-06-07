SELECT EXTRACT(year FROM date_application)  as year,
       EXTRACT(month FROM date_application) as month,
       count(EXTRACT(month FROM date_application))
FROM main_loanapplication
group by year, month;



SELECT *
from main_loanapplication
where client_fk_id = '9872927854'
ORDER BY date_application desc
LIMIT 1;

SELECT all_loan_app.client_fk_id
from main_loanapplication as all_loan_app
         join main_loanapplication as aprovved
              on all_loan_app.client_fk_id = aprovved.client_fk_id
where aprovved.solution = 'Одобрено'
  and all_loan_app.date_application > aprovved.date_application;
