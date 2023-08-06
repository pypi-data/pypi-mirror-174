#!/bin/bash

#https://stackoverflow.com/a/14203146
POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -id)
      ID="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--rootpath)
      ROOTPATH="$2"
      shift # past argument
      shift # past value
      ;;
    --data)
      DATA="$2"
      shift # past argument
      shift # past value
      ;;
    --labels)
      LABELS="$2"
      shift # past argument
      shift # past value
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

echo "ID  = ${ID}"
echo "ROOTPATH  = ${ROOTPATH}"
echo "DATA  = ${DATA}"
echo "LABELS  = ${LABELS}"
#cd /dls/science/users/jig77871/projects/volume-segmantics-vsui
#module load python/3.9
#conda activate /dls/science/users/jig77871/volseg-conda
#python3 volume_segmantics/scripts/train_2d_model.py --vsui_id ${ID} --data_dir ${ROOTPATH} --data ${DATA} --labels ${LABELS}
module load python/3.9
module load cuda/10.2
conda activate /dls/science/users/jig77871/unet-gui/env
model-train-2d --vsui_id ${ID} --data_dir ${ROOTPATH} --data ${DATA} --labels ${LABELS}