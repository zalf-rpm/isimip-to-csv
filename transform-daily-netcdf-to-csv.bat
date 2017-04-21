echo off
set start_y=%1
set end_y=%2
set start_year=1971
rem set start_year2=%3
rem set start_month=%4
rem if %start_month% neq 1 (
rem     echo running rest of year %start_year% starting with month %start_month%
rem     set /a start_year2+=1
rem     rem echo start_year=%start_year%
rem     for /l %%m in (%start_month%,1,12) do (
rem         rem echo month=%%m
rem         python transform-daily-netcdf-to-csv.py start-y=%start_y% end-y=%end_y% start-year=%start_year% end-year=%start_year% start-month=%%m end-month=%%m
rem     )
rem ) 

echo running years starting at %start_year%
for /l %%y in (%start_year%,1,2005) do (
    rem echo year=%%y
    for /l %%m in (1,1,12) do (
        rem echo month=%%m
        python transform-daily-netcdf-to-csv.py start-y=%start_y% end-y=%end_y% start-year=%%y end-year=%%y start-month=%%m end-month=%%m
    )
)