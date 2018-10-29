# Problem
From the H1B visa application dataset, we'd like to comiple two lists of top 10 job occupations and top 10 states which have the most certified H1B visa applications. The lists contain the top occupations or states, number of certified applications, and percentage of certified cases for each occuptation or state based on the total number of certified cases.

# Approach
I coded in Python to tackle this problem. First I created two dictionaries, one for occupations and one for states, to keep track of the number of certified cases for each occupation or state. I also kept track of the number of total certified cases when scanning over the dataset. After the scanning was done, I converted the two dictionaries into lists of tuples, and sorted them, first by the nuumber of certified cases in descending order, then by the alphabetical order in cases of ties. Finally, I wrote the top ten entries to output files, during which I calculated the percentage of certified cases for each entry.

# Run
To run the program, edit the `run.sh` with appropriate arguments. The first agument passed to `top_tens.py` is the .csv filename of the H1B dataset; the second and third arguments are the output filenames (e.g. `top_10_occupations.txt` and `top_10_states.txt`) for top 10 occupations and states, respectively. Then enter the command `./run.sh` from the terminal.
All the output files should be saved into `output` directory.
