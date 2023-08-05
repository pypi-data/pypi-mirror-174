python3 percentage2names.py 50 --outcsv=files/tests/50-$(date "+%Y-%m-%d").txt

if ! diff files/tests/50.txt files/tests/50-$(date "+%Y-%m-%d").txt >/dev/null 2>&1
then
	echo -e  "percentage2names test is ${RED}failing${NC}"
else
	echo -e  "percentage2names test is ${GREEN}ok${NC}"
fi

python3 percentage2names.py 40 --percentage_until=70 --outcsv=files/tests/40-70-$(date "+%Y-%m-%d").txt

if ! diff files/tests/40-70.txt files/tests/40-70-$(date "+%Y-%m-%d").txt >/dev/null 2>&1
then
	echo -e  "percentage2names test is ${RED}failing${NC}"
else
	echo -e  "percentage2names test is ${GREEN}ok${NC}"
fi

