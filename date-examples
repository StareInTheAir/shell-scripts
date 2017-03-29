#! /bin/bash

# An overly obvious reference for most commonly requested bash timestamps
# Now all you Mac fags can stop pestering me.

cat << EOD
        Format/result         |       Command              |          Output
------------------------------+----------------------------+------------------------------
YY-MM-DD_hh:mm:ss             | date +%F_%T                | $(date +%F_%T)
YYMMDD_hhmmss                 | date +%Y%m%d_%H%M%S        | $(date +%Y%m%d_%H%M%S)
YYMMDD_hhmmss (UTC version)   | date --utc +%Y%m%d_%H%M%SZ | $(date --utc +%Y%m%d_%H%M%SZ)
YYMMDD_hhmmss (with local TZ) | date +%Y%m%d_%H%M%S%Z      | $(date +%Y%m%d_%H%M%S%Z)
YYMMSShhmmss                  | date +%Y%m%d%H%M%S         | $(date +%Y%m%d%H%M%S)
YYMMSShhmmssnnnnnnnnn         | date +%Y%m%d%H%M%S%N       | $(date +%Y%m%d%H%M%S%N)
Seconds since UNIX epoch:     | date +%s                   | $(date +%s)
Nanoseconds only:             | date +%N                   | $(date +%N)
Nanoseconds since UNIX epoch: | date +%s%N                 | $(date +%s%N)
ISO8601 UTC timestamp         | date --utc +%FT%TZ         | $(date --utc +%FT%TZ)
ISO8601 Local TZ timestamp    | date +%FT%T%Z              | $(date +%FT%T%Z)
EOD
