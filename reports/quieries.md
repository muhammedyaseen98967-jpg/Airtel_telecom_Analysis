1. Monthly network demand

How much data did the network carry each month, and how many subscribers used it?

SELECT
    strftime('%Y-%m', usage_date) AS month,
    COUNT(DISTINCT customer_id) AS active_subscribers,
    ROUND(SUM(data_mb) / 1024 / 1024, 2) AS total_tb
FROM usage_daily
GROUP BY month
ORDER BY month;
___________________________________________________________________________________________________

2. How many subscribers used the network each month?

How does the monthly network user count change?


SELECT
    strftime('%Y-%m', usage_date) AS month,
    COUNT(DISTINCT customer_id) AS active_subscribers
FROM usage_daily
GROUP BY month
ORDER BY month;

____________________________________________________________________________________________________

3. Daily network usage for the selected month

How much data did the network carry each day during the selected month?

SELECT
    usage_date,
    ROUND(SUM(data_mb) / 1024, 2) AS total_gb,
    COUNT(DISTINCT customer_id) AS active_subscribers
FROM usage_daily
WHERE strftime('%Y-%m', usage_date) = '2025-06'
GROUP BY usage_date
ORDER BY usage_date;
______________________________________________________________________________________________________

4. Group A vs Group B network usage

Does daily data usage differ between Group A (Control) and Group B (Experiment)?

SELECT
    u.usage_date,
    c.ab_group,
    ROUND(AVG(u.data_mb), 2) AS avg_data_mb,
    COUNT(DISTINCT u.customer_id) AS subscribers
FROM usage_daily u
JOIN customers c
    ON u.customer_id = c.customer_id
WHERE strftime('%Y-%m', u.usage_date) = '2025-06'
GROUP BY u.usage_date, c.ab_group
ORDER BY u.usage_date, c.ab_group;

_______________________________________________________________________________________________________

5. Data usage by device type

Which device types consume the most mobile data during the selected month?

SELECT
    c.device_type,
    ROUND(SUM(u.data_mb) / 1024, 2) AS total_gb,
    COUNT(DISTINCT u.customer_id) AS subscribers
FROM usage_daily u
JOIN customers c
    ON u.customer_id = c.customer_id
WHERE strftime('%Y-%m', u.usage_date) = '2025-06'
GROUP BY c.device_type
ORDER BY total_gb DESC;
________________________________________________________________________________________________________

6. Data usage per active day

How much data does a subscriber consume on an active usage day, month by month?

SELECT
    strftime('%Y-%m', usage_date) AS month,
    ROUND(AVG(data_mb), 2) AS avg_data_per_active_day_mb,
    COUNT(*) AS usage_day_records
FROM usage_daily
GROUP BY month
ORDER BY month;
________________________________________________________________________________________________________

7. Monthly data usage by Group A and Group B

How does the monthly average data usage compare between the control and experiment groups?

SELECT
    strftime('%Y-%m', u.usage_date) AS month,
    c.ab_group,
    ROUND(SUM(u.data_mb) / 1024, 2) AS total_gb,
    COUNT(DISTINCT u.customer_id) AS subscribers
FROM usage_daily u
JOIN customers c
    ON u.customer_id = c.customer_id
GROUP BY month, c.ab_group
ORDER BY month, c.ab_group;

__________________________________________________________________________________________________________

8. Plan allowance vs actual usage

How much of their data allowance are subscribers actually using for each plan?

SELECT
    p.plan_name,
    p.daily_data_gb,
    COUNT(DISTINCT c.customer_id) AS subscribers,
    ROUND(SUM(u.data_mb) / 1024 / 1024, 2) AS total_tb,
    ROUND(AVG(u.data_mb) / 1024, 2) AS avg_gb_per_usage_day
FROM customers c
JOIN plans p
    ON c.current_plan_id = p.plan_id
JOIN usage_daily u
    ON c.customer_id = u.customer_id
GROUP BY p.plan_name, p.daily_data_gb
ORDER BY p.daily_data_gb;
