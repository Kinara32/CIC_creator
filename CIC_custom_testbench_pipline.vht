-- Quartus Prime VHDL Template
-- CIC_custom_testbench

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_textio.all;

entity CIC_custom_testbench is
end entity;

architecture logic of CIC_custom_testbench is
	
	component cicpy_decim
		port(
			clk			: in std_logic;
			reset		: in std_logic;
			data_in		: in std_logic_vector (31 downto 0);
			run			: in std_logic;
			in_sop		: in std_logic;
			in_eop		: in std_logic;
			enable		: in std_logic;

			data_out	: out std_logic_vector (83 downto 0);
			ready		: out std_logic;
			out_sop		: out std_logic;
			out_eop		: out std_logic
		);
	end component cicpy_decim;
	
	constant clk_period		: time := 10 ns;
	
	signal clk			: std_logic:= '0';
	signal reset		: std_logic:= '1';
	signal data_in		: std_logic_vector (31 downto 0):= (others => '0');
	signal run			: std_logic:= '0';
	signal in_sop		: std_logic:= '0';
	signal in_eop		: std_logic:= '0';
	signal enable		: std_logic:= '0';

	signal data_out		: std_logic_vector (83 downto 0):= (others => '0');
	signal ready		: std_logic:= '0';
	signal out_sop		: std_logic:= '0';
	signal out_eop		: std_logic:= '0';

begin
	Block_portmap:cicpy_decim port map(
		
		clk				=> clk,
		reset			=> reset,
		data_in			=> data_in,
		run				=> run,
		enable			=> enable,
		in_sop			=> in_sop,
		in_eop			=> in_eop,
		data_out		=> data_out,
		ready			=> ready,
		out_sop			=> out_sop,
		out_eop			=> out_eop
		
	);
	
	clock: process
	begin
		clk <= '0';
		wait for clk_period/2;
		clk <= '1';
		wait for clk_period/2;
	end process;
	
	rst: process
	begin
		wait for 20 ns;
		reset <= '1';
		wait for 80 ns;
		reset <= '0';
		wait;
	end process;
	
	main: process
	begin
		wait for 150 ns;
		wait until rising_edge(clk);
		enable		<= '1';
		wait for 100 ns;
		wait until rising_edge(clk);
		run 		<= '1';
		in_sop 		<= '1';
		data_in 	<= x"00000001"; --x"7FFFFFFF"
		wait until rising_edge(clk);
		in_sop 		<= '0';
		in_eop 		<= '0';
		data_in 	<= x"000000FF";
		wait until rising_edge(clk);
		in_sop 		<= '0';
		in_eop 		<= '1';
		data_in 	<= x"00000001";
		wait until rising_edge(clk);
		in_eop 		<= '0';
		data_in 	<= (others => '0');
		run 		<= '0';
		loop
			wait for 90 ns;
			wait until rising_edge(clk);
			run 		<= '1';
			in_sop 		<= '1';
			data_in 	<= x"00000000"; -- -2608 
			wait until rising_edge(clk);
			in_sop 		<= '0';
			in_eop 		<= '0';
			data_in 	<= x"00000000";
			wait until rising_edge(clk);
			in_sop 		<= '0';
			in_eop 		<= '1';
			data_in 	<= x"00000000"; -- -3808
			wait until rising_edge(clk);
			in_eop 		<= '0';
			data_in 	<= (others => '0');
			run 		<= '0';
		end loop;
	end process;
	
	write_to_file:process
	file cic_vector		: text open write_mode is "cic.txt";
	variable row		: line;
	begin
		loop
			wait until rising_edge(out_sop);
			hwrite (row,data_out);
			writeline (cic_vector,row);
		end loop;
	end process;
	
end logic;	