CREATE KEYSPACE {{ data.keyspace }} 
  WITH REPLICATION = { 
   'class' : '{{ data.replication_strategy }}',
   '{{ data.datacenter }}': 1,
   'replication_factor' : {{ data.replication_factor }}
  } ;