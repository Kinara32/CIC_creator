  transcript on
  vlib work

  set DIR_NAME "C:/Dropbox/Python/Pycharm/PGC_ATAN"

  vcom "$DIR_NAME/cic_dec_st_6_R_200_sen_3_in_32_out_32.vhd"    -work work
  vcom "$DIR_NAME/CIC_custom_testbench_pipline_hog_32.vht"         -work work

  vsim work.CIC_custom_testbench
add wave -position insertpoint  \
sim:/cic_custom_testbench/Block_portmap/clk \
sim:/cic_custom_testbench/Block_portmap/reset \
sim:/cic_custom_testbench/Block_portmap/enable \
sim:/cic_custom_testbench/Block_portmap/run \
sim:/cic_custom_testbench/Block_portmap/in_sop \
sim:/cic_custom_testbench/Block_portmap/in_eop \
sim:/cic_custom_testbench/Block_portmap/data_valid_sop  \
sim:/cic_custom_testbench/Block_portmap/data_valid_eop 

add wave -radix decimal -position insertpoint  \
sim:/cic_custom_testbench/Block_portmap/cnt \
sim:/cic_custom_testbench/Block_portmap/cnt_delay \
sim:/cic_custom_testbench/Block_portmap/sensor_number \
sim:/cic_custom_testbench/Block_portmap/channel_integ \
sim:/cic_custom_testbench/Block_portmap/channel_comb \
sim:/cic_custom_testbench/Block_portmap/channel_out \
sim:/cic_custom_testbench/Block_portmap/integ \
sim:/cic_custom_testbench/Block_portmap/strob \
sim:/cic_custom_testbench/Block_portmap/comb \
sim:/cic_custom_testbench/Block_portmap/output

add wave -radix decimal -position insertpoint  \
sim:/cic_custom_testbench/Block_portmap/data_in \
sim:/cic_custom_testbench/Block_portmap/sensors_arr \
sim:/cic_custom_testbench/Block_portmap/integrator0 \
sim:/cic_custom_testbench/Block_portmap/integrator1 \
sim:/cic_custom_testbench/Block_portmap/integrator2 \
sim:/cic_custom_testbench/Block_portmap/integrator3 \
sim:/cic_custom_testbench/Block_portmap/integrator4 \
sim:/cic_custom_testbench/Block_portmap/integrator5 \
sim:/cic_custom_testbench/Block_portmap/c0delay1 \
sim:/cic_custom_testbench/Block_portmap/c1delay1 \
sim:/cic_custom_testbench/Block_portmap/c2delay1 \
sim:/cic_custom_testbench/Block_portmap/c3delay1 \
sim:/cic_custom_testbench/Block_portmap/c4delay1 \
sim:/cic_custom_testbench/Block_portmap/c5delay1 \
sim:/cic_custom_testbench/Block_portmap/c0delay2 \
sim:/cic_custom_testbench/Block_portmap/c1delay2 \
sim:/cic_custom_testbench/Block_portmap/c2delay2 \
sim:/cic_custom_testbench/Block_portmap/c3delay2 \
sim:/cic_custom_testbench/Block_portmap/c4delay2 \
sim:/cic_custom_testbench/Block_portmap/c5delay2 \
sim:/cic_custom_testbench/Block_portmap/combin0 \
sim:/cic_custom_testbench/Block_portmap/combin1 \
sim:/cic_custom_testbench/Block_portmap/combin2 \
sim:/cic_custom_testbench/Block_portmap/combin3 \
sim:/cic_custom_testbench/Block_portmap/combin4 \
sim:/cic_custom_testbench/Block_portmap/combin5 \
sim:/cic_custom_testbench/Block_portmap/combin6

add wave -position insertpoint  \
sim:/cic_custom_testbench/Block_portmap/ready \
sim:/cic_custom_testbench/Block_portmap/out_sop \
sim:/cic_custom_testbench/Block_portmap/out_eop 

add wave -radix decimal -position insertpoint  \
sim:/cic_custom_testbench/Block_portmap/data_out 

 run 1 ms
 wave zoom full