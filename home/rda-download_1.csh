#!/usr/bin/env csh
#
# c-shell script to download selected files from rda.ucar.edu using Wget
# NOTE: if you want to run under a different shell, make sure you change
#       the 'set' commands according to your shell's syntax
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
# Experienced Wget Users: add additional command-line flags to 'opts' here
#   Use the -r (--recursive) option with care
#   Do NOT use the -b (--background) option - simultaneous file downloads
#       can cause your data access to be blocked
set opts = "-N"
#
# Check wget version.  Set the --no-check-certificate option 
# if wget version is 1.10 or higher
set v = `wget -V |grep 'GNU Wget ' | cut -d ' ' -f 3`
set a = `echo $v | cut -d '.' -f 1`
set b = `echo $v | cut -d '.' -f 2`
if(100 * $a + $b > 109) then
  set cert_opt = "--no-check-certificate"
else
  set cert_opt = ""
endif

set filelist= ( \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240601_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240601_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240601_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240601_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240602_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240602_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240602_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240602_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240603_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240603_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240603_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240603_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240604_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240604_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240604_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240604_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240605_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240605_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240605_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240605_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240606_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240606_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240606_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240606_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240607_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240607_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240607_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240607_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240608_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240608_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240608_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240608_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240609_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240609_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240609_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240609_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240610_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240610_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240610_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240610_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240611_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240611_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240611_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240611_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240612_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240612_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240612_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240612_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240613_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240613_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240613_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240613_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240614_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240614_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240614_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240614_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240615_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240615_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240615_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240615_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240616_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240616_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240616_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240616_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240617_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240617_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240617_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240617_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240618_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240618_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240618_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240618_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240619_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240619_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240619_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240619_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240620_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240620_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240620_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240620_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240621_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240621_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240621_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240621_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240622_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240622_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240622_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240622_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240623_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240623_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240623_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240623_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240624_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240624_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240624_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240624_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240625_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240625_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240625_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240625_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240626_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240626_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240626_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240626_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240627_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240627_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240627_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240627_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240628_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240628_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240628_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240628_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240629_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240629_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240629_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240629_18_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240630_00_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240630_06_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240630_12_00.grib2  \
  https://data.rda.ucar.edu/d083002/grib2/2024/2024.06/fnl_20240630_18_00.grib2  \
)
while($#filelist > 0)
  set syscmd = "wget $cert_opt $opts $filelist[1]"
  echo "$syscmd ..."
  $syscmd
  shift filelist
end
