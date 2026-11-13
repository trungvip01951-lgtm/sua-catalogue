# vẽ 8 biểu đồ (EN/VI × 150/200 × nhóm A/B) + 2 bảng; chạy từ gốc kho
W=$HOME/claude_work/wcl; PY=$HOME/cfenv/bin/python
for dn in 150 200; do
 [ $dn = 150 ] && A=150WC200-35-37,150WC180-50-55,150WC200-60-75,150WC200-70-90 B=150WC200-40-45,150WC180-80-110,150WC200-90-132
 [ $dn = 200 ] && A=200WC350-22-37,200WC300-32-45,200WC300-40-55,200WC300-60-90 B=200WC350-45-75,200WC300-65-110,200WC400-75-132
 for g in a b; do M=$([ $g = a ] && echo $A || echo $B)
  $PY -B -X utf8 tools/ve_duong_cong.py --du-lieu $W/WCL_$dn.xlsx --hang REDPUMP --ra $W/qh/en_bd$dn$g.pdf --kieu bieu_do --rong-pt 266 --cao-pt 262 --khong-tieu-de --model $M 2>&1 | grep "^ĐẠT\|KHÔNG\|LỖI" | cut -c1-120
  $PY -B -X utf8 tools/ve_duong_cong.py --du-lieu $W/WCL_$dn.xlsx --hang REDPUMP --ra $W/qh/vi_bd$dn$g.pdf --kieu bieu_do --rong-pt 266 --cao-pt 262 --khong-tieu-de --model $M --ho-so $W/HO_SO_VI_$dn.json 2>&1 | grep "^ĐẠT\|KHÔNG\|LỖI" | cut -c1-120
 done
 $PY -B -X utf8 tools/ve_duong_cong.py --du-lieu $W/WCL_$dn.xlsx --hang REDPUMP --ra $W/qh/bang$dn.pdf --kieu bang --rong-pt 540 --khong-tieu-de 2>&1 | grep "^ĐẠT\|KHÔNG\|LỖI" | cut -c1-120
done
