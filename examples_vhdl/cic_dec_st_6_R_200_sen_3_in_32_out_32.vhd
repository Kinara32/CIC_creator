--cicpy_decim

-- N_bit_in = 32
-- N_bit_out = 32
-- N_sensors = 3
-- R_DECIM = 200
-- NUM_STAGE = 6
-- Hogenauer_pruning = True


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity cicpy_decim is
	port(
		clk			 : in std_logic;
		reset		 : in std_logic;
		data_in		 : in std_logic_vector(31 downto 0);
		enable		 : in std_logic;
		run			 : in std_logic;
		in_sop		 : in std_logic;
		in_eop		 : in std_logic;
		data_out	 : out std_logic_vector(31 downto 0);
		ready		 : out std_logic;
		out_sop		 : out std_logic;
		out_eop		 : out std_logic

	);
end cicpy_decim;

architecture behavior of cicpy_decim is

type sensors_arr_type is array (0 to 2) of signed (83 downto 0);
type array_84_type	 is array (0 to 2) of signed (83 downto 0);
type array_81_type	 is array (0 to 2) of signed (80 downto 0);
type array_72_type	 is array (0 to 2) of signed (71 downto 0);
type array_65_type	 is array (0 to 2) of signed (64 downto 0);
type array_57_type	 is array (0 to 2) of signed (56 downto 0);
type array_50_type	 is array (0 to 2) of signed (49 downto 0);
type array_43_type	 is array (0 to 2) of signed (42 downto 0);
type array_39_type	 is array (0 to 2) of signed (38 downto 0);
type array_38_type	 is array (0 to 2) of signed (37 downto 0);
type array_37_type	 is array (0 to 2) of signed (36 downto 0);
type array_36_type	 is array (0 to 2) of signed (35 downto 0);
type array_35_type	 is array (0 to 2) of signed (34 downto 0);

signal cnt				: natural range 0 to 200 := 1;
signal cnt_delay		: natural range 0 to 5  := 0;
signal sensor_number	: natural range 0 to 2 := 0;
signal channel_integ	: natural range 0 to 2 := 0;
signal channel_comb		: natural range 0 to 2 := 0;
signal channel_out		: natural range 0 to 2 := 0;
signal integ			: std_logic	:=  '0' ;
signal strob			: std_logic	:=  '0' ;
signal comb				: std_logic	:=  '0' ;
signal output			: std_logic	:=  '0' ;
signal data_valid_sop	: std_logic	:=  '0' ;
signal data_valid_eop	: std_logic	:=  '0' ;
signal sensors_arr		: sensors_arr_type	:= (others => (others => '0'));
signal integrator0		: array_81_type	:= (others => (others => '0'));
signal integrator1		: array_72_type	:= (others => (others => '0'));
signal integrator2		: array_65_type	:= (others => (others => '0'));
signal integrator3		: array_57_type	:= (others => (others => '0'));
signal integrator4		: array_50_type	:= (others => (others => '0'));
signal integrator5		: array_43_type	:= (others => (others => '0'));
signal c0delay1			: array_39_type	:= (others => (others => '0'));
signal c1delay1			: array_38_type	:= (others => (others => '0'));
signal c2delay1			: array_37_type	:= (others => (others => '0'));
signal c3delay1			: array_36_type	:= (others => (others => '0'));
signal c4delay1			: array_36_type	:= (others => (others => '0'));
signal c5delay1			: array_35_type	:= (others => (others => '0'));
signal c0delay2			: array_39_type	:= (others => (others => '0'));
signal c1delay2			: array_38_type	:= (others => (others => '0'));
signal c2delay2			: array_37_type	:= (others => (others => '0'));
signal c3delay2			: array_36_type	:= (others => (others => '0'));
signal c4delay2			: array_36_type	:= (others => (others => '0'));
signal c5delay2			: array_35_type	:= (others => (others => '0'));
signal combin0			: array_39_type	:= (others => (others => '0'));
signal combin1			: array_39_type	:= (others => (others => '0'));
signal combin2			: array_38_type	:= (others => (others => '0'));
signal combin3			: array_37_type	:= (others => (others => '0'));
signal combin4			: array_36_type	:= (others => (others => '0'));
signal combin5			: array_36_type	:= (others => (others => '0'));
signal combin6			: array_35_type	:= (others => (others => '0'));

begin
	main:process(clk,reset)
	begin
		if reset = '1' then

			ready 			<= '0';
			out_sop 		<= '0';
			out_eop 		<= '0';
			data_out 		<= (others => '0');

			cnt					<=1;
			cnt_delay			<=0;
			sensor_number		<=0;
			channel_integ		<=0;
			channel_comb		<=0;
			channel_out			<=0;
			integ				<= '0' ;
			strob				<= '0' ;
			comb				<= '0' ;
			output				<= '0' ;
			data_valid_sop		<= '0' ;
			data_valid_eop		<= '0' ;
			sensors_arr			<= (others => (others => '0'));
			integrator0			<= (others => (others => '0'));
			integrator1			<= (others => (others => '0'));
			integrator2			<= (others => (others => '0'));
			integrator3			<= (others => (others => '0'));
			integrator4			<= (others => (others => '0'));
			integrator5			<= (others => (others => '0'));
			c0delay1			<= (others => (others => '0'));
			c1delay1			<= (others => (others => '0'));
			c2delay1			<= (others => (others => '0'));
			c3delay1			<= (others => (others => '0'));
			c4delay1			<= (others => (others => '0'));
			c5delay1			<= (others => (others => '0'));
			c0delay2			<= (others => (others => '0'));
			c1delay2			<= (others => (others => '0'));
			c2delay2			<= (others => (others => '0'));
			c3delay2			<= (others => (others => '0'));
			c4delay2			<= (others => (others => '0'));
			c5delay2			<= (others => (others => '0'));
			combin0				<= (others => (others => '0'));
			combin1				<= (others => (others => '0'));
			combin2				<= (others => (others => '0'));
			combin3				<= (others => (others => '0'));
			combin4				<= (others => (others => '0'));
			combin5				<= (others => (others => '0'));
			combin6				<= (others => (others => '0'));

		elsif (rising_edge(clk)) then

			if enable = '0' then
				ready 				<= run;
				out_sop 			<= '0';
				out_eop 			<= '0';
				data_out 			<= std_logic_vector(resize(signed(data_in),32));

				cnt					<=1;
				cnt_delay			<=0;
				sensor_number		<=0;
				channel_integ		<=0;
				channel_comb		<=0;
				channel_out			<=0;
				integ				<= '0' ;
				strob				<= '0' ;
				comb				<= '0' ;
				output				<= '0' ;
				data_valid_sop		<= '0' ;
				data_valid_eop		<= '0' ;
				sensors_arr			<= (others => (others => '0'));
				integrator0			<= (others => (others => '0'));
				integrator1			<= (others => (others => '0'));
				integrator2			<= (others => (others => '0'));
				integrator3			<= (others => (others => '0'));
				integrator4			<= (others => (others => '0'));
				integrator5			<= (others => (others => '0'));
				c0delay1			<= (others => (others => '0'));
				c1delay1			<= (others => (others => '0'));
				c2delay1			<= (others => (others => '0'));
				c3delay1			<= (others => (others => '0'));
				c4delay1			<= (others => (others => '0'));
				c5delay1			<= (others => (others => '0'));
				c0delay2			<= (others => (others => '0'));
				c1delay2			<= (others => (others => '0'));
				c2delay2			<= (others => (others => '0'));
				c3delay2			<= (others => (others => '0'));
				c4delay2			<= (others => (others => '0'));
				c5delay2			<= (others => (others => '0'));
				combin0				<= (others => (others => '0'));
				combin1				<= (others => (others => '0'));
				combin2				<= (others => (others => '0'));
				combin3				<= (others => (others => '0'));
				combin4				<= (others => (others => '0'));
				combin5				<= (others => (others => '0'));
				combin6				<= (others => (others => '0'));

			else
				if run = '1' then
					if in_sop = '1' then
						data_valid_sop					<= '1';
						data_valid_eop					<= '0';
						sensor_number					<= sensor_number + 1;
						sensors_arr(sensor_number) 		<= resize (signed (data_in),84);
					elsif in_eop = '1' then
						data_valid_eop					<= '1';
						sensor_number					<= 0;
						sensors_arr(sensor_number) 		<= resize (signed (data_in),84);
					else
						if (data_valid_sop = '1') and (data_valid_eop = '0') then
							sensor_number				<= sensor_number + 1;
							sensors_arr(sensor_number)	<= resize (signed (data_in),84);
						else
							sensor_number 				<= 0;
						end if;
					end if;
				else
					sensor_number 			<= 0;
					data_valid_sop			<= '0';
					data_valid_eop			<= '0';
				end if;
				if (data_valid_sop = '1') and (data_valid_eop = '1') then
					integ					<= '1';
					data_valid_sop			<= '0';
					data_valid_eop			<= '0';
				end if;

				if integ = '1' then
					integrator0(channel_integ)				<= integrator0(channel_integ) + sensors_arr(channel_integ)(83 downto 3);
					integrator1(channel_integ)				<= integrator1(channel_integ) + integrator0(channel_integ)(80 downto 9);
					integrator2(channel_integ)				<= integrator2(channel_integ) + integrator1(channel_integ)(71 downto 7);
					integrator3(channel_integ)				<= integrator3(channel_integ) + integrator2(channel_integ)(64 downto 8);
					integrator4(channel_integ)				<= integrator4(channel_integ) + integrator3(channel_integ)(56 downto 7);
					integrator5(channel_integ)				<= integrator5(channel_integ) + integrator4(channel_integ)(49 downto 7);
					if channel_integ = 2 then
						channel_integ 		<= 0;
						integ 				<= '0';
						if cnt = 199 then
							strob 				<= '0';
							cnt 				<= 0;
						elsif cnt = 5 then
							strob 				<= '1';
							cnt 				<= cnt + 1;
						else
							strob 				<= '0';
							cnt 				<= cnt + 1;
						end if;
					else
						channel_integ 		<= channel_integ + 1;
					end if;
					if strob = '1' then
						comb 				<= '1';
					end if;
				end if;

				if comb = '1' then
					c1delay1(channel_comb)				<= combin1(channel_comb)(38 downto 1);
					c2delay1(channel_comb)				<= combin2(channel_comb)(37 downto 1);
					c3delay1(channel_comb)				<= combin3(channel_comb)(36 downto 1);
					c4delay1(channel_comb)				<= combin4(channel_comb)(35 downto 0);
					c5delay1(channel_comb)				<= combin5(channel_comb)(35 downto 1);
					c0delay1(channel_comb)				<= combin0(channel_comb);

					c0delay2(channel_comb)				<= c0delay1(channel_comb);
					c1delay2(channel_comb)				<= c1delay1(channel_comb);
					c2delay2(channel_comb)				<= c2delay1(channel_comb);
					c3delay2(channel_comb)				<= c3delay1(channel_comb);
					c4delay2(channel_comb)				<= c4delay1(channel_comb);
					c5delay2(channel_comb)				<= c5delay1(channel_comb);

					combin0(channel_comb)				<= integrator5(channel_comb)(42 downto 4);
					combin1(channel_comb)				<= combin0(channel_comb)- c0delay2(channel_comb);
					combin2(channel_comb)				<= combin1(channel_comb)(38 downto 1) - c1delay2(channel_comb);
					combin3(channel_comb)				<= combin2(channel_comb)(37 downto 1) - c2delay2(channel_comb);
					combin4(channel_comb)				<= combin3(channel_comb)(36 downto 1) - c3delay2(channel_comb);
					combin5(channel_comb)				<= combin4(channel_comb)(35 downto 0) - c4delay2(channel_comb);
					combin6(channel_comb)				<= combin5(channel_comb)(35 downto 1) - c5delay2(channel_comb);

					if channel_comb = 2 then
						channel_comb 		<= 0;
						comb 				<= '0';
						if cnt_delay = 5 then
							output 				<= '1';
						else
							cnt_delay 			<= cnt_delay + 1;
						end if;
					else
						channel_comb 			<= channel_comb + 1;
					end if;
				end if;

				if output = '1' then
					ready 					<= '1';
					data_out 				<= std_logic_vector(combin6(channel_out)(34 downto 3));
					if channel_out = 0 then
						out_sop 			<= '1';
						out_eop 			<= '0';
						channel_out 		<= channel_out + 1;
					elsif channel_out = 2 then
						out_sop 			<= '0';
						out_eop 			<= '1';
						output 				<= '0';
						channel_out 		<= 0;
					else
						out_sop 			<= '0';
						out_eop 			<= '0';
						channel_out 		<= channel_out + 1;
					end if;
				else
					ready 				<= '0';
					out_sop 			<= '0';
					out_eop 			<= '0';
				end if;
			end if;
		end if;
	end process;
end behavior;