create table ip_to_country (ip_from numeric, ip_to numeric, country_code2 text, country_code3 text, country_name text);
.separator ","
.import ip-to-country.csv ip_to_country
