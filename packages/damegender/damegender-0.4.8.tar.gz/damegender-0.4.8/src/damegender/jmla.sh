#!/bin/sh

python3 accuracy.py --api=damegender --measure=accuracy --dataset_guess=files/names/names_tests/gender_JMLA.min.interguessed.csv --dataset_guess_row_name=0 --dataset_guess_row_gender=1 --dataset_test=files/names/names_tests/gender_JMLA.min.dta.csv --dataset_test_row_name=1 --dataset_test_row_gender=2 --dataset_test_row_gender_chars="female,male" > files/tests/accuracygender_JMLA-$(date "+%Y-%m-%d").txt
if ! diff files/tests/accuracygender_JMLA.txt files/tests/accuracygender_JMLA-$(date "+%Y-%m-%d").txt >/dev/null 2>&1
then
	echo -e  "accuracy JMLA dataset test is ${RED}failing${NC}"
else
	echo -e  "accuracy JMLA dataset test is ${GREEN}ok${NC}"
fi
