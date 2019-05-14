#! /bin/sh

python extract_embeddings.py \
	--dataset dataset \
	--detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7

