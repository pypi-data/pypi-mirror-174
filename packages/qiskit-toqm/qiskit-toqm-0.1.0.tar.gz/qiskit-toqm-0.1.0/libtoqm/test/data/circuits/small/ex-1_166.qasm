OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
cx q[0],q[1];
h q[0];
t q[1];
t q[2];
t q[0];
cx q[2],q[1];
cx q[0],q[2];
cx q[1],q[0];
tdg q[2];
cx q[1],q[2];
tdg q[1];
tdg q[2];
t q[0];
cx q[0],q[2];
cx q[1],q[0];
cx q[2],q[1];
h q[0];
cx q[0],q[1];
x q[0];
