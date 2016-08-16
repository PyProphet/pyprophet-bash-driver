#!/bin/bash

DATA_FOLDER={data_folder}
WORK_FOLDER={work_folder}
RESULT_FOLDER={result_folder}

JC={job_count}
JSL={job_slot_limit}

GROUP=$RESULT_FOLDER

MSG_FOLDER={work_folder}

pyprophet-cli prepare --data-folder $DATA_FOLDER \
                      --data-filename-pattern "{data_filename_pattern}" \
                      --work-folder $WORK_FOLDER \
                      {extra_args_prepare} &> $MSG_FOLDER/prepare_out

pyprophet-cli subsample --data-folder $DATA_FOLDER \
                        --data-filename-pattern "{data_filename_pattern}" \
                        --work-folder $WORK_FOLDER \
                        --job-number 1 \
                        --job-count 1 \
                        --sample-factor {sample_factor} \
                        --local-folder $WORK_FOLDER \
                        --chunk-size 1000000 \
                        {extra_args_subsample} &> $MSG_FOLDER/subsample_out

pyprophet-cli learn --work-folder $WORK_FOLDER \
                    --ignore-invalid-scores \
                    {extra_args_learn} &> $MSG_FOLDER/learn_out

pyprophet-cli apply_weights --data-folder $DATA_FOLDER \
                            --data-filename-pattern "{data_filename_pattern}" \
                            --work-folder $WORK_FOLDER \
                            --job-number 1 \
                            --job-count 1 \
                            --local-folder $WORK_FOLDER \
                            --chunk-size 1000000 \
                            {extra_args_apply_weights} &> $MSG_FOLDER/apply_weights_out

pyprophet-cli score --data-folder $DATA_FOLDER \
                    --data-filename-pattern "{data_filename_pattern}" \
                    --work-folder $WORK_FOLDER \
                    --statistics-mode {statistics_mode} \
                    --job-number 1 \
                    --job-count 1 \
                    --local-folder $WORK_FOLDER \
                    --overwrite-results \
                    --lambda {lambda_} \
                    --result-folder $RESULT_FOLDER \
                    --chunk-size 1000000 \
                    {extra_args_score} &> $MSG_FOLDER/scorer_out

echo "workflow finished" &> $MSG_FOLDER/final_out
