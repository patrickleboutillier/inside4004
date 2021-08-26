`timescale 1ns / 1ps
`default_nettype none
////////////////////////////////////////////////////////////////////////
// 
// 4004 Scratchpad Register Array
// 
// This file is part of the MCS-4 project hosted at OpenCores:
//      http://www.opencores.org/cores/mcs-4/
// 
// Copyright � 2012, 2020 by Reece Pollack <rrpollack@opencores.org>
// 
// These materials are provided under the Creative Commons
// "Attribution-NonCommercial-ShareAlike" Public License. They
// are NOT "public domain" and are protected by copyright.
// 
// This work based on materials provided by Intel Corporation and
// others under the same license. See the file doc/License for
// details of this license.
//
////////////////////////////////////////////////////////////////////////
 
module scratchpad ()

	reg  [7:0]	dram_array [0:7];
	reg  [7:0]	dram_temp;
	reg  [3:0]	din_n;
  
	// Row selection mux
	reg  [2:0]	row;					// {N0646, N0617, N0582}
	always @(posedge sysclk) begin
		if (sc & a22)
			row <= reg_rfsh;
		if (sc_m22_clk2)
			row <= data[3:1];
	end
 
 
	// Row Precharge/Read/Write stuff
	wire		row_read;				// (~POC)&CLK2&SC(A32+X12)
	wire		row_write;				// CLK2&SC(A12+M12)
 
	assign row_read  = ~(poc | ~(clk2 & sc & (a32 | x12)));
	assign row_write = sc & (a12 | m12) & clk2;
 
 
	// Column Read selection stuff
	reg n0615;
	always @(posedge sysclk) begin
		if (clk2)
			n0615 <= ~(x12 & (fin_fim_src_jin |
					(opa0_n & inc_isz_add_sub_xch_ld)));
	end
	wire rrab0 = ~(dc | n0615 | clk2);
 
	reg n0592;
	always @(posedge sysclk) begin
		if (clk2)
			n0592 <= ~((x22 & fin_fim_src_jin) |
					(~opa0_n & x12 & inc_isz_add_sub_xch_ld));
	end
	wire rrab1 = ~(dc | n0592 | clk2);
 
 
	// Column Write selection stuff
	wire n0564 = opa0_n & fin_fim_src_jin & dc;
	wire n0568 = inc_isz_xch & x32 & sc;
	wire wrab0 = clk2 & ((m12 & n0564) | ( opa0_n & n0568));
	wire wrab1 = clk2 & ((m22 & n0564) | (~opa0_n & n0568));
 
 
	// Force row 0 if FIN&X12
	wire fin_x12 = (n0636 & opa0_n) & x12;
 
	// Manage the row data buffer
	always @(posedge sysclk) begin 
		if (row_read)
			dram_temp <= dram_array[fin_x12 ? 3'b000 : row];
 
		if (wrab0)
			dram_temp[ 7:4] <= ~din_n;
		if (wrab1)
			dram_temp[ 3:0] <= ~din_n;
	end
 
	// Handle row writes
	always @(posedge sysclk) begin
		if (row_write)
			dram_array[row] <= dram_temp;
	end
 
	// Manage the data output mux
	reg   [3:0]	dout;
	always @* begin
		(* PARALLEL_CASE *)
		case (1'b1)
			rrab0:		dout = dram_temp[ 7:4];
			rrab1:		dout = dram_temp[ 3:0];
			default:	dout = 4'bzzzz;
		endcase
	end
	assign data = dout;
 
	// Data In latch
	always @(posedge sysclk) begin
		if (gate)
			din_n <= ~data;
	end
 
endmodule
 