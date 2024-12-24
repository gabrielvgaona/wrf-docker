FROM ubuntu:22.04
LABEL AUTHOR "Gabriel Gaona <gabo@gavg712.com>"
LABEL MAINTAINER "Gabriel Gaona <gabo@gavg712.com>"

# Set up base OS environment
RUN apt update -y
RUN apt install -y gcc g++ gfortran m4 make wget vim-tiny csh git
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
#RUN apt install -y file
RUN apt-get update -y --fix-missing
RUN apt install -y file build-essential curl perl libopenmpi-dev libhdf5-openmpi-dev libxml2-dev libnetcdff-dev
#RUN apt -y install mpich
#https://forum.mmm.ucar.edu/threads/full-wrf-and-wps-installation-example-gnu.12385/


# Set ENV
RUN mkdir -p /WRF_ins/wrf_dependencies
ENV InWRF /WRF_ins
ENV DIR $InWRF/wrf_dependencies
ENV NETCDF $DIR/netcdf
ENV LD_LIBRARY_PATH $NETCDF/lib:$DIR/grib2/lib
ENV PATH $NETCDF/bin:$DIR/mpich/bin:${PATH}
ENV JASPERLIB $DIR/grib2/lib
ENV JASPERINC $DIR/grib2/include

ENV CC gcc
ENV CXX g++
ENV FC gfortran
ENV FCFLAGS "-m64 -fallow-argument-mismatch"
ENV F77 gfortran
ENV FFLAGS "-m64 -fallow-argument-mismatch"
ENV LDFLAGS "-L$NETCDF/lib -L$DIR/grib2/lib"
ENV CPPFLAGS "-I$NETCDF/include -I$DIR/grib2/include -fcommon"
ENV J 16

# Install zlib

RUN cd $DIR \
&& wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-1.2.11.tar.gz \
&& tar xzvf zlib-1.2.11.tar.gz \
&& cd zlib-1.2.11 \
&& ./configure --prefix=$DIR/grib2 \
&& make -j $J \
&& make install \
&& cd $DIR \
&& rm -rf zlib*

# Install HDF5
RUN cd $DIR \
&& wget https://github.com/HDFGroup/hdf5/archive/hdf5-1_10_5.tar.gz \
&& tar xzvf hdf5-1_10_5.tar.gz \
&& cd hdf5-hdf5-1_10_5 \
&& ./configure --prefix=$DIR/netcdf --with-zlib=$DIR/grib2 --enable-fortran --enable-shared \
&& make -j $J \
&& make install \
&& cd $DIR \
&& rm -rf hdf5*

# Install NetCDF-C
RUN cd $DIR \
&& wget https://github.com/Unidata/netcdf-c/archive/v4.7.2.tar.gz \
&& tar xzvf v4.7.2.tar.gz \
&& cd netcdf-c-4.7.2 \
&& ./configure --prefix=$DIR/netcdf --disable-dap --enable-netcdf4 --enable-hdf5 --enable-shared \
&& make -j $J \
&& make install \
&& cd $DIR \
&& rm -rf v4.7.2.tar.gz netcdf-c*

# Install NetCDF-Fortran
ENV PATH $DIR/netcdf/bin:$PATH
ENV NETCDF $DIR/netcdf
ENV LIBS "-lnetcdf -lz"
RUN cd $DIR \
&& wget https://github.com/Unidata/netcdf-fortran/archive/v4.5.2.tar.gz \
&& tar xzvf v4.5.2.tar.gz \
&& cd netcdf-fortran-4.5.2 \
&& ./configure --prefix=$DIR/netcdf --disable-hdf5 --enable-shared \
&& make -j $J  \
&& make install \
&& cd $DIR \
&& rm -rf netcdf-fortran* v4.5.2.tar.gz

# Install mpich
RUN cd $DIR \
&& wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/mpich-3.0.4.tar.gz \
&& tar xzvf mpich-3.0.4.tar.gz \
&& cd mpich-3.0.4 \
&& ./configure --prefix=$DIR/mpich \
&& make -j $J 2>&1 \
&& make install \
&& cd $DIR \
&& rm -rf mpich*

#  Install libpng
RUN cd $DIR \
&& wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz \
&& tar xzvf libpng-1.2.50.tar.gz \
&& cd libpng-1.2.50 \
&& ./configure --prefix=$DIR/grib2 \
&& make -j $J \
&& make install \
&& cd $DIR \
&& rm -rf libpng*

# Install Jasper
RUN cd $DIR \
&& wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz \
&& tar xzvf jasper-1.900.1.tar.gz \
&& cd jasper-1.900.1 \
&& ./configure --prefix=$DIR/grib2 \
&& make -j $J \
&& make install \
&& cd $DIR \
&& rm -rf jasper*

# build WRF 
RUN cd $InWRF \
&& git clone --recurse-submodule https://github.com/wrf-model/WRF.git \
&& cd WRF \
&& (printf "34\n1\n" && cat) | ./configure
RUN cd $InWRF/WRF \ 
&& ./compile em_real -j $J >> /home/wrf.compile.log


# Build WPS
ENV WRF_DIR $InWRF/WRF
RUN cd $InWRF \
&& git clone https://github.com/wrf-model/WPS.git \
&& cd WPS \
&& (printf "1\n" && cat) | ./configure
RUN cd $InWRF/WPS \
&& ./compile >> /home/wps.compile.log
