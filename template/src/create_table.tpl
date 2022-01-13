CREATE TABLE {{ data.keyspace }}.{{ data.table }} (
   field1 text, 
   PRIMARY KEY (field1)) 
WITH CLUSTERING ORDER BY (field1 DESC);