# Databricks notebook source
dbutils.help()

# COMMAND ----------

dbutils.data.help()

# COMMAND ----------

dbutils.fs.help()

# COMMAND ----------

dbutils.fs.ls("/user/")

# COMMAND ----------

dbutils.fs.ls("/user/hive/warehouse")

# COMMAND ----------

dbutils.fs.ls("/user/hive/warehouse/airports/")

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE airports

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC DESCRIBE TABLE airport_frequencies

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT ap.name
# MAGIC       ,ap.*
# MAGIC       ,apf.*
# MAGIC   FROM airports ap
# MAGIC   JOIN airport_frequencies apf
# MAGIC     ON ap.id = apf.airport_ref
# MAGIC  ORDER BY 1

# COMMAND ----------

# MAGIC %md
# MAGIC **Range Join**
# MAGIC 
# MAGIC Enable range join using a range join hint
# MAGIC 
# MAGIC [range-join](https://learn.microsoft.com/en-gb/azure/databricks/optimizations/range-join)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC        ap.id
# MAGIC 	  ,ap.latitude_deg
# MAGIC 	  ,ap.longitude_deg
# MAGIC       ,ap0.id 
# MAGIC 	  ,ap0.latitude_deg
# MAGIC 	  ,ap0.longitude_deg
# MAGIC       ,ap1.id 
# MAGIC 	  ,ap1.latitude_deg
# MAGIC 	  ,ap1.longitude_deg          
# MAGIC   FROM airports ap
# MAGIC   JOIN airports ap0
# MAGIC     ON ap.latitude_deg between ap0.latitude_deg-ap0.latitude_deg/10000.0 and ap0.latitude_deg+ap0.latitude_deg/10000.0
# MAGIC    AND ap.longitude_deg between ap0.longitude_deg-ap0.longitude_deg/10000.0 and ap0.longitude_deg+ap0.longitude_deg/10000.0
# MAGIC   JOIN airports ap1
# MAGIC     ON ap0.latitude_deg between ap1.latitude_deg-ap1.latitude_deg/10000.0 and ap1.latitude_deg+ap1.latitude_deg/10000.0
# MAGIC    AND ap0.longitude_deg between ap1.longitude_deg-ap1.longitude_deg/10000.0 and ap1.longitude_deg+ap1.longitude_deg/10000.0
# MAGIC  ORDER BY ap.id,ap0.id,ap1.id
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*)
# MAGIC   FROM airports ap
# MAGIC   JOIN airports ap0
# MAGIC     ON cast(ap.latitude_deg as float)  between cast(ap0.latitude_deg as float)-0.01 and cast(ap0.latitude_deg as float)+0.01
# MAGIC    AND cast(ap.longitude_deg as float) between cast(ap0.longitude_deg as float)-0.01 and cast(ap0.longitude_deg as float)+0.01
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC SELECT count(*)
# MAGIC   FROM airports ap
# MAGIC   JOIN airports ap0
# MAGIC     ON cast(ap.latitude_deg as float)  between cast(ap0.latitude_deg as float)-0.01 and cast(ap0.latitude_deg as float)+0.01
# MAGIC    AND cast(ap.longitude_deg as float) between cast(ap0.longitude_deg as float)-0.01 and cast(ap0.longitude_deg as float)+0.01
# MAGIC   JOIN airports ap1
# MAGIC     ON cast(ap0.latitude_deg as float)  between cast(ap1.latitude_deg as float)-0.01 and cast(ap1.latitude_deg as float)+0.01
# MAGIC    AND cast(ap0.longitude_deg as float) between cast(ap1.longitude_deg as float)-0.01 and cast(ap1.longitude_deg as float)+0.01
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC SELECT /*+ RANGE_JOIN(ap,  0.01) */
# MAGIC        /*+ RANGE_JOIN(ap0, 0.01) */
# MAGIC        count(*)
# MAGIC   FROM airports ap
# MAGIC   JOIN airports ap0
# MAGIC     ON cast(ap.latitude_deg as float)  between cast(ap0.latitude_deg as float)-0.01 and cast(ap0.latitude_deg as float)+0.01
# MAGIC    AND cast(ap.longitude_deg as float) between cast(ap0.longitude_deg as float)-0.01 and cast(ap0.longitude_deg as float)+0.01
# MAGIC   JOIN airports ap1
# MAGIC     ON cast(ap0.latitude_deg as float)  between cast(ap1.latitude_deg as float)-0.01 and cast(ap1.latitude_deg as float)+0.01
# MAGIC    AND cast(ap0.longitude_deg as float) between cast(ap1.longitude_deg as float)-0.01 and cast(ap1.longitude_deg as float)+0.01
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC SELECT /*+ RANGE_JOIN(ap,  0.01) */
# MAGIC        /*+ RANGE_JOIN(ap0, 0.01) */
# MAGIC        /*+ RANGE_JOIN(ap1, 0.01) */
# MAGIC        count(*)
# MAGIC   FROM airports ap
# MAGIC   JOIN airports ap0
# MAGIC     ON cast(ap.latitude_deg as float)  between cast(ap0.latitude_deg as float)-0.01 and cast(ap0.latitude_deg as float)+0.01
# MAGIC    AND cast(ap.longitude_deg as float) between cast(ap0.longitude_deg as float)-0.01 and cast(ap0.longitude_deg as float)+0.01
# MAGIC   JOIN airports ap1
# MAGIC     ON cast(ap0.latitude_deg as float)  between cast(ap1.latitude_deg as float)-0.01 and cast(ap1.latitude_deg as float)+0.01
# MAGIC    AND cast(ap0.longitude_deg as float) between cast(ap1.longitude_deg as float)-0.01 and cast(ap1.longitude_deg as float)+0.01
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC 
# MAGIC SELECT /*+ RANGE_JOIN(ap,  0.001) */
# MAGIC        /*+ RANGE_JOIN(ap0, 0.001) */
# MAGIC        /*+ RANGE_JOIN(ap1, 0.001) */
# MAGIC        count(*)
# MAGIC   FROM airports ap
# MAGIC   JOIN airports ap0
# MAGIC     ON cast(ap.latitude_deg as float)  between cast(ap0.latitude_deg as float)-0.01 and cast(ap0.latitude_deg as float)+0.01
# MAGIC    AND cast(ap.longitude_deg as float) between cast(ap0.longitude_deg as float)-0.01 and cast(ap0.longitude_deg as float)+0.01
# MAGIC   JOIN airports ap1
# MAGIC     ON cast(ap0.latitude_deg as float)  between cast(ap1.latitude_deg as float)-0.01 and cast(ap1.latitude_deg as float)+0.01
# MAGIC    AND cast(ap0.longitude_deg as float) between cast(ap1.longitude_deg as float)-0.01 and cast(ap1.longitude_deg as float)+0.01
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC SET LastChangeDate =current_date()
# MAGIC ;
# MAGIC 
# MAGIC SELECT ${hiveconf:LastChangeDate}
# MAGIC ;
