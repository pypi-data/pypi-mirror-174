OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];
t q[4];
t q[5];
h q[6];
cx q[5],q[6];
tdg q[6];
cx q[3],q[6];
t q[6];
cx q[5],q[6];
cx q[3],q[5];
tdg q[5];
cx q[3],q[5];
h q[5];
cx q[4],q[5];
tdg q[5];
cx q[2],q[5];
t q[5];
cx q[4],q[5];
cx q[2],q[4];
tdg q[4];
cx q[2],q[4];
h q[4];
cx q[1],q[4];
tdg q[4];
cx q[0],q[4];
t q[4];
cx q[1],q[4];
tdg q[4];
cx q[0],q[4];
t q[4];
h q[4];
cx q[4],q[5];
tdg q[5];
cx q[2],q[5];
t q[5];
cx q[4],q[5];
h q[5];
cx q[5],q[6];
tdg q[6];
cx q[3],q[6];
t q[6];
cx q[5],q[6];
cx q[3],q[5];
h q[6];
t q[5];
cx q[3],q[5];
tdg q[5];
h q[5];
cx q[4],q[5];
tdg q[5];
cx q[2],q[5];
t q[5];
cx q[4],q[5];
h q[4];
cx q[1],q[4];
t q[4];
cx q[0],q[4];
tdg q[4];
cx q[1],q[4];
t q[4];
cx q[0],q[4];
tdg q[4];
h q[4];
cx q[4],q[5];
tdg q[5];
cx q[2],q[5];
t q[5];
cx q[4],q[5];
cx q[2],q[4];
h q[5];
t q[4];
cx q[2],q[4];
tdg q[4];
