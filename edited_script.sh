balm -c "expansion E0,E2 syncpoly1mach.aut expsyncpoly1mach.aut"
sleep 1
balm -c "support x,u,v,y,E(4) expsyncpoly1mach.aut supexpsyncpoly1mach.aut"
sleep 1
balm -c "product syncpoly1wait.aut supexpsyncpoly1mach.aut pro.aut"
sleep 1
balm -c "restriction E0,E2 pro.aut restr.aut"
sleep 1
balm -c "support x,y,E(2) restr.aut supp.aut"
sleep 1
balm -c "write_para_fsm x|y|E E0|E2 supp.aut fsm.aut"
sleep 1
