python3 accuracy.py --measure=accuracy --dataset_guess=files/names/names_tests/fifa.interguessed.csv --dataset_guess_row_name=0 --dataset_guess_row_gender=1 --dataset_test=files/names/names_tests/fifa.interguessed.csv --dataset_test_row_name=0 --dataset_test_row_gender=1 --api=damegender --dataset_test_row_gender_chars="female,male" > files/tests/accuracyfifafifa-$(date "+%Y-%m-%d").txt
if ! diff files/tests/accuracyfifafifa.txt files/tests/accuracyfifafifa-$(date "+%Y-%m-%d").txt
then
	echo -e  "accuracy fifa test is ${RED}failing${NC}"
else
	echo -e  "accuracy fifa test is ${GREEN}ok${NC}"
fi
