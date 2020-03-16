
R_DECIM = 32
NUM_STAGE = 3
M_DELAY = 2
Bin = 8
Bout = 10
N_sensors = 2
N_bit_in  = 32
N_bit_out = 84

const_dict = {'N_bit_in': str (N_bit_in),'N_bit_out': str (N_bit_out),'N_sensors': str (N_sensors),
              'R_DECIM': str (R_DECIM),'NUM_STAGE': str (NUM_STAGE)}

entity_name = 'cicpy_decim'

io_dict = {'clk': '\t\t\t : in std_logic;\n',
           'reset': '\t\t : in std_logic;\n',
           'data_in': '\t\t : in std_logic_vector (N_bit_in-1 downto 0);\n',
           'enable': '\t\t : in std_logic;\n',
           'run': '\t\t\t : in std_logic;\n',
           'in_sop': '\t\t : in std_logic;\n',
           'in_eop': '\t\t : in std_logic;\n',
           'data_out': '\t : out std_logic_vector(N_bit_out-1 downto 0);\n',
           'ready': '\t\t : out std_logic;\n',
           'out_sop': '\t\t : out std_logic;\n',
           'out_eop': '\t\t : out std_logic\n'}

type_dict = {'sensors_arr_type': '\t is array (0 to N_sensors-1) of signed (N_bit_out-1 downto 0);\n',
             'integ_type': '\t\t\t is array (0 to N_sensors*NUM_STAGE-1) of signed (N_bit_out-1 downto 0);\n',
             'comb_type': '\t\t\t is array (0 to N_sensors*NUM_STAGE+N_sensors-1) of signed (N_bit_out-1 downto 0);\n'}

signal_dict = {'cnt': '\t\t\t\t: natural range 0 to R_DECIM := 1;\n',
               'cnt_delay': '\t\t: natural range 0 to NUM_STAGE-1 := 0;\n',
               'sensor_number': '\t: natural	:= 0;\n',
               'channel_integ': '\t: natural	:= 0;\n',
               'channel_comb': '\t\t: natural	:= 0;\n',
               'channel_out': '\t\t: natural	:= 0;\n',
               'integ': '''\t\t\t: std_logic	:= '0';\n''',
               'strob': '''\t\t\t: std_logic	:= '0';\n''',
               'comb': '''\t\t\t\t: std_logic	:= '0';\n''',
               'output': '''\t\t\t: std_logic	:= '0';\n''',
               'data_valid_sop': '''\t: std_logic	:= '0';\n''',
               'data_valid_eop': '''\t: std_logic	:= '0';\n''',
               'sensors_arr': '''\t\t: sensors_arr_type	:= (others => (others => '0'));\n''',
               'integrator': '''\t\t: integ_type		:= (others => (others => '0'));\n''',
               'delay1': '''\t\t\t: integ_type		:= (others => (others => '0'));\n''',
               'delay2': '''\t\t\t: integ_type		:= (others => (others => '0'));\n''',
               'combin': '''\t\t\t: comb_type			:= (others => (others => '0'));\n'''}
signal_dict['cnt'] = {'a':10, 'b':15}
for key in signal_dict:
    ff = signal_dict[key]['a']
    print(ff)
    
def binom(n, k):
    from math import factorial
    return factorial(n) // factorial(k) // factorial(n - k)

def Hogenauer (N,R,Bin,Bout,M=2):
    import math as m
    import numpy as np
    third_term = 0.5*m.log2(6/N)
    Bgrowth = m.ceil(m.log2((R*M)**N))
    Binternal = Bin + Bgrowth
    Variance = (2**(Bin-Bout+Bgrowth))**2/12
    Deviation = m.sqrt(Variance)
    k = (R*M-1)*N + 2 - 1
    for L in range (m.floor(k/(R*M))+1):
        h = (-1)**L*binom(N,L)*binom(N-2+k-R*M*L,k-R*M*L)
    return h, Binternal

# aaa, Binternal = Hogenauer(NUM_STAGE,R_DECIM,Bin,Bout)
aa = 5

def WriteVHDL ():

    with open ('cic_test.vhd', 'w') as file_vhdl:
        file_vhdl.write('--'+ entity_name + '\n')
        file_vhdl.write('\n')
        file_vhdl.write('library ieee;\n')
        file_vhdl.write('use ieee.std_logic_1164.all;\n')
        file_vhdl.write('use ieee.numeric_std.all;\n')
        file_vhdl.write('\n')
        file_vhdl.write('entity '+ entity_name +' is\n')
        file_vhdl.write('\t);\n')
        file_vhdl.write('\tport(\n')
        for key, value in io_dict.items():
            file_vhdl.write('\t\t'+(key)+(value))
        file_vhdl.write('\n')
        file_vhdl.write('\t);\n')
        file_vhdl.write('end '+ entity_name +';\n')
        file_vhdl.write('\n')
        file_vhdl.write('architecture behavior of '+ entity_name +' is\n')
        file_vhdl.write('\n')
        for key, value in const_dict.items():
            file_vhdl.write('constant '+ (key) + '\t\t :\tnatural := ' + (value) +';\n')
        file_vhdl.write('\n')
        for key, value in type_dict.items():
            file_vhdl.write('type ' + (key) + (value))
        file_vhdl.write('\n')
        for key, value in signal_dict.items():
            file_vhdl.write('signal ' + (key) + (value))
        file_vhdl.write('\n')
        file_vhdl.write('begin\n')
        file_vhdl.write('\tmain:process(clk,reset)\n')
        file_vhdl.write('\tbegin\n')
        file_vhdl.write('''\t\tif reset = '1' then\n''')
        file_vhdl.write(''' ''')
        file_vhdl.write(''' ''')
        file_vhdl.write(''' ''')
        file_vhdl.write('\t\telse\n')
        file_vhdl.write('\t\tend if;\n')
        file_vhdl.write('\tend process\n')
        file_vhdl.write('end behavior;')

WriteVHDL ()









