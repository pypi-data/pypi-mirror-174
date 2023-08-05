//Note: initial mapping (logical qubit at each location): 1, 0, 2, 5, 6, -1, 3, 4, 7, 8, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, 
//Note: initial mapping (location of each logical qubit): 1, 0, 2, 6, 7, 3, 4, 8, 9, 12, 
OPENQASM 2.0;
include "qelib1.inc";
qreg q[20];
creg c[20];
h q[1]; //cycle: 0 //h q[0]
rz(-0.7854) q[1]; //cycle: 1 //rz(-0.7854) q[0]
cx q[1],q[0]; //cycle: 2 //cx q[0],q[1]
rz(0.7854) q[1]; //cycle: 4 //rz(0.7854) q[0]
cx q[1],q[0]; //cycle: 5 //cx q[0],q[1]
rz(-0.3927) q[1]; //cycle: 7 //rz(-0.3927) q[0]
h q[0]; //cycle: 7 //h q[1]
cx q[1],q[2]; //cycle: 8 //cx q[0],q[2]
rz(-0.7854) q[0]; //cycle: 8 //rz(-0.7854) q[1]
rz(0.3927) q[1]; //cycle: 10 //rz(0.3927) q[0]
cx q[1],q[2]; //cycle: 11 //cx q[0],q[2]
rz(-0.19635) q[1]; //cycle: 13 //rz(-0.19635) q[0]
cx q[1],q[6]; //cycle: 14 //cx q[0],q[3]
rz(0.19635) q[1]; //cycle: 16 //rz(0.19635) q[0]
cx q[1],q[6]; //cycle: 17 //cx q[0],q[3]
rz(-0.09815) q[1]; //cycle: 19 //rz(-0.09815) q[0]
cx q[1],q[7]; //cycle: 20 //cx q[0],q[4]
rz(0.09815) q[1]; //cycle: 22 //rz(0.09815) q[0]
cx q[1],q[7]; //cycle: 23 //cx q[0],q[4]
rz(-0.0491) q[1]; //cycle: 25 //rz(-0.0491) q[0]
swap q[1],q[2]; //cycle: 26
cx q[2],q[3]; //cycle: 32 //cx q[0],q[5]
cx q[0],q[1]; //cycle: 32 //cx q[1],q[2]
rz(0.0491) q[2]; //cycle: 34 //rz(0.0491) q[0]
rz(0.7854) q[0]; //cycle: 34 //rz(0.7854) q[1]
cx q[2],q[3]; //cycle: 35 //cx q[0],q[5]
cx q[0],q[1]; //cycle: 35 //cx q[1],q[2]
rz(-0.02455) q[2]; //cycle: 37 //rz(-0.02455) q[0]
rz(-0.3927) q[0]; //cycle: 37 //rz(-0.3927) q[1]
h q[1]; //cycle: 37 //h q[2]
rz(-0.7854) q[1]; //cycle: 38 //rz(-0.7854) q[2]
swap q[0],q[1]; //cycle: 39
swap q[2],q[3]; //cycle: 39
cx q[3],q[4]; //cycle: 45 //cx q[0],q[6]
cx q[1],q[6]; //cycle: 45 //cx q[1],q[3]
rz(0.02455) q[3]; //cycle: 47 //rz(0.02455) q[0]
rz(0.3927) q[1]; //cycle: 47 //rz(0.3927) q[1]
cx q[3],q[4]; //cycle: 48 //cx q[0],q[6]
cx q[1],q[6]; //cycle: 48 //cx q[1],q[3]
swap q[0],q[5]; //cycle: 49
rz(-0.01225) q[3]; //cycle: 50 //rz(-0.01225) q[0]
rz(-0.19635) q[1]; //cycle: 50 //rz(-0.19635) q[1]
cx q[3],q[8]; //cycle: 51 //cx q[0],q[7]
cx q[1],q[7]; //cycle: 51 //cx q[1],q[4]
rz(0.01225) q[3]; //cycle: 53 //rz(0.01225) q[0]
rz(0.19635) q[1]; //cycle: 53 //rz(0.19635) q[1]
cx q[3],q[8]; //cycle: 54 //cx q[0],q[7]
cx q[1],q[7]; //cycle: 54 //cx q[1],q[4]
cx q[5],q[6]; //cycle: 55 //cx q[2],q[3]
rz(-0.00615) q[3]; //cycle: 56 //rz(-0.00615) q[0]
rz(-0.09815) q[1]; //cycle: 56 //rz(-0.09815) q[1]
cx q[3],q[9]; //cycle: 57 //cx q[0],q[8]
cx q[1],q[2]; //cycle: 57 //cx q[1],q[5]
rz(0.7854) q[5]; //cycle: 57 //rz(0.7854) q[2]
cx q[5],q[6]; //cycle: 58 //cx q[2],q[3]
rz(0.00615) q[3]; //cycle: 59 //rz(0.00615) q[0]
rz(0.09815) q[1]; //cycle: 59 //rz(0.09815) q[1]
cx q[3],q[9]; //cycle: 60 //cx q[0],q[8]
cx q[1],q[2]; //cycle: 60 //cx q[1],q[5]
rz(-0.3927) q[5]; //cycle: 60 //rz(-0.3927) q[2]
h q[6]; //cycle: 60 //h q[3]
rz(-0.7854) q[6]; //cycle: 61 //rz(-0.7854) q[3]
swap q[6],q[7]; //cycle: 62
rz(-0.00305) q[3]; //cycle: 62 //rz(-0.00305) q[0]
rz(-0.0491) q[1]; //cycle: 62 //rz(-0.0491) q[1]
swap q[3],q[4]; //cycle: 63
swap q[8],q[12]; //cycle: 63
swap q[1],q[2]; //cycle: 64
cx q[5],q[6]; //cycle: 68 //cx q[2],q[4]
cx q[4],q[8]; //cycle: 69 //cx q[0],q[9]
cx q[2],q[3]; //cycle: 70 //cx q[1],q[6]
rz(0.3927) q[5]; //cycle: 70 //rz(0.3927) q[2]
rz(0.00305) q[4]; //cycle: 71 //rz(0.00305) q[0]
cx q[5],q[6]; //cycle: 71 //cx q[2],q[4]
swap q[0],q[1]; //cycle: 72
cx q[4],q[8]; //cycle: 72 //cx q[0],q[9]
rz(0.0491) q[2]; //cycle: 72 //rz(0.0491) q[1]
cx q[2],q[3]; //cycle: 73 //cx q[1],q[6]
rz(-0.19635) q[5]; //cycle: 73 //rz(-0.19635) q[2]
cx q[7],q[6]; //cycle: 73 //cx q[3],q[4]
h q[4]; //cycle: 74 //h q[0]
rz(-0.02455) q[2]; //cycle: 75 //rz(-0.02455) q[1]
rz(0.7854) q[7]; //cycle: 75 //rz(0.7854) q[3]
cx q[7],q[6]; //cycle: 76 //cx q[3],q[4]
cx q[5],q[0]; //cycle: 78 //cx q[2],q[5]
rz(-0.3927) q[7]; //cycle: 78 //rz(-0.3927) q[3]
h q[6]; //cycle: 78 //h q[4]
rz(-0.7854) q[6]; //cycle: 79 //rz(-0.7854) q[4]
rz(0.19635) q[5]; //cycle: 80 //rz(0.19635) q[2]
cx q[5],q[0]; //cycle: 81 //cx q[2],q[5]
swap q[1],q[7]; //cycle: 82
swap q[2],q[3]; //cycle: 82
swap q[8],q[12]; //cycle: 83
rz(-0.09815) q[5]; //cycle: 83 //rz(-0.09815) q[2]
swap q[5],q[6]; //cycle: 84
cx q[1],q[0]; //cycle: 88 //cx q[3],q[5]
cx q[3],q[8]; //cycle: 89 //cx q[1],q[7]
cx q[6],q[2]; //cycle: 90 //cx q[2],q[6]
rz(0.3927) q[1]; //cycle: 90 //rz(0.3927) q[3]
rz(0.02455) q[3]; //cycle: 91 //rz(0.02455) q[1]
cx q[1],q[0]; //cycle: 91 //cx q[3],q[5]
cx q[3],q[8]; //cycle: 92 //cx q[1],q[7]
rz(0.09815) q[6]; //cycle: 92 //rz(0.09815) q[2]
cx q[6],q[2]; //cycle: 93 //cx q[2],q[6]
rz(-0.19635) q[1]; //cycle: 93 //rz(-0.19635) q[3]
cx q[5],q[0]; //cycle: 93 //cx q[4],q[5]
swap q[7],q[8]; //cycle: 94
rz(-0.01225) q[3]; //cycle: 94 //rz(-0.01225) q[1]
cx q[3],q[9]; //cycle: 95 //cx q[1],q[8]
rz(-0.0491) q[6]; //cycle: 95 //rz(-0.0491) q[2]
cx q[1],q[2]; //cycle: 95 //cx q[3],q[6]
rz(0.7854) q[5]; //cycle: 95 //rz(0.7854) q[4]
cx q[5],q[0]; //cycle: 96 //cx q[4],q[5]
rz(0.01225) q[3]; //cycle: 97 //rz(0.01225) q[1]
rz(0.19635) q[1]; //cycle: 97 //rz(0.19635) q[3]
cx q[3],q[9]; //cycle: 98 //cx q[1],q[8]
cx q[1],q[2]; //cycle: 98 //cx q[3],q[6]
rz(-0.3927) q[5]; //cycle: 98 //rz(-0.3927) q[4]
h q[0]; //cycle: 98 //h q[5]
rz(-0.7854) q[0]; //cycle: 99 //rz(-0.7854) q[5]
rz(-0.00615) q[3]; //cycle: 100 //rz(-0.00615) q[1]
cx q[6],q[7]; //cycle: 100 //cx q[2],q[7]
rz(-0.09815) q[1]; //cycle: 100 //rz(-0.09815) q[3]
rz(0.0491) q[6]; //cycle: 102 //rz(0.0491) q[2]
cx q[6],q[7]; //cycle: 103 //cx q[2],q[7]
swap q[8],q[12]; //cycle: 105
rz(-0.02455) q[6]; //cycle: 105 //rz(-0.02455) q[2]
cx q[1],q[7]; //cycle: 105 //cx q[3],q[7]
swap q[2],q[6]; //cycle: 106
swap q[3],q[9]; //cycle: 106
rz(0.09815) q[1]; //cycle: 107 //rz(0.09815) q[3]
cx q[1],q[7]; //cycle: 108 //cx q[3],q[7]
rz(-0.0491) q[1]; //cycle: 110 //rz(-0.0491) q[3]
cx q[9],q[8]; //cycle: 112 //cx q[1],q[9]
cx q[2],q[3]; //cycle: 112 //cx q[2],q[8]
cx q[5],q[6]; //cycle: 112 //cx q[4],q[6]
rz(0.00615) q[9]; //cycle: 114 //rz(0.00615) q[1]
rz(0.02455) q[2]; //cycle: 114 //rz(0.02455) q[2]
rz(0.3927) q[5]; //cycle: 114 //rz(0.3927) q[4]
cx q[9],q[8]; //cycle: 115 //cx q[1],q[9]
cx q[2],q[3]; //cycle: 115 //cx q[2],q[8]
cx q[5],q[6]; //cycle: 115 //cx q[4],q[6]
swap q[3],q[8]; //cycle: 117
rz(-0.01225) q[2]; //cycle: 117 //rz(-0.01225) q[2]
rz(-0.19635) q[5]; //cycle: 117 //rz(-0.19635) q[4]
h q[9]; //cycle: 117 //h q[1]
swap q[1],q[7]; //cycle: 118
swap q[5],q[6]; //cycle: 118
cx q[2],q[3]; //cycle: 123 //cx q[2],q[9]
cx q[7],q[8]; //cycle: 124 //cx q[3],q[8]
cx q[6],q[1]; //cycle: 124 //cx q[4],q[7]
cx q[0],q[5]; //cycle: 124 //cx q[5],q[6]
rz(0.01225) q[2]; //cycle: 125 //rz(0.01225) q[2]
cx q[2],q[3]; //cycle: 126 //cx q[2],q[9]
rz(0.0491) q[7]; //cycle: 126 //rz(0.0491) q[3]
rz(0.19635) q[6]; //cycle: 126 //rz(0.19635) q[4]
rz(0.7854) q[0]; //cycle: 126 //rz(0.7854) q[5]
cx q[7],q[8]; //cycle: 127 //cx q[3],q[8]
cx q[6],q[1]; //cycle: 127 //cx q[4],q[7]
cx q[0],q[5]; //cycle: 127 //cx q[5],q[6]
h q[2]; //cycle: 128 //h q[2]
rz(-0.02455) q[7]; //cycle: 129 //rz(-0.02455) q[3]
rz(-0.09815) q[6]; //cycle: 129 //rz(-0.09815) q[4]
rz(-0.3927) q[0]; //cycle: 129 //rz(-0.3927) q[5]
h q[5]; //cycle: 129 //h q[6]
cx q[0],q[1]; //cycle: 130 //cx q[5],q[7]
rz(-0.7854) q[5]; //cycle: 130 //rz(-0.7854) q[6]
swap q[7],q[8]; //cycle: 131
rz(0.3927) q[0]; //cycle: 132 //rz(0.3927) q[5]
cx q[0],q[1]; //cycle: 133 //cx q[5],q[7]
rz(-0.19635) q[0]; //cycle: 135 //rz(-0.19635) q[5]
swap q[0],q[1]; //cycle: 136
cx q[8],q[3]; //cycle: 137 //cx q[3],q[9]
cx q[6],q[7]; //cycle: 137 //cx q[4],q[8]
rz(0.02455) q[8]; //cycle: 139 //rz(0.02455) q[3]
rz(0.09815) q[6]; //cycle: 139 //rz(0.09815) q[4]
cx q[8],q[3]; //cycle: 140 //cx q[3],q[9]
cx q[6],q[7]; //cycle: 140 //cx q[4],q[8]
swap q[2],q[3]; //cycle: 142
rz(-0.0491) q[6]; //cycle: 142 //rz(-0.0491) q[4]
cx q[1],q[7]; //cycle: 142 //cx q[5],q[8]
cx q[5],q[0]; //cycle: 142 //cx q[6],q[7]
h q[8]; //cycle: 142 //h q[3]
rz(0.19635) q[1]; //cycle: 144 //rz(0.19635) q[5]
rz(0.7854) q[5]; //cycle: 144 //rz(0.7854) q[6]
cx q[1],q[7]; //cycle: 145 //cx q[5],q[8]
cx q[5],q[0]; //cycle: 145 //cx q[6],q[7]
rz(-0.09815) q[1]; //cycle: 147 //rz(-0.09815) q[5]
rz(-0.3927) q[5]; //cycle: 147 //rz(-0.3927) q[6]
h q[0]; //cycle: 147 //h q[7]
swap q[1],q[7]; //cycle: 148
cx q[6],q[2]; //cycle: 148 //cx q[4],q[9]
rz(-0.7854) q[0]; //cycle: 148 //rz(-0.7854) q[7]
swap q[0],q[5]; //cycle: 149
rz(0.0491) q[6]; //cycle: 150 //rz(0.0491) q[4]
cx q[6],q[2]; //cycle: 151 //cx q[4],q[9]
h q[6]; //cycle: 153 //h q[4]
cx q[7],q[2]; //cycle: 154 //cx q[5],q[9]
cx q[0],q[1]; //cycle: 155 //cx q[6],q[8]
rz(0.09815) q[7]; //cycle: 156 //rz(0.09815) q[5]
cx q[7],q[2]; //cycle: 157 //cx q[5],q[9]
rz(0.3927) q[0]; //cycle: 157 //rz(0.3927) q[6]
cx q[0],q[1]; //cycle: 158 //cx q[6],q[8]
swap q[5],q[6]; //cycle: 159
h q[7]; //cycle: 159 //h q[5]
swap q[1],q[2]; //cycle: 160
rz(-0.19635) q[0]; //cycle: 160 //rz(-0.19635) q[6]
cx q[0],q[1]; //cycle: 166 //cx q[6],q[9]
cx q[6],q[2]; //cycle: 166 //cx q[7],q[8]
rz(0.19635) q[0]; //cycle: 168 //rz(0.19635) q[6]
rz(0.7854) q[6]; //cycle: 168 //rz(0.7854) q[7]
cx q[0],q[1]; //cycle: 169 //cx q[6],q[9]
cx q[6],q[2]; //cycle: 169 //cx q[7],q[8]
rz(-0.3927) q[6]; //cycle: 171 //rz(-0.3927) q[7]
h q[2]; //cycle: 171 //h q[8]
h q[0]; //cycle: 171 //h q[6]
cx q[6],q[1]; //cycle: 172 //cx q[7],q[9]
rz(-0.7854) q[2]; //cycle: 172 //rz(-0.7854) q[8]
rz(0.3927) q[6]; //cycle: 174 //rz(0.3927) q[7]
cx q[6],q[1]; //cycle: 175 //cx q[7],q[9]
cx q[2],q[1]; //cycle: 177 //cx q[8],q[9]
h q[6]; //cycle: 177 //h q[7]
rz(0.7854) q[2]; //cycle: 179 //rz(0.7854) q[8]
cx q[2],q[1]; //cycle: 180 //cx q[8],q[9]
h q[1]; //cycle: 182 //h q[9]
h q[2]; //cycle: 182 //h q[8]
h q[1]; //cycle: 183 //h q[9]
//200 original gates
//227 gates in generated circuit
//97 ideal depth (cycles)
//184 depth of generated circuit
//86315 nodes popped from queue for processing.
//1527 nodes remain in queue.
