import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

os.makedirs("./data", exist_ok=True)

DOCUMENTS = [
    {
        "filename": "./data/Noi_quy_lao_dong.pdf",
        "title": "NOI QUY LAO DONG VA KY LUAT",
        "sections": [
            ("Dieu 1: Thoi gian lam viec", "Thoi gian lam viec tieu chuan la 8 gio moi ngay, tu thu Hai den thu Sau. Gio bat dau tu 8:30 sang va ket thuc vao 17:30 chieu. Nghi trua tu 12:00 den 13:00. Nhan vien can quet van tay hoac diem danh qua ung dung cham cong truoc 8:30."),
            ("Dieu 2: Trang phuc cong so", "Nhan vien mac trang phuc lich su tu thu Hai den thu Nam. Thu Sau duoc phep mac trang phuc thoai mai (Casual Friday) nhung van phai dam bao tinh trang nha va lich su."),
            ("Dieu 3: Xu ly vi pham ky luat", "Di muon qua 3 lan trong mot thang khong co ly do chinh dang se bi nhac nho bang van ban. Vi pham tiet lo bi mat kinh doanh se bi sa thai ngay lap tuc ma khong can bao truoc theo quy dinh phap luat.")
        ]
    },
    {
        "filename": "./data/So_tay_nhan_vien.pdf",
        "title": "SO TAY NHAN VIEN VA VAN HOA DOANH NGHIEP",
        "sections": [
            ("Chuong 1: Gia tri cot loi", "Cong ty hoat dong dua tren ba gia tri cot loi: Minh bach, Sang tao va Trach nhiem. Chung toi khuyen khich moi thanh vien dong gop y kien thang than trong cac buoi hop tong ket hang thang."),
            ("Chuong 2: Che do thu viec", "Thoi gian thu viec tieu chuan keo dai 02 thang doi voi vi tri chuyen mon. Trong thoi gian nay, muc luong thu viec toi thieu bang 85% muc luong chinh thuc. Danh gia thu viec dien ra vao tuan thu 7."),
            ("Chuong 3: Cap phat thiet bi lam viec", "Moi nhan vien chinh thuc duoc cap mot may tinh xach tay phuc vu cong viec. Nhan vien co trach nhiem bao quan thiet bi va ban giao lai cho phong IT khi nghi viec.")
        ]
    },
    {
        "filename": "./data/Quy_dinh_nghi_phep_va_phuc_loi.pdf",
        "title": "QUY DINH NGHI PHEP VA PHUC LOI",
        "sections": [
            ("Dieu 4: Phep nam tieu chuan", "Moi nhan vien chinh thuc duoc nghi phep 12 ngay/nam co huong nguyen luong. Nhan vien lam viec du 5 nam se duoc cong them 1 ngay phep nam vao quy phep hang nam."),
            ("Dieu 5: Bao luu ngay phep", "Phep nam chua su dung het trong nam hien tai duoc phep bao luu toi da 5 ngay va phai duoc su dung truoc ngay 31 thang 3 cua nam tiep theo. Sau thoi han nay, phep con lai se tu dong het han."),
            ("Dieu 6: Che do bao hiem mo rong", "Ngoai bao hiem y te bat buoc, cong ty cung cap goi bao hiem suc khoe PVI Care cho toan bo nhan vien chinh thuc sau khi ky hop dong lao dong khong xac dinh thoi han.")
        ]
    },
    {
        "filename": "./data/Huong_dan_an_toan_thong_tin.pdf",
        "title": "HUONG DAN AN TOAN THONG TIN",
        "sections": [
            ("Muc 1: Quan ly mat khau", "Mat khau tai khoan noi bo phai co do dai toi thieu 12 ky tu, bao gom chu hoa, chu thuong, chu so va ky tu dac biet. Mat khau bat buoc thay doi dinh ky 90 ngay mot lan."),
            ("Muc 2: Xac thuc hai yeu to (2FA)", "Tat ca cac he thong bao gom Email cong ty, Github va Portal noi bo deu bat buoc phai kich hoat xac thuc 2 lop thong qua Google Authenticator."),
            ("Muc 3: Quy dinh thiet bi ca nhan (BYOD)", "Khong duoc sao chep du lieu khach hang hoac ma nguon du an vao USB ca nhan. Khi ket noi vao mang cong ty bang thiet bi ca nhan, phai thong qua mang WiFi khach (Guest).")
        ]
    },
    {
        "filename": "./data/Quy_trinh_cong_tac_phi.pdf",
        "title": "QUY TRINH CONG TAC PHI VA QUYET TOAN",
        "sections": [
            ("Buoc 1: Dang ky cong tac", "Nhan vien can lap giay de nghi cong tac truoc it nhat 03 ngay lam viec va duoc Quan ly truc tiep phe duyet truoc khi tien hanh chuyen di."),
            ("Buoc 2: Dinh muc luu tru va an uong", "Dinh muc khach san tai Ha Noi va TP. Ho Chi Minh toi da 1.200.000 VND/dem. Cac tinh thanh khac toi da 700.000 VND/dem. Phu cap tien an (Per Diem) la 250.000 VND/ngay."),
            ("Buoc 3: Ho so va han quyet toan", "Trong vong 07 ngay lam viec ke tu ngay ket thuc cong tac, nhan vien phai nop toan bo hoa don do (VAT), the len may bay va giay de nghi thanh toan cho phong Ke toan.")
        ]
    }
]

def build_pdf(doc_data):
    doc = SimpleDocTemplate(doc_data["filename"], pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        spaceAfter=14
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = styles['Normal']
    body_style.fontSize = 10
    body_style.leading = 14

    story = []
    # Title
    story.append(Paragraph(doc_data["title"], title_style))
    story.append(Spacer(1, 10))

    # Sections
    for heading, content in doc_data["sections"]:
        story.append(Paragraph(heading, h2_style))
        story.append(Paragraph(content, body_style))
        story.append(Spacer(1, 8))

    doc.build(story)
    print(f"-> Da tao xong: {doc_data['filename']}")

if __name__ == "__main__":
    for item in DOCUMENTS:
        build_pdf(item)
    print("\nTao thanh cong toan bo 5 file PDF trong thu muc ./data!")