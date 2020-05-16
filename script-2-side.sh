balm -c "read_para_fsm i|u|o|v /home/sotnik/QtPojects/build-FSMs-composition-tool-Desktop-Debug/2-side/Aut2.aut polyAut2.aut"
balm -c "read_para_fsm x|v|y|u /home/sotnik/QtPojects/build-FSMs-composition-tool-Desktop-Debug/2-side/Aut1.aut polyAut1.aut"
balm -c "chan_sync x|v|y|u|E i|u|o|v|E  polyAut1.aut polyAut2.aut syncpolyAut1.aut syncpolyAut2.aut"
python3 main.py polyAut2.aut syncpolyAut2.aut polyAut1.aut syncpolyAut1.aut
sh edited_script.sh
exit 25
balm -c "expansion x,y syncpolyAut2.aut expsyncpolyAut2.aut"
balm -c "expansion i,o syncpolyAut1.aut expsyncpolyAut1.aut"
balm -c "support x,v,y,u,E(4) expsyncpolyAut2.aut supexpsyncpolyAut2.aut"
balm -c "product expsyncpolyAut1.aut supexpsyncpolyAut2.aut pro.aut"
balm -c "restriction x,i,y,o pro.aut restr.aut"
balm -c "support i,x,o,y,E(4) restr.aut supp.aut"
balm -c "write_para_fsm i|x|o|y|E x|i|y|o supp.aut fsm.aut"