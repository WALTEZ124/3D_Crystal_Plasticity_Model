#!/bin/bash

# File for transfer to and from cluster local disk

#PBS -l nodes=1:ppn=12
#PBS -l walltime=20:00:00
#PBS -V
#PBS -l vmem=50gb
########PBS -l software=abaqus:12
#PBS -k eo

suffix=#suffix_value#

slip_suffix=#slip_suffix_value#

modes_plane=#modes_plane_value#

InitJobName=#InitJobName_value#

SecJobName=#SecJobName_value#



inp_folder=inp_files_${suffix}
in_folder=/u/tezeghdanti/3D_Model_Crystal_Plasticity/Yield_Surface_For_Slip_Planes/${inp_folder}/${slip_suffix}


Init_Job_Location=/data6/tezeghdanti/3D_Model_Crystal_Plasticity/Yield_Surface_For_Slip_Planes/${inp_folder}/${slip_suffix}

out_folder_gnode=/data2/tezeghdanti/3D_Model_Crystal_Plasticity/Yield_Surface_For_Slip_Planes/${inp_folder}/${slip_suffix}

cat $PBS_NODEFILE > ${in_folder}/node_${slip_suffix}_${modes_plane}_${PBS_JOBID}

#today_dir=$(date +%F)
temp_folder=/usrtmp/tezeghdanti/${inp_folder}

echo $(hostname)

mkdir -p ${temp_folder}

cp -r $in_folder  $temp_folder/

cd $temp_folder/${slip_suffix}

scp ${Init_Job_Location}/${InitJobName}.* .

####source ~zebulon/Z8.7/do_config.sh

source /u/gosselet/Z8.6/do_config.sh

Zmat cpus=8 memory=20gb -oj ${InitJobName} ${SecJobName}

rm ${InitJobName}.*

echo "#########################Resync to origin################"

mkdir -p $out_folder_gnode

rsync -rtv $temp_folder/${slip_suffix}/ $out_folder_gnode/

rm -r $temp_folder/${slip_suffix}

#scp -r $out_folder_gnode/${inp_folder} $ou_folder_local/
