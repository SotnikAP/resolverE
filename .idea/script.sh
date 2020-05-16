balm -c "read_para_fsm x|v|y|u /home/sotnik/QtPojects/build-FSMs-composition-tool-Desktop-Debug/1wait.aut poly1wait.aut" &>> log.txt
balm -c "read_para_fsm u|v /home/sotnik/QtPojects/build-FSMs-composition-tool-Desktop-Debug/1mach.aut poly1mach.aut" &>> log.txt
balm -c "chan_sync x|v|y|u|E u|v|E  poly1wait.aut poly1mach.aut syncpoly1wait.aut syncpoly1mach.aut" &>> log.txt
python3 main.py poly1wait.aut syncpoly1wait.aut poly1mach.aut syncpoly1mach.aut
sh edited_script.sh
exit 25

balm -c "expansion x,y syncpoly1mach.aut expsyncpoly1mach.aut"
balm -c "support x,v,y,u,E(4) expsyncpoly1mach.aut supexpsyncpoly1mach.aut" &>> log.txt
balm -c "product syncpoly1wait.aut supexpsyncpoly1mach.aut pro.aut" &>> log.txt
balm -c "restriction x,y pro.aut restr.aut" &>> log.txt
balm -c "support x,y,E(2) restr.aut supp.aut" &>> log.txt
balm -c "write_para_fsm x|y|E x|y supp.aut fsm.aut" &>> log.txt
