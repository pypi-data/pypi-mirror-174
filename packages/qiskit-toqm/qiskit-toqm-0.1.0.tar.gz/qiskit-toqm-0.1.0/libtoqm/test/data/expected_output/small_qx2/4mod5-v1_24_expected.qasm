//Note: initial mapping (logical qubit at each location): 1, 3, 2, 0, 4, 
//Note: initial mapping (location of each logical qubit): 3, 0, 2, 1, 4, 
OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg c[5];
swap q[0],q[1]; //cycle: 0
x q[4]; //cycle: 0 //x q[4]
h q[3]; //cycle: 0 //h q[0]
t q[2]; //cycle: 0 //t q[2]
t q[4]; //cycle: 1 //t q[4]
t q[3]; //cycle: 1 //t q[0]
cx q[2],q[4]; //cycle: 2 //cx q[2],q[4]
cx q[3],q[2]; //cycle: 4 //cx q[0],q[2]
cx q[0],q[1]; //cycle: 6 //cx q[3],q[1]
cx q[4],q[3]; //cycle: 6 //cx q[4],q[0]
tdg q[2]; //cycle: 6 //tdg q[2]
cx q[4],q[2]; //cycle: 8 //cx q[4],q[2]
swap q[0],q[1]; //cycle: 8
t q[3]; //cycle: 8 //t q[0]
tdg q[4]; //cycle: 10 //tdg q[4]
tdg q[2]; //cycle: 10 //tdg q[2]
cx q[3],q[2]; //cycle: 11 //cx q[0],q[2]
cx q[4],q[3]; //cycle: 13 //cx q[4],q[0]
cx q[2],q[4]; //cycle: 15 //cx q[2],q[4]
h q[3]; //cycle: 15 //h q[0]
t q[3]; //cycle: 16 //t q[0]
swap q[0],q[2]; //cycle: 17
swap q[3],q[4]; //cycle: 17
cx q[2],q[3]; //cycle: 23 //cx q[1],q[4]
x q[2]; //cycle: 25 //x q[1]
h q[3]; //cycle: 25 //h q[4]
t q[2]; //cycle: 26 //t q[1]
t q[3]; //cycle: 26 //t q[4]
cx q[4],q[2]; //cycle: 27 //cx q[0],q[1]
cx q[3],q[4]; //cycle: 29 //cx q[4],q[0]
cx q[2],q[3]; //cycle: 31 //cx q[1],q[4]
tdg q[4]; //cycle: 31 //tdg q[0]
cx q[2],q[4]; //cycle: 33 //cx q[1],q[0]
t q[3]; //cycle: 33 //t q[4]
tdg q[2]; //cycle: 35 //tdg q[1]
tdg q[4]; //cycle: 35 //tdg q[0]
cx q[3],q[4]; //cycle: 36 //cx q[4],q[0]
cx q[2],q[3]; //cycle: 38 //cx q[1],q[4]
cx q[4],q[2]; //cycle: 40 //cx q[0],q[1]
h q[3]; //cycle: 40 //h q[4]
//36 original gates
//40 gates in generated circuit
//36 ideal depth (cycles)
//42 depth of generated circuit
//2196 nodes popped from queue for processing.
//2661 nodes remain in queue.
//HashFilter filtered 2864 total nodes.
//HashFilter2 filtered 1574 total nodes.
//HashFilter2 marked 2391 total nodes.
