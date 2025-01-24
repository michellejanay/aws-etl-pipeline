SELECT
sum(total_amount), store_name from transactions group by store_name;