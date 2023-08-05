OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
h q[0];
rz(-0.7854) q[0];
cx q[0],q[1];
rz(0.7854) q[0];
cx q[0],q[1];
rz(-0.3927) q[0];
cx q[0],q[2];
rz(0.3927) q[0];
cx q[0],q[2];
rz(-0.19635) q[0];
cx q[0],q[3];
rz(0.19635) q[0];
cx q[0],q[3];
rz(-0.09815) q[0];
cx q[0],q[4];
rz(0.09815) q[0];
cx q[0],q[4];
rz(-0.0491) q[0];
cx q[0],q[5];
rz(0.0491) q[0];
cx q[0],q[5];
rz(-0.02455) q[0];
cx q[0],q[6];
rz(0.02455) q[0];
cx q[0],q[6];
rz(-0.01225) q[0];
cx q[0],q[7];
rz(0.01225) q[0];
cx q[0],q[7];
rz(-0.00615) q[0];
cx q[0],q[8];
rz(0.00615) q[0];
cx q[0],q[8];
rz(-0.00305) q[0];
cx q[0],q[9];
rz(0.00305) q[0];
cx q[0],q[9];
h q[1];
rz(-0.7854) q[1];
cx q[1],q[2];
rz(0.7854) q[1];
cx q[1],q[2];
rz(-0.3927) q[1];
cx q[1],q[3];
rz(0.3927) q[1];
cx q[1],q[3];
rz(-0.19635) q[1];
cx q[1],q[4];
rz(0.19635) q[1];
cx q[1],q[4];
rz(-0.09815) q[1];
cx q[1],q[5];
rz(0.09815) q[1];
cx q[1],q[5];
rz(-0.0491) q[1];
cx q[1],q[6];
rz(0.0491) q[1];
cx q[1],q[6];
rz(-0.02455) q[1];
cx q[1],q[7];
rz(0.02455) q[1];
cx q[1],q[7];
rz(-0.01225) q[1];
cx q[1],q[8];
rz(0.01225) q[1];
cx q[1],q[8];
rz(-0.00615) q[1];
cx q[1],q[9];
rz(0.00615) q[1];
cx q[1],q[9];
h q[2];
rz(-0.7854) q[2];
cx q[2],q[3];
rz(0.7854) q[2];
cx q[2],q[3];
rz(-0.3927) q[2];
cx q[2],q[4];
rz(0.3927) q[2];
cx q[2],q[4];
rz(-0.19635) q[2];
cx q[2],q[5];
rz(0.19635) q[2];
cx q[2],q[5];
rz(-0.09815) q[2];
cx q[2],q[6];
rz(0.09815) q[2];
cx q[2],q[6];
rz(-0.0491) q[2];
cx q[2],q[7];
rz(0.0491) q[2];
cx q[2],q[7];
rz(-0.02455) q[2];
cx q[2],q[8];
rz(0.02455) q[2];
cx q[2],q[8];
rz(-0.01225) q[2];
cx q[2],q[9];
rz(0.01225) q[2];
cx q[2],q[9];
h q[3];
rz(-0.7854) q[3];
cx q[3],q[4];
rz(0.7854) q[3];
cx q[3],q[4];
rz(-0.3927) q[3];
cx q[3],q[5];
rz(0.3927) q[3];
cx q[3],q[5];
rz(-0.19635) q[3];
cx q[3],q[6];
rz(0.19635) q[3];
cx q[3],q[6];
rz(-0.09815) q[3];
cx q[3],q[7];
rz(0.09815) q[3];
cx q[3],q[7];
rz(-0.0491) q[3];
cx q[3],q[8];
rz(0.0491) q[3];
cx q[3],q[8];
rz(-0.02455) q[3];
cx q[3],q[9];
rz(0.02455) q[3];
cx q[3],q[9];
h q[4];
rz(-0.7854) q[4];
cx q[4],q[5];
rz(0.7854) q[4];
cx q[4],q[5];
rz(-0.3927) q[4];
cx q[4],q[6];
rz(0.3927) q[4];
cx q[4],q[6];
rz(-0.19635) q[4];
cx q[4],q[7];
rz(0.19635) q[4];
cx q[4],q[7];
rz(-0.09815) q[4];
cx q[4],q[8];
rz(0.09815) q[4];
cx q[4],q[8];
rz(-0.0491) q[4];
cx q[4],q[9];
rz(0.0491) q[4];
cx q[4],q[9];
h q[5];
rz(-0.7854) q[5];
cx q[5],q[6];
rz(0.7854) q[5];
cx q[5],q[6];
rz(-0.3927) q[5];
cx q[5],q[7];
rz(0.3927) q[5];
cx q[5],q[7];
rz(-0.19635) q[5];
cx q[5],q[8];
rz(0.19635) q[5];
cx q[5],q[8];
rz(-0.09815) q[5];
cx q[5],q[9];
rz(0.09815) q[5];
cx q[5],q[9];
h q[6];
rz(-0.7854) q[6];
cx q[6],q[7];
rz(0.7854) q[6];
cx q[6],q[7];
rz(-0.3927) q[6];
cx q[6],q[8];
rz(0.3927) q[6];
cx q[6],q[8];
rz(-0.19635) q[6];
cx q[6],q[9];
rz(0.19635) q[6];
cx q[6],q[9];
h q[7];
rz(-0.7854) q[7];
cx q[7],q[8];
rz(0.7854) q[7];
cx q[7],q[8];
rz(-0.3927) q[7];
cx q[7],q[9];
rz(0.3927) q[7];
cx q[7],q[9];
h q[8];
rz(-0.7854) q[8];
cx q[8],q[9];
rz(0.7854) q[8];
cx q[8],q[9];
h q[9];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[6];
h q[7];
h q[8];
h q[9];
