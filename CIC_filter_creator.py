###########################################################################################################
NUM_STAGE = 6  # 6
R_DECIM = 200  # 200
N_bit_in = 64  # 32
N_bit_out = 64  # 32
M_DELAY = 2
N_sensors = 48
Hogenauer_pruning = True

# NUM_STAGE = 3  # 6
# R_DECIM = 32  # 200
# N_bit_in = 8  # 32
# N_bit_out = 10  # 32
#
# NUM_STAGE = 6  # 6
# R_DECIM = 200  # 200
# N_bit_in = 64  # 32
# N_bit_out = 64  # 32

##########################################################################################################
const_dict = {'N_bit_in': str(N_bit_in), 'N_bit_out': str(N_bit_out), 'N_sensors': str(N_sensors),
              'R_DECIM': str(R_DECIM), 'NUM_STAGE': str(NUM_STAGE), 'Hogenauer_pruning': str(Hogenauer_pruning)}

entity_name = 'cicpy_decim'

io_dict = {'clk': '\t\t\t : in std_logic;\n',
           'reset': '\t\t : in std_logic;\n',
           'data_in': '\t\t : in std_logic_vector(' + str(N_bit_in - 1) + ' downto 0);\n',
           'enable': '\t\t : in std_logic;\n',
           'run': '\t\t\t : in std_logic;\n',
           'in_sop': '\t\t : in std_logic;\n',
           'in_eop': '\t\t : in std_logic;\n',
           'data_out': '\t : out std_logic_vector(' + str(N_bit_out - 1) + ' downto 0);\n',
           'ready': '\t\t : out std_logic;\n',
           'out_sop': '\t\t : out std_logic;\n',
           'out_eop': '\t\t : out std_logic\n'}

signal_dict = {'cnt\t\t\t': {'type': '\t: natural range 0 to ' + str(R_DECIM) + ' := ', 'value': '1'},
               'cnt_delay\t': {'type': '\t: natural range 0 to ' + str(NUM_STAGE - 1) + '  := ', 'value': '0'},
               'sensor_number': {'type': '\t: natural range 0 to ' + str(N_sensors - 1) + ' := ', 'value': '0'},
               'channel_integ': {'type': '\t: natural range 0 to ' + str(N_sensors - 1) + ' := ', 'value': '0'},
               'channel_comb': {'type': '\t\t: natural range 0 to ' + str(N_sensors - 1) + ' := ', 'value': '0'},
               'channel_out\t': {'type': '\t: natural range 0 to ' + str(N_sensors - 1) + ' := ', 'value': '0'},
               'integ\t\t': {'type': '''\t: std_logic	:= ''', 'value': ''' '0' '''},
               'strob\t\t': {'type': '''\t: std_logic	:= ''', 'value': ''' '0' '''},
               'comb\t\t': {'type': '''\t\t: std_logic	:= ''', 'value': ''' '0' '''},
               'output\t\t': {'type': '''\t: std_logic	:= ''', 'value': ''' '0' '''},
               'data_valid_sop': {'type': '''\t: std_logic	:= ''', 'value': ''' '0' '''},
               'data_valid_eop': {'type': '''\t: std_logic	:= ''', 'value': ''' '0' '''},
               'sensors_arr\t': {'type': '''\t: sensors_arr_type	:=''',
                                 'value': ''' (others => (others => '0'))'''}}


def binom(n, k):
    from math import factorial
    return factorial(n) // factorial(k) // factorial(n - k)


def hogenauer():
    import math as m
    import numpy as np
    third_term = 0.5 * m.log2(6 / NUM_STAGE)
    bgrowth = m.ceil(m.log2((R_DECIM * M_DELAY) ** NUM_STAGE))
    bmax = N_bit_in + bgrowth
    variance = (2 ** (bmax - N_bit_out)) ** 2 / 12
    deviation = m.sqrt(variance)

    f = np.zeros(NUM_STAGE * 2)
    bits_discarded_high = np.zeros(NUM_STAGE * 2 + 1, dtype=np.int64)
    f_binom = np.array([2, 6, 20, 70, 252, 924, 3432, 12870], dtype=np.float64)

    for i in range(1, NUM_STAGE + 1):
        h = np.zeros((R_DECIM * M_DELAY - 1) * NUM_STAGE + i - 1)
        for k in range((R_DECIM * M_DELAY - 1) * NUM_STAGE + i - 1):
            for L in range(m.floor(k / (R_DECIM * M_DELAY)) + 1):
                change = (-1) ** L * binom(NUM_STAGE, L) * binom(NUM_STAGE - i + k - R_DECIM * M_DELAY * L,
                                                                 k - R_DECIM * M_DELAY * L)
                h[k] = h[k] + change
        f[i - 1] = m.sqrt(m.fsum(h ** 2))
    for i in range(NUM_STAGE + 1, 2 * NUM_STAGE + 1):
        f[i - 1] = m.sqrt(f_binom[2 * NUM_STAGE + 1 - i - 1])
    f = np.append(f, 1)
    bits_truncation = np.int64(np.floor(m.log2(deviation) + third_term - np.log2(f)))
    bits_truncation[2 * NUM_STAGE] = bmax - N_bit_out
    bits_discarded_low = np.diff(bits_truncation)
    bits_discarded_low = np.insert(bits_discarded_low, 0, bits_truncation[0])

    bits_discarded_high[0] = bmax
    for i in range(2 * NUM_STAGE):
        bits_discarded_high[i + 1] = bits_discarded_high[i] - bits_discarded_low[i]

    return list(bits_discarded_high - 1), list(bits_discarded_low), bmax


if Hogenauer_pruning:
    Bits_discarded_high, Bits_discarded_low, Bmax = hogenauer()

    type_dict = {'sensors_arr_type': ' is array (0 to ' + str(N_sensors - 1) + ') of signed (' + str(
        Bmax - 1) + ' downto 0);\n'}

    for j in range(len(Bits_discarded_high)):
        type_dict['array_' + str(Bits_discarded_high[j] + 1) + '_type'] = '\t is array (0 to ' + str(
            N_sensors - 1) + ') of signed (' + str(
            Bits_discarded_high[j]) + ' downto 0);\n'

    for j in range(NUM_STAGE):
        signal_dict['integrator' + str(j) + '\t'] = {
            'type': '\t: array_' + str(Bits_discarded_high[j + 1] + 1) + '_type	:=',
            'value': ''' (others => (others => '0'))'''}
    for j in range(NUM_STAGE):
        signal_dict['c' + str(j) + 'delay1\t'] = {
            'type': '\t\t: array_' + str(Bits_discarded_high[NUM_STAGE + j + 1] + 1) + '_type	:=',
            'value': ''' (others => (others => '0'))'''}
    for j in range(NUM_STAGE):
        signal_dict['c' + str(j) + 'delay2\t'] = {
            'type': '\t\t: array_' + str(Bits_discarded_high[NUM_STAGE + j + 1] + 1) + '_type	:=',
            'value': ''' (others => (others => '0'))'''}
    signal_dict['combin0\t\t'] = {
        'type': '\t: array_' + str(Bits_discarded_high[NUM_STAGE + 1] + 1) + '_type	:=',
        'value': ''' (others => (others => '0'))'''}
    for j in range(1, NUM_STAGE + 1):
        signal_dict['combin' + str(j) + '\t\t'] = {
            'type': '\t: array_' + str(Bits_discarded_high[NUM_STAGE + j] + 1) + '_type	:=',
            'value': ''' (others => (others => '0'))'''}
    integ_dict = {
        'integrator0(channel_integ)': {'value': '\t\t<= integrator0(channel_integ) + sensors_arr(channel_integ)',
                                       'pruning': '(' + str(Bits_discarded_high[0]) + ' downto ' + str(
                                           Bits_discarded_low[0]) + ')'}}
    comb_dict = {'combin0(channel_comb)': {'value_comb': '\t\t<= integrator' + str(NUM_STAGE - 1) + '(channel_comb)',
                                           'value_delay': '',
                                           'pruning': '(' + str(Bits_discarded_high[NUM_STAGE]) + ' downto ' + str(
                                               Bits_discarded_low[NUM_STAGE]) + ')'},
                 'combin1(channel_comb)': {'value_comb': '\t\t<= combin0(channel_comb)- c0delay2(channel_comb)',
                                           'value_delay': '',
                                           'pruning': ''}}
    delay1_dict = {'c' + str(j) + 'delay1(channel_comb)': {'value': '\t\t<= combin' + str(j) + '(channel_comb)',
                                                           'pruning': '(' + str(
                                                               Bits_discarded_high[NUM_STAGE + j]) + ' downto ' + str(
                                                               Bits_discarded_low[NUM_STAGE + j]) + ')'} for j in
                   range(1, NUM_STAGE)}
    delay1_dict['c0delay1(channel_comb)'] = {'value': '\t\t<= combin0(channel_comb)',
                                             'pruning': ''}

    delay2_dict = {'c' + str(j) + 'delay2(channel_comb)': '\t\t<= c' + str(j) + 'delay1(channel_comb)' for j in
                   range(NUM_STAGE)}

    for j in range(1, NUM_STAGE):
        integ_dict['integrator' + str(j) + '(channel_integ)'] = {'value': '\t\t<= integrator' + str(
            j) + '(channel_integ) + integrator' + str(j - 1) + '(channel_integ)',
                                                                 'pruning': '(' + str(
                                                                     Bits_discarded_high[j]) + ' downto ' + str(
                                                                     Bits_discarded_low[j]) + ')'}
    for j in range(1, NUM_STAGE):
        comb_dict['combin' + str(j + 1) + '(channel_comb)'] = {
            'value_comb': '\t\t<= combin' + str(j) + '(channel_comb)', 'value_delay': ' - c' + str(
                j) + 'delay2(channel_comb)',
            'pruning': '(' + str(Bits_discarded_high[NUM_STAGE + j]) + ' downto ' + str(
                Bits_discarded_low[NUM_STAGE + j]) + ')'}


else:
    for j in range(NUM_STAGE):
        signal_dict['integrator' + str(j)] = {'type': '''\t\t: sensors_arr_type	:=''',
                                              'value': ''' (others => (others => '0'))'''}
    for j in range(NUM_STAGE):
        signal_dict['c' + str(j) + 'delay1'] = {'type': '''\t\t: sensors_arr_type	:=''',
                                                'value': ''' (others => (others => '0'))'''}
    for j in range(NUM_STAGE):
        signal_dict['c' + str(j) + 'delay2'] = {'type': '''\t\t: sensors_arr_type	:=''',
                                                'value': ''' (others => (others => '0'))'''}
    for j in range(NUM_STAGE + 1):
        signal_dict['combin' + str(j)] = {'type': '''\t\t: sensors_arr_type	:=''',
                                          'value': ''' (others => (others => '0'))'''}

    type_dict = {'sensors_arr_type': '\t is array (0 to ' + str(N_sensors - 1) + ') of signed (' + str(
        N_bit_out - 1) + ' downto 0);\n'}
    integ_dict = {
        'integrator0(channel_integ)': {'value': '\t\t<= integrator0(channel_integ) + sensors_arr(channel_integ)',
                                       'pruning': ''}}
    comb_dict = {'combin0(channel_comb)': {'value_comb': '\t\t<= integrator' + str(NUM_STAGE - 1) + '(channel_comb)',
                                           'value_delay': '',
                                           'pruning': ''},
                 'combin1(channel_comb)': {'value_comb': '\t\t<= combin0(channel_comb)- c0delay2(channel_comb)',
                                           'value_delay': '',
                                           'pruning': ''}}
    delay1_dict = {'c' + str(j) + 'delay1(channel_comb)': {'value': '\t\t<= combin' + str(j) + '(channel_comb)',
                                                           'pruning': ''} for j in
                   range(1, NUM_STAGE)}
    delay1_dict['c0delay1(channel_comb)'] = {'value': '\t\t<= combin0(channel_comb)',
                                             'pruning': ''}

    delay2_dict = {'c' + str(j) + 'delay2(channel_comb)': '\t\t<= c' + str(j) + 'delay1(channel_comb)' for j in
                   range(NUM_STAGE)}

    for j in range(1, NUM_STAGE):
        integ_dict['integrator' + str(j) + '(channel_integ)'] = {'value': '\t\t<= integrator' + str(
            j) + '(channel_integ) + integrator' + str(j - 1) + '(channel_integ)',
                                                                 'pruning': ''}
    for j in range(1, NUM_STAGE):
        comb_dict['combin' + str(j + 1) + '(channel_comb)'] = {
            'value_comb': '\t\t<= combin' + str(j) + '(channel_comb)', 'value_delay': ' - c' + str(
                j) + 'delay2(channel_comb)',
            'pruning': ''}


def write_vhdl():
    file_name = 'cic_dec_st_' + str(NUM_STAGE) + '_R_' + str(R_DECIM) + '_sen_' + str(
        N_sensors) + '_in_' + str(N_bit_in) + '_out_' + str(N_bit_out) + '.vhd'
    with open(file_name, 'w') as file_vhdl:
        file_vhdl.write('--' + entity_name + '\n')
        file_vhdl.write('\n')
        for key, value in const_dict.items():
            file_vhdl.write('-- ' + key + ' = ' + value + '\n')
        file_vhdl.write('\n')
        file_vhdl.write('\n')
        file_vhdl.write('library ieee;\n')
        file_vhdl.write('use ieee.std_logic_1164.all;\n')
        file_vhdl.write('use ieee.numeric_std.all;\n')
        file_vhdl.write('\n')
        file_vhdl.write('entity ' + entity_name + ' is\n')
        file_vhdl.write('\tport(\n')
        for key, value in io_dict.items():
            file_vhdl.write('\t\t' + key + value)
        file_vhdl.write('\n')
        file_vhdl.write('\t);\n')
        file_vhdl.write('end ' + entity_name + ';\n')
        file_vhdl.write('\n')
        file_vhdl.write('architecture behavior of ' + entity_name + ' is\n')
        file_vhdl.write('\n')
        for key, value in type_dict.items():
            file_vhdl.write('type ' + key + value)
        file_vhdl.write('\n')
        for key in signal_dict:
            type_of_signal = signal_dict[key]['type']
            value = signal_dict[key]['value']
            file_vhdl.write('signal ' + key + type_of_signal + value + ';\n')
        file_vhdl.write('\n')
        file_vhdl.write('begin\n')
        file_vhdl.write('\tmain:process(clk,reset)\n')
        file_vhdl.write('\tbegin\n')
        file_vhdl.write('''\t\tif reset = '1' then\n''')
        file_vhdl.write('\n')
        file_vhdl.write('''\t\t\tready \t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\tout_sop \t\t<= '0';\n''')
        file_vhdl.write('''\t\t\tout_eop \t\t<= '0';\n''')
        file_vhdl.write('''\t\t\tdata_out \t\t<= (others => '0');\n''')
        file_vhdl.write('\n')
        for key in signal_dict:
            value = signal_dict[key]['value']
            file_vhdl.write('\t\t\t' + key + '\t\t<=' + value + ';\n')
        file_vhdl.write('\n')
        file_vhdl.write('\t\telsif (rising_edge(clk)) then\n')
        file_vhdl.write('\n')
        file_vhdl.write('''\t\t\tif enable = '0' then\n''')
        file_vhdl.write('\t\t\t\tready 	\t\t\t<= run;\n')
        file_vhdl.write('''\t\t\t\tout_sop \t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\tout_eop \t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\tdata_out \t\t\t<= std_logic_vector(resize(signed(data_in),' + str(N_bit_out) + '));\n')
        file_vhdl.write('\n')
        for key in signal_dict:
            value = signal_dict[key]['value']
            file_vhdl.write('\t\t\t\t' + key + '\t\t<=' + value + ';\n')
        file_vhdl.write('\n')
        file_vhdl.write('\t\t\telse\n')
        file_vhdl.write('''\t\t\t\tif run = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\tif in_sop = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\t\tdata_valid_sop	\t\t\t\t<= '1';\n''')
        file_vhdl.write('''\t\t\t\t\t\tdata_valid_eop	\t\t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\t\tsensor_number	\t\t\t\t<= sensor_number + 1;\n''')
        if Hogenauer_pruning:
            file_vhdl.write(
                '\t\t\t\t\t\tsensors_arr(sensor_number) \t\t<= resize (signed (data_in),' + str(Bmax) + ');\n')
        else:
            file_vhdl.write(
                '\t\t\t\t\t\tsensors_arr(sensor_number) \t\t<= resize (signed (data_in),' + str(N_bit_out) + ');\n')
        file_vhdl.write('''\t\t\t\t\telsif in_eop = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\t\tdata_valid_eop	\t\t\t\t<= '1';\n''')
        file_vhdl.write('''\t\t\t\t\t\tsensor_number	\t\t\t\t<= 0;\n''')
        if Hogenauer_pruning:
            file_vhdl.write(
                '\t\t\t\t\t\tsensors_arr(sensor_number) \t\t<= resize (signed (data_in),' + str(Bmax) + ');\n')
        else:
            file_vhdl.write(
                '\t\t\t\t\t\tsensors_arr(sensor_number) \t\t<= resize (signed (data_in),' + str(N_bit_out) + ');\n')
        file_vhdl.write('\t\t\t\t\telse\n')
        file_vhdl.write('''\t\t\t\t\t\tif (data_valid_sop = '1') and (data_valid_eop = '0') then\n''')
        file_vhdl.write('\t\t\t\t\t\t\tsensor_number\t\t\t\t<= sensor_number + 1;\n')
        if Hogenauer_pruning:
            file_vhdl.write(
                '\t\t\t\t\t\t\tsensors_arr(sensor_number)\t<= resize (signed (data_in),' + str(Bmax) + ');\n')
        else:
            file_vhdl.write(
                '\t\t\t\t\t\t\tsensors_arr(sensor_number)\t<= resize (signed (data_in),' + str(N_bit_out) + ');\n')
        file_vhdl.write('\t\t\t\t\t\telse\n')
        file_vhdl.write('\t\t\t\t\t\t\tsensor_number \t\t\t\t<= 0;\n')
        file_vhdl.write('\t\t\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\t\telse\n')
        file_vhdl.write('\t\t\t\t\tsensor_number \t\t\t<= 0;\n')
        file_vhdl.write('''\t\t\t\t\tdata_valid_sop\t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\tdata_valid_eop\t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\tend if;\n')
        file_vhdl.write('''\t\t\t\tif (data_valid_sop = '1') and (data_valid_eop = '1') then\n''')
        file_vhdl.write('''\t\t\t\t\tinteg\t\t\t\t\t<= '1';\n''')
        file_vhdl.write('''\t\t\t\t\tdata_valid_sop\t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\tdata_valid_eop\t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\tend if;\n')
        file_vhdl.write('\n')
        file_vhdl.write('''\t\t\t\tif integ = '1' then\n''')
        for key in integ_dict:
            value = integ_dict[key]['value']
            pruning = integ_dict[key]['pruning']
            file_vhdl.write('\t\t\t\t\t' + key + '\t\t' + value + pruning + ';\n')
        file_vhdl.write('\t\t\t\t\tif channel_integ = ' + str(N_sensors - 1) + ' then\n')
        file_vhdl.write('\t\t\t\t\t\tchannel_integ 	\t<= 0;\n')
        file_vhdl.write('''\t\t\t\t\t\tinteg 	\t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\t\t\tif cnt = ' + str(R_DECIM - 1) + ' then\n')
        file_vhdl.write('''\t\t\t\t\t\t\tstrob 	\t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\t\t\t\tcnt 	\t\t\t<= 0;\n')
        file_vhdl.write('\t\t\t\t\t\telsif cnt = ' + str(NUM_STAGE - 1) + ' then\n')
        file_vhdl.write('''\t\t\t\t\t\t\tstrob 	\t\t\t<= '1';\n''')
        file_vhdl.write('\t\t\t\t\t\t\tcnt 	\t\t\t<= cnt + 1;\n')
        file_vhdl.write('\t\t\t\t\t\telse\n')
        file_vhdl.write('''\t\t\t\t\t\t\tstrob 	\t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\t\t\t\tcnt 	\t\t\t<= cnt + 1;\n')
        file_vhdl.write('\t\t\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\t\t\telse\n')
        file_vhdl.write('\t\t\t\t\t\tchannel_integ 	\t<= channel_integ + 1;\n')
        file_vhdl.write('\t\t\t\t\tend if;\n')
        file_vhdl.write('''\t\t\t\t\tif strob = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\t\tcomb \t\t\t\t<= '1';\n''')
        file_vhdl.write('\t\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\t\tend if;\n')
        file_vhdl.write('\n')
        file_vhdl.write('''\t\t\t\tif comb = '1' then\n''')
        for key in delay1_dict:
            value = delay1_dict[key]['value']
            pruning = delay1_dict[key]['pruning']
            file_vhdl.write('\t\t\t\t\t' + key + '\t\t' + value + pruning + ';\n')
        file_vhdl.write('\n')
        for key, value in delay2_dict.items():
            file_vhdl.write('\t\t\t\t\t' + key + '\t\t' + value + ';\n')
        file_vhdl.write('\n')
        for key in comb_dict:
            value_comb = comb_dict[key]['value_comb']
            value_delay = comb_dict[key]['value_delay']
            pruning = comb_dict[key]['pruning']
            file_vhdl.write('\t\t\t\t\t' + key + '\t\t' + value_comb + pruning + value_delay + ';\n')
        file_vhdl.write('\n')
        file_vhdl.write('\t\t\t\t\tif channel_comb = ' + str(N_sensors - 1) + ' then\n')
        file_vhdl.write('\t\t\t\t\t\tchannel_comb 	\t<= 0;\n')
        file_vhdl.write('''\t\t\t\t\t\tcomb 	\t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\t\t\tif cnt_delay = ' + str(NUM_STAGE - 1) + ' then\n')
        file_vhdl.write('''\t\t\t\t\t\t\toutput 	\t\t\t<= '1';\n''')
        file_vhdl.write('\t\t\t\t\t\telse\n')
        file_vhdl.write('\t\t\t\t\t\t\tcnt_delay 	\t\t<= cnt_delay + 1;\n')
        file_vhdl.write('\t\t\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\t\t\telse\n')
        file_vhdl.write('\t\t\t\t\t\tchannel_comb \t\t\t<= channel_comb + 1;\n')
        file_vhdl.write('\t\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\t\tend if;\n')
        file_vhdl.write('\n')
        file_vhdl.write('''\t\t\t\tif output = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\tready \t\t\t\t\t<= '1';\n''')
        if Hogenauer_pruning:
            file_vhdl.write(
                '\t\t\t\t\tdata_out \t\t\t\t<= std_logic_vector(combin' + str(
                    NUM_STAGE) + '(channel_out)(' + str(
                    Bits_discarded_high[2 * NUM_STAGE]) + ' downto ' + str(
                    Bits_discarded_low[2 * NUM_STAGE]) + '));\n')
        else:
            file_vhdl.write(
                '\t\t\t\t\tdata_out \t\t\t\t<= std_logic_vector(combin' + str(NUM_STAGE) + '(channel_out));\n')
        file_vhdl.write('''\t\t\t\t\tif channel_out = 0 then\n''')
        file_vhdl.write('''\t\t\t\t\t\tout_sop \t\t\t<= '1';\n''')
        file_vhdl.write('''\t\t\t\t\t\tout_eop \t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\t\t\tchannel_out \t\t<= channel_out + 1;\n')
        file_vhdl.write('\t\t\t\t\telsif channel_out = ' + str(N_sensors - 1) + ' then\n')
        file_vhdl.write('''\t\t\t\t\t\tout_sop \t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\t\tout_eop \t\t\t<= '1';\n''')
        file_vhdl.write('''\t\t\t\t\t\toutput \t\t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\t\t\tchannel_out \t\t<= 0;\n')
        file_vhdl.write('\t\t\t\t\telse\n')
        file_vhdl.write('''\t\t\t\t\t\tout_sop \t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\t\tout_eop \t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\t\t\tchannel_out \t\t<= channel_out + 1;\n')
        file_vhdl.write('\t\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\t\telse\n')
        file_vhdl.write('''\t\t\t\t\tready \t\t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\tout_sop \t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\tout_eop \t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\tend if;\n')
        file_vhdl.write('\t\t\tend if;\n')
        file_vhdl.write('\t\tend if;\n')
        file_vhdl.write('\tend process;\n')
        file_vhdl.write('end behavior;')


write_vhdl()
