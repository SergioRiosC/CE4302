`timescale 1 ps / 1 ps

module system_tb;

  logic clk;
  logic reset_n;
  wire [31:0] addr;

  initial begin
    reset_n <= 0;
    #20;
    reset_n <= 1;
  end

  always begin
    clk <= 0;
    #5;
    clk <= 1;
    #5;
  end
  

 sisa_test dut(
		.clk_clk(clk),                //          clk.clk
		.instr_export_instr_if(addr),  // instr_export.instr_if
		//.instr_export_instr_de,  //             .instr_de
		//.instr_export_instr_ex,  //             .instr_ex
		//.instr_export_instr_mem, //             .instr_mem
		//.instr_export_instr_wb,  //             .instr_wb
		.reset_reset_n(reset_n)           //        reset.reset_n
	);

 
  always @(posedge clk) begin
    if (addr == 32'h100) begin
      #100;
      $display("Simulation ended");
      $stop;
    end

  end



endmodule
