balm -c "read_para_fsm x|u|y|v /home/sotnik/QtPojects/build-FSMs-composition-tool-Desktop-Debug/1wait.aut poly1wait.aut"
balm -c "read_para_fsm v|u /home/sotnik/QtPojects/build-FSMs-composition-tool-Desktop-Debug/1mach.aut poly1mach.aut"
balm -c "chan_sync x|u|y|v|E v|u|E  poly1wait.aut poly1mach.aut syncpoly1wait.aut syncpoly1mach.aut"
python3 main.py poly1wait.aut syncpoly1wait.aut poly1mach.aut syncpoly1mach.aut
sh edited_script.sh
exit 25

balm -c "expansion x,y syncpoly1mach.aut expsyncpoly1mach.aut"
balm -c "support x,u,y,v,E(4) expsyncpoly1mach.aut supexpsyncpoly1mach.aut"
balm -c "product syncpoly1wait.aut supexpsyncpoly1mach.aut pro.aut"
balm -c "restriction x,y pro.aut restr.aut"
balm -c "support x,y,E(2) restr.aut supp.aut"
balm -c "write_para_fsm x|y|E x|y supp.aut fsm.aut"