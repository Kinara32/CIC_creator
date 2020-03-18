
R_DECIM = 200
NUM_STAGE = 6
M_DELAY = 2
Bin = 8
Bout = 10
N_sensors = 3
N_bit_in  = 32
N_bit_out = 84

const_dict = {'N_bit_in': str (N_bit_in),'N_bit_out': str (N_bit_out),'N_sensors': str (N_sensors),
              'R_DECIM': str (R_DECIM),'NUM_STAGE': str (NUM_STAGE)}

entity_name = 'cicpy_decim'

io_dict = {'clk': '\t\t\t : in std_logic;\n',
           'reset': '\t\t : in std_logic;\n',
           'data_in': '\t\t : in std_logic_vector ('+str (N_bit_in-1)+' downto 0);\n',
           'enable': '\t\t : in std_logic;\n',
           'run': '\t\t\t : in std_logic;\n',
           'in_sop': '\t\t : in std_logic;\n',
           'in_eop': '\t\t : in std_logic;\n',
           'data_out': '\t : out std_logic_vector('+str (N_bit_out-1)+' downto 0);\n',
           'ready': '\t\t : out std_logic;\n',
           'out_sop': '\t\t : out std_logic;\n',
           'out_eop': '\t\t : out std_logic\n'}

type_dict = {'sensors_arr_type': '\t is array (0 to '+str (N_sensors-1)+') of signed ('+str (N_bit_out-1)+' downto 0);\n'}
             # 'integ_type': '\t\t\t is array (0 to N_sensors*NUM_STAGE-1) of signed (N_bit_out-1 downto 0);\n',
             # 'comb_type': '\t\t\t is array (0 to N_sensors*NUM_STAGE+N_sensors-1) of signed (N_bit_out-1 downto 0);\n'}

signal_dict = {'cnt':{'type': '\t\t\t\t: natural range 0 to '+str (R_DECIM)+' := ', 'value': '1'},
               'cnt_delay':{'type':'\t\t: natural range 0 to '+str (NUM_STAGE-1)+'  := ', 'value': '0'} ,
               'sensor_number':{'type':'\t: natural range 0 to '+str (N_sensors-1)+' := ', 'value':'0'},
               'channel_integ': {'type' : '\t: natural range 0 to '+str (N_sensors-1)+' := ', 'value' : '0'},
               'channel_comb': {'type' : '\t\t: natural range 0 to '+str (N_sensors-1)+' := ', 'value' : '0'},
               'channel_out': {'type' : '\t\t: natural range 0 to '+str (N_sensors-1)+' := ', 'value' : '0'},
               'integ':{'type' :'''\t\t\t: std_logic	:= ''', 'value': ''' '0' '''},
               'strob':{'type' : '''\t\t\t: std_logic	:= ''', 'value': ''' '0' '''},
               'comb':{'type' :'''\t\t\t\t: std_logic	:= ''', 'value': ''' '0' '''},
               'output':{'type' : '''\t\t\t: std_logic	:= ''', 'value': ''' '0' '''},
               'data_valid_sop':{'type' :'''\t: std_logic	:= ''', 'value': ''' '0' '''},
               'data_valid_eop':{'type' :'''\t: std_logic	:= ''', 'value': ''' '0' '''},
               'sensors_arr':{'type': '''\t\t: sensors_arr_type	:=''', 'value': ''' (others => (others => '0'))'''}}

for j in range(NUM_STAGE):
    signal_dict['integrator'+str(j)] = {'type': '''\t\t: sensors_arr_type	:=''', 'value': ''' (others => (others => '0'))'''}
for j in range(NUM_STAGE):
    signal_dict['c'+str(j)+'delay1'] = {'type': '''\t\t: sensors_arr_type	:=''', 'value': ''' (others => (others => '0'))'''}
for j in range(NUM_STAGE):
    signal_dict['c'+str(j)+'delay2'] = {'type': '''\t\t: sensors_arr_type	:=''', 'value': ''' (others => (others => '0'))'''}
for j in range(NUM_STAGE+1):
    signal_dict['combin' + str(j)] = {'type': '''\t\t: sensors_arr_type	:=''', 'value': ''' (others => (others => '0'))'''}

integ_dict = {'integrator0(channel_integ)': '\t\t<= integrator0(channel_integ) + sensors_arr(channel_integ)'}
comb_dict = {'combin0(channel_comb)': '\t\t<= integrator'+str (NUM_STAGE-1)+'(channel_comb)'}
delay1_dict = {'c'+str(j)+'delay1(channel_comb)': '\t\t<= combin'+str(j)+'(channel_comb)' for j in range(NUM_STAGE)}
delay2_dict = {'c'+str(j)+'delay2(channel_comb)': '\t\t<= c'+str(j)+'delay1(channel_comb)' for j in range(NUM_STAGE)}

for j in range(NUM_STAGE-1):
    integ_dict['integrator'+str(j+1)+'(channel_integ)'] = '\t\t<= integrator'+str(j+1)+'(channel_integ) + integrator'+str(j)+'(channel_integ)'
for j in range(NUM_STAGE):
    comb_dict['combin'+str(j+1)+'(channel_comb)'] = '\t\t<= combin'+str(j)+'(channel_comb) - c'+str(j)+'delay2(channel_comb)'

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
        for key, value in const_dict.items():
            file_vhdl.write('-- '+ (key) + ' = ' + (value) +'\n')
        file_vhdl.write('\n')
        file_vhdl.write('\n')
        file_vhdl.write('library ieee;\n')
        file_vhdl.write('use ieee.std_logic_1164.all;\n')
        file_vhdl.write('use ieee.numeric_std.all;\n')
        file_vhdl.write('\n')
        file_vhdl.write('entity '+ entity_name +' is\n')
        file_vhdl.write('\tport(\n')
        for key, value in io_dict.items():
            file_vhdl.write('\t\t'+(key)+(value))
        file_vhdl.write('\n')
        file_vhdl.write('\t);\n')
        file_vhdl.write('end '+ entity_name +';\n')
        file_vhdl.write('\n')
        file_vhdl.write('architecture behavior of '+ entity_name +' is\n')
        file_vhdl.write('\n')
        for key, value in type_dict.items():
            file_vhdl.write('type ' + (key) + (value))
        file_vhdl.write('\n')
        for key in signal_dict:
            type_of_signal = signal_dict[key]['type']
            value = signal_dict[key]['value']
            file_vhdl.write('signal ' + (key) + (type_of_signal)+(value)+';\n')
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
            file_vhdl.write('\t\t\t'+(key)+'\t\t\t<='+(value)+';\n')
        file_vhdl.write('\n')
        file_vhdl.write('\t\telsif (rising_edge(clk)) then\n')
        file_vhdl.write('\n')
        file_vhdl.write('''\t\t\tif enable = '0' then\n''')
        file_vhdl.write('\t\t\t\tready 	\t\t\t<= run;\n')
        file_vhdl.write('''\t\t\t\tout_sop \t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\tout_eop \t\t\t<= '0';\n''')
        file_vhdl.write('\t\t\t\tdata_out \t\t\t<= std_logic_vector(resize(signed(data_in),' +str(N_bit_out)+'));\n')
        for key in signal_dict:
            value = signal_dict[key]['value']
            file_vhdl.write('\t\t\t\t'+(key)+'\t\t<='+(value)+';\n')
        file_vhdl.write('\n')
        file_vhdl.write('\t\t\telse\n')
        file_vhdl.write('''\t\t\t\tif run = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\tif in_sop = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\t\tdata_valid_sop	\t\t\t\t<= '1';\n''')
        file_vhdl.write('''\t\t\t\t\t\tdata_valid_eop	\t\t\t\t<= '0';\n''')
        file_vhdl.write('''\t\t\t\t\t\tsensor_number	\t\t\t\t<= sensor_number + 1;\n''')
        file_vhdl.write('\t\t\t\t\t\tsensors_arr(sensor_number) \t\t<= resize (signed (data_in),' + str(N_bit_out) + ');\n')
        file_vhdl.write('''\t\t\t\t\telsif in_eop = '1' then\n''')
        file_vhdl.write('''\t\t\t\t\t\tdata_valid_eop	\t\t\t\t<= '1';\n''')
        file_vhdl.write('''\t\t\t\t\t\tsensor_number	\t\t\t\t<= 0;\n''')
        file_vhdl.write('\t\t\t\t\t\tsensors_arr(sensor_number) \t\t<= resize (signed (data_in),' + str(N_bit_out) + ');\n')
        file_vhdl.write('\t\t\t\t\telse\n')
        file_vhdl.write('''\t\t\t\t\t\tif (data_valid_sop = '1') and (data_valid_eop = '0') then\n''')
        file_vhdl.write('\t\t\t\t\t\t\tsensor_number\t\t\t\t<= sensor_number + 1;\n')
        file_vhdl.write('\t\t\t\t\t\t\tsensors_arr(sensor_number)\t<= resize (signed (data_in),' + str(N_bit_out) + ');\n')
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
        for key, value in integ_dict.items():
            file_vhdl.write('\t\t\t\t\t'+(key)+'\t\t'+(value)+';\n')
        file_vhdl.write('\t\t\t\t\tif channel_integ = '+str(N_sensors-1)+' then\n')
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
        for key, value in delay1_dict.items():
            file_vhdl.write('\t\t\t\t\t'+(key)+'\t\t'+(value)+';\n')
        file_vhdl.write('\n')
        for key, value in delay2_dict.items():
            file_vhdl.write('\t\t\t\t\t' + (key) + '\t\t' + (value) + ';\n')
        file_vhdl.write('\n')
        for key, value in comb_dict.items():
            file_vhdl.write('\t\t\t\t\t'+(key)+'\t\t'+(value)+';\n')
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
        file_vhdl.write('\t\t\t\t\tdata_out \t\t\t\t<= std_logic_vector(combin' + str(NUM_STAGE) + '(channel_out));\n')
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

WriteVHDL ()









