import os
import sys


def process_data(csv_file):
    """
    process_data() takes in csv file, and outputs two dictionaries that map job titles
    and work states to # of certified cases

    args:
    csv_file: .csv ";" delimited data file to te processed

    returns:
    occ_num_cert_app: a dictionary w/ keys as job titles, and values as number of occurrence of certified cases
    state_num_cert_app: a dictionary w/ keys as work states, and values as number of occurrence of certified cases
    total_app: total # of certified cases
    """

    if csv_file not in os.listdir("input"):
        raise ValueError('Specified data file not found in input directory.')
    else:
        filename = os.path.join("input", csv_file)

    # initialize two dict's storing occupation and work states as keys, and # of certification as values
    occ_num_cert_app = {}
    state_num_cert_app = {}

    with open(filename) as f:
        header = f.readline()

        # create mapping b/w header entries and column indices
        status_idx = -1
        job_title_idx = -1
        work_state_idx = []
        idx = 0
        for field in header.strip().split(';'):
            field.upper()
            if 'STATUS' in field:
                if status_idx == -1:
                    status_idx = idx
                else:
                    print('duplicate status')

            if 'SOC' in field and 'NAME' in field:
                if job_title_idx == -1:
                    job_title_idx = idx
                else:
                    print('duplicate job title')

            if 'WORK' in field and 'STATE' in field:
                work_state_idx.append(idx)

            idx += 1

        # scan over data one at a time; insert certified cases into dictionaries
        total_app = 0
        for line in f:
            entry = line.split(';')
            if entry[status_idx].strip('" ').upper() == 'CERTIFIED':
                total_app += 1
                # first, update top_occupation dict
                job_title = entry[job_title_idx].strip('" ').upper()
                if job_title not in occ_num_cert_app.keys():
                    occ_num_cert_app[job_title] = 1
                else:
                    occ_num_cert_app[job_title] += 1

                # second, update top_state dict
                for idx in work_state_idx:
                    work_state = entry[idx].strip('" ').upper()
                    if len(work_state) == 2:
                        if work_state not in state_num_cert_app.keys():
                            state_num_cert_app[work_state] = 1
                        else:
                            state_num_cert_app[work_state] += 1

    f.close()

    return occ_num_cert_app, state_num_cert_app, total_app


def sort_data(occ_num_cert_app, state_num_cert_app, verbose=True):
    """
    sort_data() sorts the output dict's from process_data() into appropriate orders, and returns lists of tuples.

    args:
    occ_num_cert_app, state_num_cert_app: dict outputs from process_data()
    verbose: True if print top lists to terminal; False if not

    returns:
    occ_list, state_list: sorted lists based on # of certified cases first (desc) and alphabetical order on job titles
    or work states (asc). Each entry is a tuple of (job_title, # cases) or (work_state, # cases).
    """
    # sort the top occupation list
    occ_num_total = 0
    occ_list = []
    for k, v in occ_num_cert_app.items():
        occ_num_total += v
        occ_list.append((k, v))
    occ_list.sort(key=lambda tup: (-tup[1], tup[0]))

    # sort the top state list
    state_num_total = 0
    state_list = []
    for k, v in state_num_cert_app.items():
        state_num_total += v
        state_list.append((k, v))
    state_list.sort(key=lambda tup: (-tup[1], tup[0]))

    if verbose:
        if len(occ_list) > 10:
            print(occ_list[0:10])
        else:
            print(occ_list)

        if len(state_list) > 10:
            print(state_list[0:10])
        else:
            print(state_list)

    return occ_list, state_list


def write_to_file(occ_list, state_list, total_num, occ_filename, state_filename):
    """
        write_to_file() writes the top ten job titles and states to specified .txt.files according to specified format.

        args:
        occ_list, state_list: sorted lists of tuples from sort_data()
        total_num: total number of certified cases from process_data()
        occ_filename, state_filename: specified output filenames
        """

    with open('output/' + occ_filename, 'w') as f:
        f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for i in range(min(10, len(occ_list))):
            per = 100.0 * occ_list[i][1] / total_num
            f.write(occ_list[i][0] + ';' + str(occ_list[i][1]) + ';' + "%0.1f" % (per,) + '%\n')

    with open('output/' + state_filename, 'w') as f:
        f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for i in range(min(10, len(state_list))):
            per = 100.0 * state_list[i][1] / total_num
            f.write(state_list[i][0] + ';' + str(state_list[i][1]) + ';' + "%0.1f" % (per,) + '%\n')


# main file #
csv_in = sys.argv[1]
occ_out = sys.argv[2]
state_out = sys.argv[3]

occ_map, state_map, total_cert = process_data(csv_in)

occ_sorted_list, state_sorted_list = sort_data(occ_map, state_map, verbose=True)

write_to_file(occ_sorted_list, state_sorted_list, total_cert, occ_out, state_out)
