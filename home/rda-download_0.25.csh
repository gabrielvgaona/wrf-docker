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
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061400.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061400.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061400.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061400.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061406.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061406.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061406.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061406.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061412.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061412.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061412.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061412.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061418.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061418.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061418.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061418.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061500.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061500.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061500.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061500.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061506.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061506.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061506.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061506.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061512.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061512.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061512.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061512.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061518.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061518.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061518.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061518.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061600.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061600.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061600.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061600.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061606.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061606.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061606.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061606.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061612.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061612.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061612.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061612.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061618.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061618.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061618.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061618.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061700.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061700.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061700.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061700.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061706.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061706.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061706.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061706.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061712.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061712.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061712.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061712.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061718.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061718.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061718.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061718.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061800.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061800.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061800.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061800.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061806.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061806.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061806.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061806.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061812.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061812.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061812.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061812.f09.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061818.f00.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061818.f03.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061818.f06.grib2  \
  https://data.rda.ucar.edu/d083003/2024/202406/gdas1.fnl0p25.2024061818.f09.grib2  \
)
while($#filelist > 0)
  set syscmd = "wget $cert_opt $opts $filelist[1]"
  echo "$syscmd ..."
  $syscmd
  shift filelist
end
