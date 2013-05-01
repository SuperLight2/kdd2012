data_folder=$1
original_training=training.txt
original_test=test.txt

python normalizer.py ${data_folder}/${original_training} ${data_folder}/${original_test} \
    -q ${data_folder}/queryid_tokensid.txt \
    -p ${data_folder}/purchasedkeywordid_tokensid.txt \
    -t ${data_folder}/titleid_tokensid.txt \
    -d ${data_folder}/descriptionid_tokensid.txt \
    -u ${data_folder}/userid_profile.txt \
    --result-training result.training.tsv.gz \
    --result-test result.test.tsv.gz

python dolbilka.py result.training.tsv.gz result.test.tsv.gz
