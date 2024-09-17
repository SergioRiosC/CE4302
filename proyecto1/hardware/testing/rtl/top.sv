//`define ENABLE_HPS
//`default_nettype none

module top (
    ///////// CLOCK2 /////////
    input              CLOCK2_50,
    ///////// CLOCK3 /////////
    input              CLOCK3_50,
    ///////// CLOCK4 /////////
    input              CLOCK4_50,
    ///////// CLOCK /////////
    input              CLOCK_50,

    ///////// GPIO /////////
    inout [35:0] GPIO_0,
    inout [35:0] GPIO_1,
    ///////// HEX0 /////////
    output      [6:0]  HEX0,
    ///////// HEX1 /////////
    output      [6:0]  HEX1,
    ///////// HEX2 /////////
    output      [6:0]  HEX2,
    ///////// HEX3 /////////
    output      [6:0]  HEX3,
    ///////// HEX4 /////////
    output      [6:0]  HEX4,
    ///////// HEX5 /////////
    output      [6:0]  HEX5,
    ///////// KEY /////////
    input       [3:0]  KEY,

    ///////// LEDR /////////
    output [7:0] LEDR,

    ///////// SW /////////
    input [9:0] SW
);

  // KEY 0 es clk manual 
  wire debug_mode;
  assign debug_mode = SW[1];

  wire manual_clk;
  assign manual_clk = KEY[0];

	wire [31:0] addr;

	assign LEDR[0] = addr[0];

  wire clk;
  assign clk = (debug_mode)?  CLOCK_50 : manual_clk;

  wire reset;
  assign reset = SW[0];


endmodule
