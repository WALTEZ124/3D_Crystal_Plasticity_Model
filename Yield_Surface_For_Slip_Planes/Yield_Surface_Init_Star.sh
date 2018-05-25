#!/bin/bash

# File for transfer to and from cluster local disk

#PBS -l nodes=1:ppn=12
#PBS -l walltime=20:00:00
#PBS -V
#PBS -l vmem=50gb
########PBS -l software=abaqus:12
#PBS -k eo


hkl=(#hkl_value#)
uvw=(#uvw_value#)

slip_suffix=#slip_suffix_value#
modes_plane=#modes_plane_value#

suffix=${hkl[0]}${hkl[1]}${hkl[2]}_${uvw[0]}${uvw[1]}${uvw[2]}

inp_folder=inp_files_${suffix}
in_folder=/u/tezeghdanti/3D_Model_Crystal_Plasticity/Yield_Surface_For_Slip_Planes/${inp_folder}/${slip_suffix}

cat $PBS_NODEFILE > ${in_folder}/node_${slip_suffix}_${modes_plane}_${PBS_JOBID}

out_folder_gnode=/data6/tezeghdanti/3D_Model_Crystal_Plasticity/Yield_Surface_For_Slip_Planes/${inp_folder}/${slip_suffix}

#today_dir=$(date +%F)
temp_folder=/usrtmp/tezeghdanti/${inp_folder}

echo $(hostname)

mkdir -p ${temp_folder}

cp -r $in_folder  $temp_folder/

cd $temp_folder/${slip_suffix}

####source ~zebulon/Z8.7/do_config.sh

JobName=$(sed -n 1p Star_init_job_details_${modes_plane}.txt)

NewJobName="${JobName}_${slip_suffix}.inp"

source /u/gosselet/Z8.6/do_config.sh

Zmat cpus=8 memory=32gb ${NewJobName}

echo "#########################Resync to origin################"

mkdir -p $out_folder_gnode

rsync -rtv $temp_folder/${slip_suffix}/ $out_folder_gnode/

rm -r $temp_folder/${slip_suffix}

#scp -r $out_folder_gnode/${inp_folder} $ou_folder_local/
