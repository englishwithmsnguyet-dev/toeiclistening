import json
import re

# Data extracted from VSTEP PDF
VOCAB_DATA = {
    "dang_01_identity": [
        {
            "category": "LĨNH VỰC GIÁO DỤC",
            "items": [
                ("teacher", "/ˈtiː.tʃər/ (n)", "giáo viên"),
                ("professor", "/prəˈfes.ər/ (n)", "giáo sư"),
                ("tutor", "/ˈtʃuː.tər/ (n)", "gia sư"),
                ("lecturer", "/ˈlek.tʃər.ər/ (n)", "giảng viên đại học"),
                ("principal", "/ˈprɪn.sə.pəl/ (n)", "hiệu trưởng (trường phổ thông)"),
                ("dean", "/diːn/ (n)", "trưởng khoa"),
                ("librarian", "/laɪˈbreə.ri.ən/ (n)", "thủ thư"),
                ("teaching assistant", "/ˈtiː.tʃɪŋ əˌsɪs.tənt/ (n)", "trợ giảng"),
                ("academic advisor", "/ˌæk.əˈdem.ɪk ədˈvaɪ.zər/ (n)", "cố vấn học tập"),
                ("school counselor", "/ˈskuːl ˌkaʊn.səl.ər/ (n)", "chuyên viên tư vấn học đường")
            ]
        },
        {
            "category": "LĨNH VỰC KHOA HỌC – NGHIÊN CỨU",
            "items": [
                ("scientist", "/ˈsaɪən.tɪst/ (n)", "nhà khoa học"),
                ("researcher", "/rɪˈsɜː.tʃər/ (n)", "nhà nghiên cứu"),
                ("lab technician", "/læb tekˈnɪʃ.ən/ (n)", "kỹ thuật viên phòng thí nghiệm"),
                ("chemist", "/ˈkem.ɪst/ (n)", "nhà hóa học"),
                ("biologist", "/baɪˈɒl.ə.dʒɪst/ (n)", "nhà sinh vật học"),
                ("physicist", "/ˈfɪz.ɪ.sɪst/ (n)", "nhà vật lý học"),
                ("ecologist", "/iˈkɒl.ə.dʒɪst/ (n)", "nhà sinh thái học"),
                ("data analyst", "/ˈdeɪ.tə ˌæn.ə.lɪst/ (n)", "nhà phân tích dữ liệu")
            ]
        },
        {
            "category": "LĨNH VỰC Y TẾ",
            "items": [
                ("doctor", "/ˈdɒk.tər/ (n)", "bác sĩ"),
                ("nurse", "/nɜːs/ (n)", "y tá"),
                ("surgeon", "/ˈsɜː.dʒən/ (n)", "bác sĩ phẫu thuật"),
                ("pharmacist", "/ˈfɑː.mə.sɪst/ (n)", "dược sĩ"),
                ("dentist", "/ˈden.tɪst/ (n)", "nha sĩ"),
                ("therapist", "/ˈθer.ə.pɪst/ (n)", "chuyên viên trị liệu"),
                ("paramedic", "/ˌpær.əˈmed.ɪk/ (n)", "nhân viên cấp cứu"),
                ("medical assistant", "/ˈmed.ɪ.kəl əˈsɪs.tənt/ (n)", "trợ lý y tế"),
                ("receptionist", "/rɪˈsep.ʃən.ɪst/ (n)", "nhân viên lễ tân"),
                ("lab technician", "/læb tekˈnɪʃ.ən/ (n)", "kỹ thuật viên phòng thí nghiệm"),
                ("dietician", "/ˌdaɪ.əˈtɪʃ.ən/ (n)", "chuyên gia dinh dưỡng"),
                ("physician", "/fɪˈzɪʃ.ən/ (n)", "bác sĩ điều trị (nội khoa)")
            ]
        },
        {
            "category": "LĨNH VỰC KINH DOANH – HÀNH CHÍNH",
            "items": [
                ("manager", "/ˈmæn.ɪ.dʒər/ (n)", "quản lý"),
                ("accountant", "/əˈkaʊn.tənt/ (n)", "kế toán"),
                ("supervisor", "/ˈsuː.pə.vaɪ.zər/ (n)", "giám sát viên"),
                ("director", "/daɪˈrek.tər/ (n)", "giám đốc"),
                ("assistant", "/əˈsɪs.tənt/ (n)", "trợ lý"),
                ("executive", "/ɪɡˈzek.jə.tɪv/ (n)", "nhân viên điều hành"),
                ("business analyst", "/ˈbɪz.nəs ˌæn.ə.lɪst/ (n)", "nhà phân tích kinh doanh"),
                ("employee / clerk", "/ɪmˈplɔɪ.iː/ / /klɑːk/ (n)", "nhân viên"),
                ("HR officer", "/ˌeɪtʃ ˈɑː ˈɒf.ɪ.sər/ (n)", "nhân viên nhân sự"),
                ("consultant", "/kənˈsʌl.tənt/ (n)", "cố vấn"),
                ("secretary", "/ˈsek.rə.tri/ (n)", "thư ký"),
                ("financial advisor", "/faɪˈnæn.ʃəl ədˈvaɪ.zər/ (n)", "cố vấn tài chính")
            ]
        },
        {
            "category": "LĨNH VỰC DỊCH VỤ – BÁN HÀNG",
            "items": [
                ("cashier", "/kæʃˈɪər/ (n)", "thu ngân"),
                ("store clerk", "/stɔː klɑːk/ (n)", "nhân viên bán hàng (trong cửa hàng)"),
                ("store owner", "/stɔːr ˈəʊ.nər/ (n)", "chủ cửa hàng"),
                ("waiter / waitress", "/ˈweɪ.tər/ / /ˈweɪ.trəs/ (n)", "phục vụ bàn"),
                ("barista", "/bəˈriː.stə/ (n)", "nhân viên pha chế cà phê"),
                ("salesperson", "/ˈseɪlzˌpɜː.sən/ (n)", "nhân viên bán hàng"),
                ("delivery person", "/dɪˈlɪv.ər.i ˌpɜː.sən/ (n)", "nhân viên giao hàng"),
                ("receptionist", "/rɪˈsep.ʃən.ɪst/ (n)", "nhân viên lễ tân"),
                ("customer service rep", "/ˈkʌs.tə.mər ˈsɜː.vɪs rep/ (n)", "nhân viên CSKH"),
                ("housekeeper", "/ˈhaʊsˌkiː.pər/ (n)", "nhân viên dọn phòng"),
                ("caterer", "/ˈkeɪ.tər.ər/ (n)", "người cung cấp dịch vụ ăn uống"),
                ("concierge", "/ˌkɒn.siˈeəʒ/ (n)", "nhân viên hỗ trợ khách sạn")
            ]
        },
        {
            "category": "LĨNH VỰC CÔNG NGHỆ – TRUYỀN THÔNG",
            "items": [
                ("technician", "/tekˈnɪʃ.ən/ (n)", "kỹ thuật viên"),
                ("programmer", "/ˈprəʊ.ɡræm.ər/ (n)", "lập trình viên"),
                ("IT specialist", "/ˌaɪˈtiː ˈspeʃ.əl.ɪst/ (n)", "chuyên viên công nghệ thông tin"),
                ("web developer", "/web dɪˈvel.ə.pər/ (n)", "lập trình viên web"),
                ("designer", "/dɪˈzaɪ.nər/ (n)", "nhà thiết kế"),
                ("editor", "/ˈed.ɪ.tər/ (n)", "biên tập viên"),
                ("journalist", "/ˈdʒɜː.nə.lɪst/ (n)", "nhà báo"),
                ("photographer", "/fəˈtɒɡ.rə.fər/ (n)", "nhiếp ảnh gia"),
                ("publisher", "/ˈpʌb.lɪ.ʃər/ (n)", "nhà xuất bản"),
                ("broadcaster", "/ˈbrɔːdˌkɑː.stər/ (n)", "phát thanh viên"),
                ("news reporter", "/njuːz rɪˈpɔː.tər/ (n)", "phóng viên"),
                ("sound engineer", "/saʊnd ˌen.dʒɪˈnɪər/ (n)", "kỹ sư âm thanh")
            ]
        },
        {
            "category": "LĨNH VỰC XÂY DỰNG – GIAO THÔNG",
            "items": [
                ("architect", "/ˈɑː.kɪ.tekt/ (n)", "kiến trúc sư"),
                ("civil engineer", "/ˈsɪv.əl ˌen.dʒɪˈnɪər/ (n)", "kỹ sư xây dựng dân dụng"),
                ("construction worker", "/kənˈstrʌk.ʃən ˌwɜː.kər/ (n)", "công nhân xây dựng"),
                ("site supervisor", "/saɪt ˈsuː.pə.vaɪ.zər/ (n)", "giám sát công trình"),
                ("project manager", "/ˈprɒ.dʒekt ˈmæn.ɪ.dʒər/ (n)", "quản lý dự án"),
                ("crane operator", "/kreɪn ˈɒp.ər.eɪ.tər/ (n)", "người điều khiển cần cẩu"),
                ("plumber", "/ˈplʌm.ər/ (n)", "thợ sửa ống nước"),
                ("electrician", "/ɪˌlekˈtrɪʃ.ən/ (n)", "thợ điện"),
                ("welder", "/ˈwel.dər/ (n)", "thợ hàn"),
                ("bricklayer", "/ˈbɪkˌleɪ.ər/ (n)", "thợ xây"),
                ("truck driver", "/trʌk ˈdraɪ.vər/ (n)", "tài xế xe tải"),
                ("delivery driver", "/dɪˈlɪv.ər.i ˈdraɪ.vər/ (n)", "tài xế giao hàng"),
                ("bus driver", "/bʌs ˈdraɪ.vər/ (n)", "tài xế xe buýt"),
                ("taxi driver", "/ˈtæk.si ˈdraɪ.vər/ (n)", "tài xế taxi"),
                ("train conductor", "/treɪn kənˈdʌk.tər/ (n)", "trưởng tàu"),
                ("pilot", "/ˈpaɪ.lət/ (n)", "phi công"),
                ("mechanic", "/məˈkæn.ɪk/ (n)", "thợ máy"),
                ("road maintenance worker", "/rəʊd ˈmeɪn.tə.nəns ˌwɜː.kər/ (n)", "công nhân bảo trì đường"),
                ("traffic controller", "/ˈtræf.ɪk kənˌtrəʊ.lər/ (n)", "nhân viên điều phối giao thông"),
                ("forklift operator", "/'fɔː.klɪft ˈɒp.ər.eɪ.tər/ (n)", "người lái xe nâng"),
                ("building contractor", "/ˈbɪl.dɪŋ kənˈtræk.tər/ (n)", "nhà thầu xây dựng"),
                ("building inspector", "/ˈbɪl.dɪŋ ɪnˈspek.tər/ (n)", "thanh tra xây dựng")
            ]
        },
        {
            "category": "LĨNH VỰC NGHỆ THUẬT – GIẢI TRÍ",
            "items": [
                ("artist", "/ˈɑː.tɪst/ (n)", "họa sĩ / nghệ sĩ"),
                ("actor", "/ˈæk.tər/ (n)", "nam diễn viên"),
                ("actress", "/ˈæk.trəs/ (n)", "nữ diễn viên"),
                ("singer", "/ˈsɪŋ.ər/ (n)", "ca sĩ"),
                ("musician", "/mjuˈzɪʃ.ən/ (n)", "nhạc công"),
                ("dancer", "/ˈdɑːn.sər/ (n)", "vũ công"),
                ("composer", "/kəmˈpəʊ.zər/ (n)", "nhà soạn nhạc"),
                ("film director", "/ˈfɪlm daɪˈrek.tər/ (n)", "đạo diễn phim"),
                ("producer", "/prəˈdʒuː.sər/ (n)", "nhà sản xuất"),
                ("model", "/ˈmɒd.əl/ (n)", "người mẫu")
            ]
        },
        {
            "category": "LĨNH VỰC LUẬT – CHÍNH PHỦ",
            "items": [
                ("lawyer", "/ˈlɔɪ.ər/ (n)", "luật sư"),
                ("judge", "/dʒʌdʒ/ (n)", "thẩm phán"),
                ("police officer", "/pəˈliːs ˌɒf.ɪ.sər/ (n)", "cảnh sát"),
                ("detective", "/dɪˈtek.tɪv/ (n)", "thám tử"),
                ("soldier", "/ˈsəʊl.dʒər/ (n)", "người lính"),
                ("government official", "/ˈɡʌv.ən.mənt əˈfɪʃ.əl/ (n)", "cán bộ nhà nước (viên chức, cán bộ bổ nhiệm)"),
                ("firefighter", "/ˈfaɪəˌfaɪ.tər/ (n)", "lính cứu hỏa"),
                ("security guard", "/sɪˈkjʊə.rə.ti ɡɑːd/ (n)", "nhân viên bảo vệ"),
                ("civil servant", "/ˌsɪv.əl ˈsɜː.vənt/ (n)", "công chức chính phủ"),
                ("mayor", "/meər/ (n)", "thị trưởng"),
                ("politician", "/ˌpɒl.ɪˈtɪʃ.ən/ (n)", "chính trị gia"),
                ("town official", "/taʊn əˈfɪʃ.əl/ (n)", "cán bộ/quan chức địa phương")
            ]
        },
        {
            "category": "LĨNH VỰC THỦ CÔNG – KỸ THUẬT",
            "items": [
                ("carpenter", "/ˈkɑː.pɪn.tər/ (n)", "thợ mộc"),
                ("blacksmith", "/ˈblæk.smɪθ/ (n)", "thợ rèn"),
                ("tailor", "/ˈteɪ.lər/ (n)", "thợ may"),
                ("shoemaker", "/ˈʃuːˌmeɪ.kər/ (n)", "thợ đóng giày"),
                ("repair technician", "/rɪˈpeər tekˈnɪʃ.ən/ (n)", "kỹ thuật viên sửa chữa"),
                ("locksmith", "/ˈlock.smɪθ/ (n)", "thợ sửa khóa")
            ]
        },
        {
            "category": "LĨNH VỰC LOGISTICS – KHO VẬN",
            "items": [
                ("warehouse worker", "/ˈweə.haʊs ˌwɜː.kər/ (n)", "công nhân kho"),
                ("packer", "/ˈpæk.ər/ (n)", "người đóng gói hàng"),
                ("forklift operator", "/ˈfɔː.klɪft ˈɒp.ər.eɪ.tər/ (n)", "người lái xe nâng"),
                ("shipping manager", "/ˈʃɪp.ɪŋ ˈmæn.ɪ.dʒər/ (n)", "quản lý vận chuyển"),
                ("logistician", "/ˌləʊ.dʒɪˈstɪʃ.ən/ (n)", "chuyên viên hậu cần"),
                ("supply chain manager", "/səˈplaɪ tʃeɪn ˈmæn.ɪ.dʒər/ (n)", "quản lý chuỗi cung ứng")
            ]
        },
        {
            "category": "MỘT SỐ NGHỀ NGHIỆP KHÁC",
            "items": [
                ("tour guide", "/tʊər ɡaɪd/ (n)", "hướng dẫn viên du lịch"),
                ("travel agent", "/ˈtræv.əl ˌeɪ.dʒənt/ (n)", "đại lý du lịch"),
                ("flight attendant", "/ˈflaɪt əˌten.dənt/ (n)", "tiếp viên hàng không"),
                ("real estate agent", "/ˈrɪəl ɪˌsteɪt ˌeɪ.dʒənt/ (n)", "nhân viên bất động sản"),
                ("cleaner", "/ˈkliː.nər/ (n)", "nhân viên vệ sinh"),
                ("babysitter", "/ˈbeɪ.biˌsɪt.ər/ (n)", "người trông trẻ"),
                ("farmer", "/ˈfɑː.mər/ (n)", "nông dân"),
                ("gardener", "/ˈɡɑː.dən.ər/ (n)", "người làm vườn")
            ]
        }
    ],
    "dang_01_location": [
        {
            "category": "at a restaurant – tại nhà hàng",
            "items": [
                ("menu", "/ˈmen.juː/ (n)", "thực đơn"),
                ("waiter", "/ˈweɪ.tər/ (n)", "bồi bàn nam"),
                ("customer", "/ˈkʌs.tə.mər/ (n)", "khách hàng"),
                ("bill", "/bɪl/ (n)", "hóa đơn"),
                ("seat", "/siːt/ (n)", "chỗ ngồi"),
                ("meal", "/miːl/ (n)", "bữa ăn"),
                ("receipt", "/rɪˈsiːt/ (n)", "biên lai"),
                ("refreshment", "/rɪˈfreʃ.mənt/ (n)", "món ăn nhẹ/giải khát"),
                ("reserve", "/rɪˈzɜːv/ (v)", "đặt trước"),
                ("order", "/ˈɔː.dər/ (v)", "gọi món"),
                ("book a table", "/bʊk ə ˈteɪ.bəl/ (v phr)", "đặt bàn"),
                ("make a reservation", "/meɪk ə ˌrez.əˈveɪ.ʃən/ (v phr)", "đặt chỗ trước")
            ]
        },
        {
            "category": "at a hotel – tại khách sạn",
            "items": [
                ("front desk / reception desk", "/ˌfrʌnt ˈdesk/ / /rɪˈsep.ʃən desk/ (n)", "quầy lễ tân"),
                ("room key", "/ruːm kiː/ (n)", "chìa khóa phòng"),
                ("room service", "/ˈruːm ˌsɜː.vɪs/ (n)", "dịch vụ phục vụ phòng"),
                ("bellboy", "/ˈbel.bɔɪ/ (n)", "nhân viên khuân hành lý"),
                ("receptionist", "/rɪˈsep.ʃən.ɪst/ (n)", "nhân viên lễ tân"),
                ("manager", "/ˈmæn.ɪ.dʒər/ (n)", "quản lý"),
                ("lobby", "/ˈlɒb.i/ (n)", "sảnh chờ"),
                ("housekeeping", "/ˈhaʊsˌkiː.pɪŋ/ (n)", "bộ phận dọn phòng"),
                ("register", "/ˈredʒ.ɪ.stər/ (v)", "đăng ký"),
                ("check in", "/tʃek ɪn/ (v)", "nhận phòng"),
                ("check out", "/tʃek aʊt/ (v)", "trả phòng"),
                ("guest", "/ɡest/ (n)", "khách")
            ]
        },
        {
            "category": "at the bank – tại ngân hàng",
            "items": [
                ("cash", "/kæʃ/ (n)", "tiền mặt"),
                ("credit card", "/ˈkred.ɪt kɑːd/ (n)", "thẻ tín dụng"),
                ("interest", "/ˈɪn.trəst/ (n)", "lãi suất"),
                ("transaction", "/trænˈzæk.ʃən/ (n)", "giao dịch"),
                ("client", "/ˈklaɪ.ənt/ (n)", "khách hàng (dịch vụ)"),
                ("balance", "/ˈbæl.əns/ (n)", "số dư"),
                ("ATM", "/ˌeɪ.tiːˈem/ (n)", "máy rút tiền tự động"),
                ("transfer", "/ˈtræns.fɜːr/ (v)", "chuyển khoản"),
                ("deposit", "/dɪˈpɒz.ɪt/ (v)", "gửi tiền vào"),
                ("withdraw", "/wɪðˈdrɔː/ (v)", "rút tiền"),
                ("account", "/əˈkaʊnt/ (n)", "tài khoản"),
                ("loan", "/ləʊn/ (n)", "khoản vay")
            ]
        },
        {
            "category": "at the post office – tại bưu điện",
            "items": [
                ("send", "/send/ (v)", "gửi"),
                ("by air", "/baɪ eə(r)/ (adv phr)", "bằng đường hàng không"),
                ("mailbox", "/ˈmeɪl.bɒks/ (n)", "hộp thư"),
                ("address label", "/əˈdres ˈleɪ.bəl/ (n)", "nhãn địa chỉ"),
                ("stamp", "/stæmp/ (n)", "tem thư"),
                ("envelope", "/ˈen.və.ləʊp/ (n)", "phong bì"),
                ("package", "/ˈpæk.ɪdʒ/ (n)", "gói hàng"),
                ("postal code", "/ˈpəʊ.stəl kəʊd/ (n)", "mã bưu chính"),
                ("ship", "/ʃɪp/ (v)", "vận chuyển"),
                ("deliver", "/dɪˈlɪv.ər/ (v)", "giao hàng"),
                ("delivery", "/dɪˈlɪv.ər.i/ (n)", "sự giao hàng"),
                ("tracking number", "/ˈtræk.ɪŋ ˌnʌm.bər/ (n)", "mã theo dõi"),
                ("registered mail", "/ˌredʒ.ɪ.stəd ˈmeɪl/ (n)", "thư bảo đảm")
            ]
        },
        {
            "category": "at a medical office – tại phòng khám",
            "items": [
                ("doctor", "/ˈdɒk.tər/ (n)", "bác sĩ"),
                ("nurse", "/nɜːs/ (n)", "y tá"),
                ("patient", "/ˈpeɪ.ʃənt/ (n)", "bệnh nhân"),
                ("medicine", "/ˈmed.ɪ.sən/ (n)", "thuốc"),
                ("prescription", "/prɪˈskrɪp.ʃən/ (n)", "đơn thuốc"),
                ("check-up", "/ˈtʃek.ʌp/ (n)", "cuộc khám sức khỏe"),
                ("appointment", "/əˈpɔɪnt.mənt/ (n)", "cuộc hẹn"),
                ("clinic", "/ˈklɪn.ɪk/ (n)", "phòng khám"),
                ("treatment", "/ˈtriːt.mənt/ (n)", "sự điều trị"),
                ("examination", "/ɪɡˌzæm.ɪˈneɪ.ʃən/ (n)", "sự kiểm tra sức khỏe"),
                ("medical record", "/ˈmed.ɪ.kəl ˌrek.ɔːd/ (n)", "hồ sơ y tế"),
                ("receptionist", "/rɪˈsep.ʃən.ɪst/ (n)", "nhân viên lễ tân")
            ]
        },
        {
            "category": "at the airport – tại sân bay",
            "items": [
                ("passport", "/ˈpɑːs.pɔːt/ (n)", "hộ chiếu"),
                ("boarding pass", "/ˈbɔː.dɪŋ ˌpɑːs/ (n)", "thẻ lên máy bay"),
                ("passenger", "/ˈpæs.ən.dʒər/ (n)", "hành khách"),
                ("luggage / baggage", "/ˈlʌɡ.ɪdʒ/ / /ˈbæɡ.ɪdʒ/ (n)", "hành lý"),
                ("flight", "/flaɪt/ (n)", "chuyến bay"),
                ("gate", "/ɡeɪt/ (n)", "cổng ra máy bay"),
                ("departure", "/dɪˈpɑː.tʃər/ (n)", "sự khởi hành"),
                ("arrival", "/əˈraɪ.vəl/ (n)", "sự đến nơi"),
                ("terminal", "/ˈtɜː.mɪ.nəl/ (n)", "nhà ga"),
                ("security check", "/sɪˈkjʊə.rə.ti tʃek/ (n)", "kiểm tra an ninh"),
                ("airline", "/ˈeə.laɪn/ (n)", "hãng hàng không"),
                ("carry-on bag", "/ˈkæri ɒn bæɡ/ (n)", "hành lý xách tay")
            ]
        },
        {
            "category": "at a shop/store – tại cửa hàng",
            "items": [
                ("cashier", "/kæʃˈɪər/ (n)", "thu ngân"),
                ("salesperson", "/ˈseɪlzˌpɜː.sən/ (n)", "nhân viên bán hàng"),
                ("item", "/aɪ.təm/ (n)", "món hàng"),
                ("in stock", "/ɪn stɒk/ (adj phr)", "còn hàng"),
                ("out of stock", "/ˌaʊt əv ˈstɒk/ (adj phr)", "hết hàng"),
                ("refund", "/ˈriː.fʌnd/ (n)", "khoản hoàn tiền"),
                ("payment", "/ˈpeɪ.mənt/ (n)", "khoản thanh toán"),
                ("shopping bag", "/ˈʃɒp.ɪŋ bæɡ/ (n)", "túi mua sắm"),
                ("shopping cart", "/ˈʃɒp.ɪŋ kɑːt/ (n)", "xe đẩy mua hàng"),
                ("on sale", "/ɒn seɪl/ (adj phr)", "đang giảm giá"),
                ("receipt", "/rɪˈsiːt/ (n)", "hóa đơn"),
                ("discount", "/ˈdɪs.kaʊnt/ (n)", "chiết khấu, giảm giá"),
                ("price tag", "/ˈpraɪs ˌtæɡ/ (n)", "mác giá")
            ]
        },
        {
            "category": "at a warehouse – tại nhà kho",
            "items": [
                ("shipment", "/ˈʃɪp.mənt/ (n)", "lô hàng"),
                ("package", "/ˈpæk.ɪdʒ/ (n)", "kiện hàng"),
                ("inventory", "/ˈɪn.vən.tər.i/ (n)", "hàng tồn kho"),
                ("storage", "/ˈstɔː.rɪdʒ/ (n)", "kho lưu trữ"),
                ("loading dock", "/ˈləʊ.dɪŋ dɒk/ (n)", "khu bốc xếp hàng"),
                ("forklift", "/ˈfɔː.klɪft/ (n)", "xe nâng"),
                ("load", "/ləʊd/ (v)", "chất hàng"),
                ("unload", "/ʌnˈləʊd/ (v)", "dỡ hàng"),
                ("stack", "/stæk/ (v)", "xếp chồng"),
                ("label", "/ˈleɪ.bəl/ (n)", "nhãn dán"),
                ("invoice", "/ˈɪn.vɔɪs/ (n)", "hóa đơn"),
                ("drop off", "/drɒp ɒf/ (v)", "giao hàng")
            ]
        },
        {
            "category": "at an office – tại văn phòng",
            "items": [
                ("manager", "/ˈmæn.ɪ.dʒər/ (n)", "quản lý"),
                ("employee", "/ɪmˈplɔɪ.iː/ (n)", "nhân viên"),
                ("employer", "/ɪmˈplɔɪ.ər/ (n)", "người tuyển dụng"),
                ("coworker / colleague", "/ˈkəʊˌwɜː.kər/ / /ˈkɒl.iːɡ/ (n)", "đồng nghiệp"),
                ("department", "/dɪˈpa:t.mənt/ (n)", "phòng ban"),
                ("interview", "/ˈɪn.tə.vjuː/ (n)", "buổi phỏng vấn"),
                ("project", "/ˈprɒdʒ.ekt/ (n)", "dự án"),
                ("meeting", "/ˈmiː.tɪŋ/ (n)", "cuộc họp"),
                ("deadline", "/ˈded.laɪn/ (n)", "hạn chót"),
                ("memo", "/ˈmem.əʊ/ (n)", "thông báo nội bộ"),
                ("salary", "/ˈsæl.ər.i/ (n)", "lương"),
                ("CEO", "/ˌsiː.iːˈəʊ/ (n)", "giám đốc điều hành"),
                ("contract", "/ˈkɒn.trækt/ (n)", "hợp đồng")
            ]
        },
        {
            "category": "at a theater – tại rạp/nhà hát",
            "items": [
                ("ticket", "/ˈtɪk.ɪt/ (n)", "vé"),
                ("seat", "/siːt/ (n)", "chỗ ngồi"),
                ("showtime", "/ˈʃəʊ.taɪm/ (n)", "giờ chiếu"),
                ("curtain", "/ˈkɜː.tən/ (n)", "màn sân khẩu"),
                ("play", "/pleɪ/ (n)", "vở kịch"),
                ("movie", "/ˈmuː.vi/ (n)", "phim"),
                ("performance", "/pəˈfɔː.məns/ (n)", "buổi biểu diễn"),
                ("audience", "/ˈɔː.di.əns/ (n)", "khán giả"),
                ("actor", "/ˈæk.tər/ (n)", "nam diễn viên"),
                ("actress", "/ˈæk.trəs/ (n)", "nữ diễn viên"),
                ("stage", "/steɪdʒ/ (n)", "sân khấu"),
                ("director", "/daɪˈrek.tər/ (n)", "đạo diễn"),
                ("sold out", "/səʊld aʊt/ (adj)", "hết vé")
            ]
        },
        {
            "category": "at a real estate agency – tại công ty bất động sản",
            "items": [
                ("apartment", "/əˈpɑːt.mənt/ (n)", "căn hộ"),
                ("home", "/həʊm/ (n)", "nhà"),
                ("rent", "/rent/ (v)", "thuê"),
                ("landlord", "/ˈlænd.lɔːd/ (n)", "chủ nhà (cho thuê)"),
                ("tenant", "/ˈten.ənt/ (n)", "người thuê nhà"),
                ("lease", "/liːs/ (n)", "hợp đồng thuê"),
                ("move in", "/muːv ɪn/ (v)", "chuyển vào"),
                ("move out", "/muːv aʊt/ (v)", "chuyển ra"),
                ("property", "/ˈprɒp.ə.ti/ (n)", "bất động sản, tài sản"),
                ("contract", "/ˈkɒn.trækt/ (n)", "hợp đồng"),
                ("real estate agent", "/ˈrɪəl ɪˌsteɪt ˌeɪ.dʒənt/ (n)", "nhân viên môi giới nhà đất"),
                ("listing", "/ˈlɪs.tɪŋ/ (n)", "danh sách bất động sản")
            ]
        },
        {
            "category": "at a train/bus station – tại trạm xe lửa/xe buýt",
            "items": [
                ("ticket booth", "/ˈtɪk.ɪt buːð/ (n)", "quầy bán vé"),
                ("schedule", "/ˈʃed.juːl/ (n)", "lịch trình"),
                ("platform", "/ˈplæt.fɔːm/ (n)", "sân ga"),
                ("departure", "/dɪˈpɑː.tʃər/ (n)", "sự khởi hành"),
                ("arrival", "/əˈraɪ.vəl/ (n)", "sự đến"),
                ("train", "/treɪn/ (n)", "tàu"),
                ("bus", "/bas/ (n)", "xe buýt"),
                ("track", "/træk/ (n)", "đường ray"),
                ("conductor", "/kənˈdʌk.tər/ (n)", "nhân viên soát vé"),
                ("route", "/ruːt/ (n)", "tuyến đường"),
                ("stop", "/stɒp/ (n)", "trạm dừng"),
                ("transfer", "/ˈtræns.fɜːr/ (n)", "sự chuyển tuyến")
            ]
        },
        {
            "category": "an advertising company – tại công ty quảng cáo",
            "items": [
                ("campaign", "/kæmˈpeɪn/ (n)", "chiến dịch"),
                ("client", "/ˈklaɪ.ənt/ (n)", "khách hàng (dịch vụ)"),
                ("marketing", "/ˈmɑː.kɪ.tɪŋ/ (n)", "tiếp thị"),
                ("design", "/dɪˈzaɪn/ (n)", "thiết kế"),
                ("pitch", "/pɪtʃ/ (n)", "bài thuyết trình chào hàng")
            ]
        },
        {
            "category": "a factory – tại nhà máy",
            "items": [
                ("machinery", "/məˈʃiː.nər.i/ (n)", "máy móc"),
                ("production", "/prəˈdʌk.ʃən/ (n)", "sản xuất"),
                ("assembly line", "/əˈsem.bli ˌlaɪn/ (n)", "dây chuyền lắp ráp"),
                ("workers", "/ˈwɜː.kərz/ (n)", "công nhân")
            ]
        },
        {
            "category": "a newspaper / press office – tại tòa soạn báo/văn phòng báo chí",
            "items": [
                ("reporter", "/rɪˈpɔː.tər/ (n)", "phóng viên"),
                ("article", "/ˈɑː.tɪ.kəl/ (n)", "bài báo"),
                ("deadline", "/ˈded.laɪn/ (n)", "hạn chót"),
                ("editor", "/ˈed.ɪ.tər/ (n)", "biên tập viên"),
                ("print", "/prɪnt/ (v)", "in ấn")
            ]
        },
        {
            "category": "a customer service center – tại trung tâm dịch vụ khách hàng",
            "items": [
                ("complaint", "/kəmˈpleɪnt/ (n)", "lời phàn nàn"),
                ("inquiry", "/ɪnˈkwaɪə.ri/ (n)", "yêu cầu thông tin"),
                ("hotline", "/ˈhɒt.laɪn/ (n)", "đường dây nóng"),
                ("feedback", "/ˈfiːd.bæk/ (n)", "phản hồi"),
                ("support", "/səˈpɔːt/ (n)", "hỗ trợ")
            ]
        },
        {
            "category": "a car dealership – tại đại lý ô tô",
            "items": [
                ("test drive", "/ˈtest ˌdraɪv/ (n)", "lái thử"),
                ("showroom", "/ˈʃəʊ.ruːm/ (n)", "phòng trưng bày xe"),
                ("vehicle", "/ˈvɪə.kəl/ (n)", "phương tiện"),
                ("salesman", "/ˈsalesman/ (n)", "nhân viên bán hàng")
            ]
        },
        {
            "category": "a fitness center / gym – tại phòng tập thể hình",
            "items": [
                ("workout", "/ˈwɜː.kaʊt/ (n)", "buổi tập luyện"),
                ("trainer", "/ˈtreɪ.nər/ (n)", "huấn luyện viên"),
                ("membership", "/ˈmem.bə.ʃɪp/ (n)", "thẻ hội viên"),
                ("treadmill", "/ˈtred.mɪl/ (n)", "máy chạy bộ")
            ]
        },
        {
            "category": "a university campus – tại khuôn viên trường đại học",
            "items": [
                ("lecture", "/ˈlek.tʃər/ (n)", "bài giảng"),
                ("student ID", "/ˌstjuː.dənt aɪˈdiː/ (n)", "thẻ sinh viên"),
                ("dorm", "/dɔːm/ (n)", "ký túc xá"),
                ("registrar", "/ˌredʒ.ɪˈstrɑːr/ (n)", "phòng đào tạo"),
                ("semester", "/sɪˈmes.tər/ (n)", "học kỳ")
            ]
        },
        {
            "category": "a grocery store – tại cửa hàng tạp hoá",
            "items": [
                ("aisle", "/aɪl/ (n)", "lối đi giữa các kệ"),
                ("cart", "/kɑːt/ (n)", "xe đẩy hàng"),
                ("checkout", "/ˈtʃek.aʊt/ (n)", "quầy thanh toán"),
                ("receipt", "/rɪˈsiːt/ (n)", "biên lai"),
                ("promotion", "/prəˈməʊ.ʃən/ (n)", "chương trình khuyến mãi")
            ]
        },
        {
            "category": "a delivery hub – tại trung tâm phân phối hàng hóa",
            "items": [
                ("parcel", "/ˈpɑː.səl/ (n)", "bưu kiện"),
                ("dispatch", "/dɪˈspætʃ/ (n)", "sự gửi hàng"),
                ("logistics", "/ləˈdʒɪs.tɪks/ (n)", "hậu cần"),
                ("courier", "/ˈkʊə.ri.ər/ (n)", "nhân viên giao hàng"),
                ("scan", "/skæn/ (v)", "quét (mã, hàng)")
            ]
        },
        {
            "category": "a market – tại chợ",
            "items": [
                ("vendor", "/ˈven.dər/ (n)", "người bán hàng"),
                ("stall", "/stɔːl/ (n)", "sạp hàng"),
                ("bargain", "/ˈbɑː.ɡɪn/ (n)", "món hời, giá hời"),
                ("fresh produce", "/freʃ ˈprɒ.djuːs/ (n)", "nông sản tươi"),
                ("price tag", "/ˈpraɪs ˌtæɡ/ (n)", "mác giá")
            ]
        }
    ],
    "dang_01_topic": [
        {
            "category": "a music festival – lễ hội âm nhạc",
            "items": [
                ("stage", "/steɪdʒ/ (n)", "sân khấu"),
                ("band", "/bænd/ (n)", "ban nhạc"),
                ("crowd", "/kraʊd/ (n)", "đám đông"),
                ("soundcheck", "/ˈsaʊnd.tʃek/ (n)", "kiểm tra âm thanh"),
                ("ticket", "/ˈtɪk.ɪt/ (n)", "vé")
            ]
        },
        {
            "category": "a sporting event – sự kiện thể thao",
            "items": [
                ("stadium", "/ˈsteɪ.di.əm/ (n)", "sân vận động"),
                ("team", "/tiːm/ (n)", "đội"),
                ("match", "/mætʃ/ (n)", "trận đấu"),
                ("score", "/skɔːr/ (n)", "điểm số"),
                ("cheer", "/tʃɪər/ (v)", "cổ vũ")
            ]
        },
        {
            "category": "an orientation session – buổi định hướng",
            "items": [
                ("welcome", "/ˈwel.kəm/ (n)", "lời chào mừng"),
                ("new staff", "/njuː stɑːf/ (n)", "nhân viên mới"),
                ("schedule", "/ˈʃed.juːl/ (n)", "lịch trình"),
                ("policy", "/ˈpɒl.ə.si/ (n)", "chính sách")
            ]
        },
        {
            "category": "an anniversary celebration – lễ kỷ niệm",
            "items": [
                ("years", "/jɪərz/ (n)", "số năm (kỷ niệm)"),
                ("invite", "/ɪnˈvaɪt/ (n)", "thư mời"),
                ("speech", "/spiːtʃ/ (n)", "bài phát biểu"),
                ("cake", "/keɪk/ (n)", "bánh kem"),
                ("memory", "/ˈmem.ər.i/ (n)", "kỷ niệm")
            ]
        },
        {
            "category": "a community fundraiser – buổi gây quỹ cộng đồng",
            "items": [
                ("donation", "/dəʊˈneɪ.ʃən/ (n)", "sự quyên góp"),
                ("raffle", "/ˈræf.əl/ (n)", "bốc thăm trúng thưởng"),
                ("cause", "/kɔːz/ (n)", "mục đích từ thiện"),
                ("support", "/səˈpɔːt/ (n)", "sự ủng hộ"),
                ("volunteer", "/ˌvɒl.ənˈtɪər/ (n)", "tình nguyện viên")
            ]
        },
        {
            "category": "a press conference – cuộc họp báo",
            "items": [
                ("media", "/ˈmiː.di.ə/ (n)", "truyền thông"),
                ("spokesperson", "/ˈspəʊksˌpɜː.sən/ (n)", "người phát ngôn"),
                ("announcement", "/əˈnaʊns.mənt/ (n)", "thông báo"),
                ("live", "/laɪv/ (adj)", "truyền trực tiếp")
            ]
        },
        {
            "category": "a product demonstration – buổi trình diễn sản phẩm",
            "items": [
                ("try out", "/traɪ aʊt/ (v)", "thử nghiệm"),
                ("feature", "/ˈfiː.tʃər/ (n)", "tính năng"),
                ("benefit", "/ˈben.ɪ.fɪt/ (n)", "lợi ích"),
                ("sample", "/ˈsɑːm.pəl/ (n)", "mẫu dùng thử"),
                ("showcase", "/ˈʃəʊ.keɪs/ (v)", "trình bày, trưng bày")
            ]
        },
        {
            "category": "a charity auction – buổi đấu giá từ thiện",
            "items": [
                ("bid", "/bɪd/ (v/n)", "đấu giá"),
                ("item", "/ˈaɪ.təm/ (n)", "món đồ"),
                ("cause", "/kɔːz/ (n)", "mục đích từ thiện"),
                ("donation", "/dəʊˈneɪ.ʃən/ (n)", "khoản quyên góp"),
                ("winner", "/ˈwɪn.ər/ (n)", "người thắng")
            ]
        },
        {
            "category": "an employee training – buổi đào tạo nhân viên",
            "items": [
                ("instruction", "/ɪnˈstrʌk.ʃən/ (n)", "hướng dẫn"),
                ("safety", "/ˈseɪf.ti/ (n)", "an toàn"),
                ("skills", "/skɪlz/ (n)", "kỹ năng"),
                ("handbook", "/ˈhænd.bʊk/ (n)", "sổ tay")
            ]
        },
        {
            "category": "a company outing – chuyến đi chơi của công ty",
            "items": [
                ("picnic", "/ˈpɪk.nɪk/ (n)", "buổi dã ngoại"),
                ("event", "/ɪˈvent/ (n)", "sự kiện"),
                ("bonding", "/ˈbɒn.dɪŋ/ (n)", "sự gắn kết"),
                ("register", "/ˈredʒ.ɪ.stər/ (v)", "đăng ký"),
                ("lunch", "/lʌntʃ/ (n)", "bữa trưa")
            ]
        },
        {
            "category": "a school open house – ngày hội mở trường",
            "items": [
                ("tour", "/tʊər/ (n)", "chuyến tham quan"),
                ("parent", "/ˈpeə.rənt/ (n)", "phụ huynh"),
                ("classroom", "/ˈklɑːs.ruːm/ (n)", "lớp học"),
                ("introduction", "/ˌɪn.trəˈdʌk.ʃən/ (n)", "sự giới thiệu")
            ]
        },
        {
            "category": "a union meeting – cuộc họp công đoàn",
            "items": [
                ("workers", "/ˈwɜː.kərz/ (n)", "công nhân"),
                ("vote", "/vəʊt/ (v/n)", "bầu chọn"),
                ("agreement", "/əˈɡriː.mənt/ (n)", "thỏa thuận"),
                ("protest", "/ˈprəʊ.test/ (n)", "cuộc biểu tình"),
                ("negotiation", "/nɪˌɡəʊ.ʃiˈeɪ.ʃən/ (n)", "cuộc đàm phán")
            ]
        }
    ]
}

def build_vocabulary_slides(sec_id, category_list):
    slides = []
    fake_idx = 1000
    
    title_map = {
        "dang_01_identity": "TỪ VỰNG VỀ NGHỀ NGHIỆP/CHỨC VỤ",
        "dang_01_location": "TỪ VỰNG LIÊN QUAN ĐẾN ĐỊA ĐIỂM",
        "dang_01_topic": "TỪ VỰNG VỀ CÁC SỰ KIỆN HAY XUẤT HIỆN"
    }
    
    main_title = title_map.get(sec_id, "MỘT SỐ TỪ VỰNG QUAN TRỌNG")
    
    for cat in category_list:
        fake_idx += 1
        cat_title = cat["category"]
        
        text = [
            f"<strong><span style=\"color: #00B0F0;\">{main_title}</span></strong>",
            f"• <strong><span style=\"color: #FF0000;\">{cat_title}</span></strong>"
        ]
        
        vietnamese_text = [
            main_title,
            f"• {cat_title}"
        ]
        
        for w, ipa, meaning in cat["items"]:
            bullet_str = f"<span style=\"color: #00B050;\">{w}</span> {ipa}: {meaning}"
            text.append(bullet_str)
            
            viet_bullet = f"{meaning} {ipa}"
            vietnamese_text.append(viet_bullet)
            
        slides.append({
            "slide_index": fake_idx,
            "text": text,
            "vietnamese_text": vietnamese_text
        })
        
    return slides

def main():
    # Load current json database
    with open("data/part03_data.json", "r", encoding="utf-8") as f:
        db = json.load(f)
        
    for section in db:
        sec_id = section.get("id")
        if sec_id in VOCAB_DATA:
            vocab_slides = build_vocabulary_slides(sec_id, VOCAB_DATA[sec_id])
            section["vocabulary"] = vocab_slides
            print(f"Updated section {sec_id}: populated {len(vocab_slides)} slides of vocabulary.")
            
    # Save back to json
    with open("data/part03_data.json", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    # Save back to js (window.part03Data)
    with open("data/part03_data.js", "w", encoding="utf-8") as f:
        f.write("window.part03Data = ")
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write(";\n")
        
    print("Successfully updated database files.")

if __name__ == "__main__":
    main()
