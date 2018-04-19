#!/bin/bash

if [ $# -lt 2 ] ; then
  echo "ERROR: need 2 arguments!"
  echo "-> $0 zmat_file inp_file"
  echo "For instance:"
  echo " $0 zpreload.txt EL_Norm_hkl_010_uvw_100_KI_1_KII_0_KIII_0.inp"
  exit 1
fi

grep -A 4 '*MATERIAL' $1 > mat.txt

materials_location=`grep -n '** MATERIALS' $2 | awk -F ":" '{print $1}'`
#echo $materials_location
#read -n 1

insertion_line=$(($materials_location+2))
#echo $insertion_line
#read -n 1

sed -i "${insertion_line}i **here" $2
#grep -C 2 '**here' $2
#read -n 1

begin="**here"
end="*Material, name=Elastic-Rigid"
#echo $begin
#echo $end
#read -n 1

sed -i -e "/$begin/,/$end/{/$begin/{p; r mat.txt
	   }; /$end/p; d}" $2

sed -i '/**here/d' $2
