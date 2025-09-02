🚀 Data Engineering Interview Refresh Kit

1. What Makes an ETL/Data Pipeline Scalable?

Scalability = ability to handle more data or users without breaking.
Key techniques:

Parallelization / Multithreading → Break big jobs into smaller chunks processed simultaneously.

Distributed Processing → Use frameworks (Spark, Flink, Hadoop) to spread work across multiple machines.

Containerization (Docker, Kubernetes) → Run jobs in isolated, easily reproducible environments; scale workers up/down as needed.

Message Queues (Kafka, RabbitMQ, SQS) → Decouple producers and consumers, allowing asynchronous and resilient processing.

Partitioning/Sharding → Split large tables/files into smaller, parallelizable chunks (by time, ID, region, etc.).

Streaming vs Batch → Stream when near-real-time data is needed; batch for heavy but less frequent workloads.


💡 Interview tip: Pick one or two techniques and give an example from your work. That grounds your answer in reality.


---

2. TRUNCATE vs DELETE

DELETE

Removes rows one by one (can use WHERE).

Logs each row removal (slower on big tables).

Can be rolled back (transaction-safe).

Triggers DELETE triggers.


TRUNCATE

Removes all rows (no WHERE).

Drops and resets table pages (much faster).

Resets identity/auto-increment counters.

Cannot be rolled back in some systems (depends on DB).

No triggers fired.



💡 Rule of thumb: Use DELETE for selective row removal; TRUNCATE for wiping a table clean.


---

3. SQL Query Execution Order

Even though you write SQL as SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY, the execution order is:

1. FROM / JOIN → build dataset


2. WHERE → filter rows


3. GROUP BY → group rows


4. HAVING → filter groups


5. SELECT → choose columns/expressions


6. ORDER BY → sort results


7. LIMIT → final row restriction




---

4. HAVING vs WHERE

WHERE → filters before grouping (on raw rows).

HAVING → filters after grouping (on aggregates).


Example:

-- WHERE filters rows before grouping
SELECT department, AVG(salary)
FROM employees
WHERE salary > 50000
GROUP BY department;

-- HAVING filters groups after aggregation
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000;


---

5. Other Quick-Hit SQL Refreshers

Indexes → speed up reads, slow down writes. Use on columns in WHERE, JOIN, ORDER BY.

Normalization vs Denormalization

Normalization = reduce redundancy, better writes.

Denormalization = faster reads, common in analytics.


Window Functions (ROW_NUMBER(), RANK(), SUM() OVER(...)) → used for advanced aggregations without collapsing rows.

ACID Properties → Atomicity, Consistency, Isolation, Durability.



---

6. Data Engineering Scaling Concepts

Batch vs Streaming

Batch = periodic, big chunks (nightly ETL).

Streaming = continuous, real-time (Kafka + Flink/Spark Streaming).


Idempotency → re-running the same job doesn’t break data (e.g., MERGE instead of duplicate inserts).

Orchestration → tools like Airflow, Prefect, Dagster manage dependencies, retries, scheduling.

Cloud Scaling Patterns

Storage: partitioning (S3, Delta Lake).

Compute: autoscaling clusters (Databricks, EMR).