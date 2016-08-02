work=0
vacation=0
for i in {1..1000}; do
	output="`./behaviortest.py`"
	if [ -n "$(echo "$output" | grep -i 'Work')" ]; then
		work=$(($work + 1))
	fi
	if [ -n "$(echo "$output" | grep -i 'vacation')" ]; then
		vacation=$(($vacation + 1))
	fi
	echo $i
done

echo "Work: $work"
echo "Vacation: $vacation"
echo "Total: $(($work + $vacation))"
