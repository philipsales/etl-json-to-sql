DEV datasource
curl -v http:e//172.104.49.91:8093/query/service -H 'Accept: application/json' -H 'Authorization: Basic c3VwZXJtYW46a3J5cHRvbml0ZQ==' -H 'Cache-Control: no-cache' -H 'Postman-Token: d05030f2-c373-4215-9016-886674fa9265' -d 'statement=SELECT meta(awhcurisdb010832).id as cb_id, awhcurisdb010832.* FROM `awhcurisdb010832` WHERE (address.country="Philippines" OR address.country="PHL") AND _deleted IS MISSING AND LOWER(organization)!="test rhu" AND type="user-resident" ' >> source.4087-items.json

UAT datasource
curl -v http://13.76.6.56:8093/query/service    -H 'Accept: application/json' -H 'Authorization: Basic c3VwZXJtYW46a3J5cHRvbml0ZQ==' -H 'Cache-Control: no-cache' -H 'Postman-Token: 3cf974b2-b950-4133-a74d-8b30fb6809f5' -d 'statement=SELECT meta(awhcurisdb).id as cb_id, awhcurisdb.* FROM `awhcurisdb` ' >> source.38470-items.json