# Logo và bảng SP6 theo yêu cầu mới

ĐẠT riêng logo/bảng/chú thích sửa mới, có kiểm độc lập trên PDF thật. Toàn trang CHƯA ĐẠT vì nhãn đồ thị cũ còn lỗi và một điểm vượt cách đo sai lệch5% mới. Bản chính không đổi.

| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| NEW-LOGO | SP | 6 | Logo nhỏ, ô nền xanh | Logo Perotac rõ, nền trắng đồng nhất | Dùng nguyên tài sản1041×356 từcatalogueWC gốc cùngthươnghiệu,giữbyte | ĐẠT độc lập | KIEM DOC LAP.md,KIEM TRA LOGO BANG.json |
| NEW-TABLE | SP | 6 | Bảng thiếu nhómQ/H trực quan,đầu bảng chưa rõkhung | MODEL/P₂/DELIVERY;pha/điện/kW/HP;Qhaihàngm³/h vàl/min;H(m) riêng | Dựng lạiheader/cácôbằngvectorcatfix | ĐẠT độc lập | PDF vàKIEM DOC LAP.md |
| NEW-NUM | SP | 6 | 39mã/426H ởmẫu2 | 39mã/426H giữđúngtừngô | ĐọcchữtrongPDF đãlưu,không đổithôngsố | ĐẠT trong phạm vi kiểm | 0ôlệch |
| NEW-SYMBOL | SP | 6 | n=2850,thiếuP2 | n≈2850,P₂ khôi phục | Chữnhúng/haicỡchữchochỉsốdưới | ĐẠT độc lập | PDF thật |
| HOLD-PLOT | SP | 6 | Nhãn cũFAIL/STOP2 | Đường,nhãn vàη nguyênmẫu2 | Không thửlại cáchđặtnhãn;chỉđổiheader/table | Bảo toànĐẠT;nhãnCHƯAĐẠT | Plotpixel180/200dpi trùng |
| NEW-95 | SP | 6 | Ngưỡngriêngcũmax(1m,2%H) | Diễngiảiyêucầu95% thànhlệch≤5% tại mỗiQ/H>0 | Sànglọc426mốc,giữkhóavàkhôngnớingưỡngcũ | 425/426đạt5%;1điểmcầnchỉnh | 6SP36-2,Q48,Hbảng14,Hđường13.222222,lệch5.555556% |
| NEW-POWER | SP | 6 | Anh nhắc cócặp côngsuất ngược đểsửasau | Lưuluậtso cùngdòng/cùngđiềukiện;chỉsànglọcđiểmbảngtrang6 | Không tựđổikW/H/Q | 0cặp ngược ởđiểmbảngđãkiểm;phầnkhácCHƯAKIỂM | CONG SUAT CAN RA SOAT SAU.json |
| HOLD-SOURCE | SP | 1–12 | Nguồn/bảnchính và11trangkhác | Nguyênbyte50tệpnguồn/bảnchính;11trangkhácgiữhình | SHA,render100dpi,metadata/link/mụclục/khổ | ĐẠT phạmvikiểm | Hồsơclose,KIEM TRA LOGO BANG.json |

Tệp SP6 - LOGO VA BANG MOI.pdf là bảnxem1trang; bản12trang giữcatalogueđầyđủvớimẫuởtrang6. Đây làứngviênriêng,khôngbảnpháthành. Khôngđổi426số ởlượtnày;haiôH đãsửa trongmẫu2vẫnchưađượctiếpnhậnvàobảnchính. Chưa kiểm bảnin giấy. 95% là cáchđoAI đãnêurõ, khôngkhẳngđịnhanhđãcho nguyênvăncôngthức.

Đã lưu vào thư viện templates/catalogue/SP6_LOGO_TABLE_V2 với dữliệu, mapô, logo nguồn, mãthamkhảo và trạngthái. V1 giữlạivàkhôngđượccoi là mẫuđãđạt.
