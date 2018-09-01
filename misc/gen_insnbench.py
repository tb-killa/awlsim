#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# AWL simulator - Generate instruction benchmark
#
# Copyright 2018 Michael Buesch <m@bues.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import division, absolute_import, print_function, unicode_literals

import sys
import random


nrIterations = 10000
if len(sys.argv) > 1:
	try:
		nrIterations = int(sys.argv[1])
		if nrIterations < 0:
			raise ValueError
	except ValueError:
		print("Invalid number of iterations.", file=sys.stderr)
		sys.exit(1)


insnCollection = (
	(
		( "U",		"BOOL"),
	), (
		( "UN",		"BOOL"),
	), (
		( "O",		"BOOL"),
	), (
		( "ON",		"BOOL"),
	), (
		( "X",		"BOOL"),
	), (
		( "XN",		"BOOL"),
	), (
		( "U(",		""),
		( ")",		""),
	), (
		( "UN(",	""),
		( ")",		""),
	), (
		( "O(",		""),
		( ")",		""),
	), (
		( "ON(",	""),
		( ")",		""),
	), (
		( "X(",		""),
		( ")",		""),
	), (
		( "XN(",	""),
		( ")",		""),
	), (
		( "=",		"BOOL"),
	), (
		( "R",		"BOOL"),
	), (
		( "S",		"BOOL"),
	), (
		( "NOT",	""),
	), (
		( "SET",	""),
	), (
		( "CLR",	""),
	), (
		( "SAVE",	""),
	), (
		( "FN",		"BOOL"),
	), (
		( "FP",		"BOOL"),
	), (
		( "==I",	""),
	), (
		( "<>I",	""),
	), (
		( ">I",		""),
	), (
		( "<I",		""),
	), (
		( ">=I",	""),
	), (
		( "<=I",	""),
	), (
		( "==D",	""),
	), (
		( "<>D",	""),
	), (
		( ">D",		""),
	), (
		( "<D",		""),
	), (
		( ">=D",	""),
	), (
		( "<=D",	""),
	), (
		( "==R",	""),
	), (
		( "<>R",	""),
	), (
		( ">R",		""),
	), (
		( "<R",		""),
	), (
		( ">=R",	""),
	), (
		( "<=R",	""),
	), (
		( "L",		"0"),
		( "BTI",	""),
	), (
		( "ITB",	""),
	), (
		( "L",		"0"),
		( "BTD",	""),
	), (
		( "ITD",	""),
	), (
		( "DTB",	""),
	), (
		( "DTR",	""),
	), (
		( "INVI",	""),
	), (
		( "INVD",	""),
	), (
		( "NEGI",	""),
	), (
		( "NEGD",	""),
	), (
		( "NEGR",	""),
	), (
		( "TAW",	""),
	), (
		( "TAD",	""),
	), (
		( "RND",	""),
	), (
		( "TRUNC",	""),
	), (
		( "RND+",	""),
	), (
		( "RND-",	""),
	), (
		( "FR",		"COUNTER"),
	), (
		( "L",		"RANDOM_DWORD"),
	), (
		( "LC",		"WORD"),
	), (
		( "ZV",		"COUNTER"),
	), (
		( "ZR",		"COUNTER"),
	), (
		( "AUF",	"DB"),
	), (
		( "TDB",	""),
	), (
		( "SPA",	"LABEL"),
	), (
		( "SPL",	"LABEL"),
	), (
		( "SPB",	"LABEL"),
	), (
		( "SPBN",	"LABEL"),
	), (
		( "SPBB",	"LABEL"),
	), (
		( "SPBNB",	"LABEL"),
	), (
		( "SPBI",	"LABEL"),
	), (
		( "SPBIN",	"LABEL"),
	), (
		( "SPO",	"LABEL"),
	), (
		( "SPS",	"LABEL"),
	), (
		( "SPZ",	"LABEL"),
	), (
		( "SPN",	"LABEL"),
	), (
		( "SPP",	"LABEL"),
	), (
		( "SPM",	"LABEL"),
	), (
		( "SPPZ",	"LABEL"),
	), (
		( "SPMZ",	"LABEL"),
	), (
		( "SPU",	"LABEL"),
	), (
		( "LOOP",	"LABEL"),
	), (
		( "+I",		""),
	), (
		( "-I",		""),
	), (
		( "*I",		""),
	), (
		( "/I",		""),
	), (
		( "+",		"0"),
	), (
		( "+D",		""),
	), (
		( "-D",		""),
	), (
		( "*D",		""),
	), (
		( "/D",		""),
	), (
		( "MOD",	""),
	), (
		( "+R",		""),
	), (
		( "-R",		""),
	), (
		( "*R",		""),
	), (
		( "/R",		""),
	), (
		( "ABS",	""),
	), (
		( "SQR",	""),
	), (
		( "SQRT",	""),
	), (
		( "EXP",	""),
	), (
		( "LN",		""),
	), (
		( "SIN",	""),
	), (
		( "COS",	""),
	), (
		( "TAN",	""),
	), (
		( "ASIN",	""),
	), (
		( "ACOS",	""),
	), (
		( "ATAN",	""),
	), (
		( "LAR1",	""),
	), (
		( "LAR2",	""),
	), (
		( "T",		"DWORD"),
	), (
		( "TAR",	""),
	), (
		( "TAR1",	""),
	), (
		( "TAR2",	""),
	), (
		( "MCR(",	""),
		( "MCRA",	""),
		( "MCRD",	""),
		( ")MCR",	""),
	), (
		( "SSI",	""),
	), (
		( "SSD",	""),
	), (
		( "SLW",	""),
	), (
		( "SRW",	""),
	), (
		( "SLD",	""),
	), (
		( "SRD",	""),
	), (
		( "RLD",	""),
	), (
		( "RRD",	""),
	), (
		( "RLDA",	""),
	), (
		( "RRDA",	""),
	), (
		( "L",		"0"),
		( "SI",		"TIMER"),
	), (
		( "L",		"0"),
		( "SV",		"TIMER"),
	), (
		( "L",		"0"),
		( "SE",		"TIMER"),
	), (
		( "L",		"0"),
		( "SS",		"TIMER"),
	), (
		( "L",		"0"),
		( "SA",		"TIMER"),
	), (
		( "UW",		""),
	), (
		( "OW",		""),
	), (
		( "XOW",	""),
	), (
		( "UD",		""),
	), (
		( "OD",		""),
	), (
		( "XOD",	""),
	), (
		( "TAK",	""),
	), (
		( "PUSH",	""),
	), (
		( "POP",	""),
	), (
		( "ENT",	""),
	), (
		( "LEAVE",	""),
	), (
		( "INC",	"0"),
	), (
		( "DEC",	"0"),
	), (
		( "+AR1",	""),
	), (
		( "+AR2",	""),
	), (
		( "BLD",	"0"),
	), (
		( "NOP",	"0"),
	), (
		( "CALL",	"FC 42"),
	), (
		( "CALL",	"FB 45, DB 45"),
	), (
		( "SET",	""),
	), (
		( "CC",		"FC 43"),
	), (
		( "UC",		"FC 44"),
	)
)

def getLabelName(index):
	ret = [None] * 4
	for i in range(3, -1, -1):
		ret[i] = chr(ord("A") + (index % 26))
		index //= 26
	return "".join(ret)

rnd = random.Random()
rnd.seed(42)

labelIndex = 0
print("// nrIterations=%d" % nrIterations)
print("ORGANIZATION_BLOCK OB 1")
print("BEGIN")
for i in range(nrIterations):
	for insn, args in rnd.choice(insnCollection):
		prefixStr = suffixStr = None
		if args == "":
			argsStr = ""
		elif args == "BOOL":
			argsStr = "M 0.4"
		elif args == "WORD":
			argsStr = "MW 0"
		elif args == "DWORD":
			argsStr = "MD 0"
		elif args == "TIMER":
			argsStr = "T 42"
		elif args == "COUNTER":
			argsStr = "Z 42"
		elif args == "DB":
			argsStr = "DB 42"
		elif args == "LABEL":
			labelName = getLabelName(labelIndex)
			prefixStr = "\tL 0;\n\tCLR;"
			argsStr = labelName
			suffixStr = "%s:\tNOP 0;" % labelName
			labelIndex += 1
		elif args == "RANDOM_DWORD":
			argsStr = "DW#16#%08X" % rnd.randint(0, 0xFFFFFFFF)
		else:
			argsStr = args
		if prefixStr:
			print(prefixStr)
		if argsStr:
			argsStr = " " + argsStr
		print("\t%s%s;" % (insn, argsStr))
		if suffixStr:
			print(suffixStr)
print("END_ORGANIZATION_BLOCK")

print("\nDATA_BLOCK DB 42")
print("\tSTRUCT")
print("\t\tVAR : INT;")
print("\tEND_STRUCT")
print("BEGIN")
print("END_DATA_BLOCK")

print("\nFUNCTION FC 42 : VOID")
print("BEGIN")
print("\tBE;")
print("END_FUNCTION")

print("\nFUNCTION FC 43 : VOID")
print("BEGIN")
print("\tBEA")
print("END_FUNCTION")

print("\nFUNCTION FC 44 : VOID")
print("BEGIN")
print("\tSET;")
print("\tBEB;")
print("END_FUNCTION")

print("\nFUNCTION_BLOCK FB 45")
print("BEGIN")
print("END_FUNCTION_BLOCK")

print("\nDATA_BLOCK DB 45")
print("\tFB 45")
print("BEGIN")
print("END_DATA_BLOCK")