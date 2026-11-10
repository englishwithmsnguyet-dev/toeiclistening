// Dữ liệu Nghe Chép Chính Tả PART 01 (Tất cả câu ví dụ + Toàn bộ các phương án A, B, C, D của tất cả bài luyện tập & Test 1-10)
(function() {
  const dang01Examples = [
    {
      "id": 1,
      "slide_index": 4,
      "audio": "media/part01_examples/p1_ex_slide4.mp3",
      "singleAudio": true,
      "sentence": "The man is adjusting a watch.",
      "vi": "Người đàn ông đang điều chỉnh đồng hồ đeo tay.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 2,
      "slide_index": 7,
      "audio": "media/part01_examples/p1_ex_slide7.mp3",
      "singleAudio": true,
      "sentence": "The man is approaching a counter.",
      "vi": "Người đàn ông đang tiến lại gần quầy.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 3,
      "slide_index": 10,
      "audio": "media/part01_examples/p1_ex_slide10.mp3",
      "singleAudio": true,
      "sentence": "The man is carrying a ladder.",
      "vi": "Người đàn ông đang khiêng một chiếc thang.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 4,
      "slide_index": 13,
      "audio": "media/part01_examples/p1_ex_slide13.mp3",
      "singleAudio": true,
      "sentence": "The woman is checking a list.",
      "vi": "Người phụ nữ đang kiểm tra một danh sách.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 5,
      "slide_index": 16,
      "audio": "media/part01_examples/p1_ex_slide16.mp3",
      "singleAudio": true,
      "sentence": "The woman is entering a supermarket.",
      "vi": "Người phụ nữ đang bước vào một siêu thị.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 6,
      "slide_index": 19,
      "audio": "media/part01_examples/p1_ex_slide19.mp3",
      "singleAudio": true,
      "sentence": "The man is hanging some photographs on the wall.",
      "vi": "Người đàn ông đang treo vài bức ảnh lên tường.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 7,
      "slide_index": 22,
      "audio": "media/part01_examples/p1_ex_slide22.mp3",
      "singleAudio": true,
      "sentence": "The woman is holding a suitcase.",
      "vi": "Người phụ nữ đang cầm một chiếc vali.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 8,
      "slide_index": 25,
      "audio": "media/part01_examples/p1_ex_slide25.mp3",
      "singleAudio": true,
      "sentence": "The man is leaning against a wall.",
      "vi": "Người đàn ông đang tựa vào một bức tường.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 9,
      "slide_index": 28,
      "audio": "media/part01_examples/p1_ex_slide28.mp3",
      "singleAudio": true,
      "sentence": "The worker is loading some boxes onto a truck.",
      "vi": "Người công nhân đang bốc các hộp lên xe tải.",
      "hint": "The worker",
      "type": "example"
    },
    {
      "id": 10,
      "slide_index": 31,
      "audio": "media/part01_examples/p1_ex_slide31.mp3",
      "singleAudio": true,
      "sentence": "The woman is looking at the monitor.",
      "vi": "Người phụ nữ đang nhìn vào màn hình.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 11,
      "slide_index": 34,
      "audio": "media/part01_examples/p1_ex_slide34.mp3",
      "singleAudio": true,
      "sentence": "The woman is opening her handbag.",
      "vi": "Người phụ nữ đang mở túi xách của mình.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 12,
      "slide_index": 37,
      "audio": "media/part01_examples/p1_ex_slide37.mp3",
      "singleAudio": true,
      "sentence": "The man is paying for a purchase.",
      "vi": "Người đàn ông đang thanh toán tiền mua hàng.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 13,
      "slide_index": 40,
      "audio": "media/part01_examples/p1_ex_slide40.mp3",
      "singleAudio": true,
      "sentence": "The man is pouring coffee into a cup.",
      "vi": "Người đàn ông đang rót cà phê vào cốc.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 14,
      "slide_index": 43,
      "audio": "media/part01_examples/p1_ex_slide43.mp3",
      "singleAudio": true,
      "sentence": "The woman is pushing a shopping cart.",
      "vi": "Người phụ nữ đang đẩy một chiếc xe chở hàng.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 15,
      "slide_index": 46,
      "audio": "media/part01_examples/p1_ex_slide46.mp3",
      "singleAudio": true,
      "sentence": "The man is pulling a suitcase.",
      "vi": "Người đàn ông đang kéo một chiếc vali.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 16,
      "slide_index": 49,
      "audio": "media/part01_examples/p1_ex_slide49.mp3",
      "singleAudio": true,
      "sentence": "She is putting a book on the table.",
      "vi": "Cô ấy đang đặt một cuốn sách lên bàn.",
      "hint": "She is",
      "type": "example"
    },
    {
      "id": 17,
      "slide_index": 52,
      "audio": "media/part01_examples/p1_ex_slide52.mp3",
      "singleAudio": true,
      "sentence": "The man is reaching for a book.",
      "vi": "Người đàn ông đang với tay lấy một cuốn sách.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 18,
      "slide_index": 55,
      "audio": "media/part01_examples/p1_ex_slide55.mp3",
      "singleAudio": true,
      "sentence": "The man is reading a document.",
      "vi": "Người đàn ông đang đọc một tài liệu.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 19,
      "slide_index": 58,
      "audio": "media/part01_examples/p1_ex_slide58.mp3",
      "singleAudio": true,
      "sentence": "The woman is searching in her handbag.",
      "vi": "Người phụ nữ đang tìm đồ trong túi xách.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 20,
      "slide_index": 61,
      "audio": "media/part01_examples/p1_ex_slide61.mp3",
      "singleAudio": true,
      "sentence": "The woman is sitting at a desk.",
      "vi": "Người phụ nữ đang ngồi tại bàn làm việc.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 21,
      "slide_index": 64,
      "audio": "media/part01_examples/p1_ex_slide64.mp3",
      "singleAudio": true,
      "sentence": "The man is standing near a counter.",
      "vi": "Người đàn ông đang đứng gần một chiếc quầy.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 22,
      "slide_index": 67,
      "audio": "media/part01_examples/p1_ex_slide67.mp3",
      "singleAudio": true,
      "sentence": "The man is talking on the phone.",
      "vi": "Người đàn ông đang nói chuyện điện thoại.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 23,
      "slide_index": 69,
      "audio": "media/part01_examples/p1_ex_slide69.mp3",
      "singleAudio": true,
      "sentence": "The man is using a computer.",
      "vi": "Người đàn ông đang sử dụng máy tính.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 24,
      "slide_index": 72,
      "audio": "media/part01_examples/p1_ex_slide72.mp3",
      "singleAudio": true,
      "sentence": "The man is waiting at a bus stop.",
      "vi": "Người đàn ông đang chờ ở trạm xe buýt.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 25,
      "slide_index": 75,
      "audio": "media/part01_examples/p1_ex_slide75.mp3",
      "singleAudio": true,
      "sentence": "The man is walking up a stairway.",
      "vi": "Người đàn ông đang bước lên cầu thang.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 26,
      "slide_index": 78,
      "audio": "media/part01_examples/p1_ex_slide78.mp3",
      "singleAudio": true,
      "sentence": "The man is wearing a jacket.",
      "vi": "Người đàn ông đang mặc một chiếc áo khoác.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 27,
      "slide_index": 81,
      "audio": "media/part01_examples/p1_ex_slide81.mp3",
      "singleAudio": true,
      "sentence": "The man is putting on a cap.",
      "vi": "Người đàn ông đang đội mũ lưỡi trai.",
      "hint": "The man",
      "type": "example"
    },
    {
      "id": 28,
      "slide_index": 84,
      "audio": "media/part01_examples/p1_ex_slide84.mp3",
      "singleAudio": true,
      "sentence": "The woman is working at a computer.",
      "vi": "Người phụ nữ đang làm việc bên máy tính.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 29,
      "slide_index": 87,
      "audio": "media/part01_examples/p1_ex_slide87.mp3",
      "singleAudio": true,
      "sentence": "The woman is writing notes.",
      "vi": "Người phụ nữ đang ghi chép.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 30,
      "slide_index": 90,
      "audio": "media/part01_examples/p1_ex_slide90.mp3",
      "singleAudio": true,
      "sentence": "The woman is folding clothes.",
      "vi": "Người phụ nữ đang gấp quần áo.",
      "hint": "The woman",
      "type": "example"
    },
    {
      "id": 31,
      "slide_index": 93,
      "audio": "media/part01_examples/p1_ex_slide93.mp3",
      "singleAudio": true,
      "sentence": "The man is wiping the table.",
      "vi": "Người đàn ông đang lau bàn.",
      "hint": "The man",
      "type": "example"
    }
  ];

  const DANG01_VI = {
    "1_A": "Một người đàn ông đang đẩy xe đẩy hàng.",
    "1_B": "Một người đàn ông đang chờ để mua hàng.",
    "1_C": "Một người đàn ông đang cầm một số hàng hoá.",
    "1_D": "Một người đàn ông đang lắp ráp một số chiếc kệ.",
    "2_A": "Cô ấy đang tìm đồ trong túi xách.",
    "2_B": "Cô ấy đang nhìn vào tủ trưng bày.",
    "2_C": "Cô ấy đang thanh toán tiền mua hàng.",
    "2_D": "Cô ấy đang cầm vài bông hoa.",
    "3_A": "Anh ấy đang đi dạo dọc bờ biển.",
    "3_B": "Anh ấy đang bơi ở biển.",
    "3_C": "Anh ấy đang cầm một chiếc cần câu cá.",
    "3_D": "Anh ấy đang bước lên thuyền.",
    "4_A": "Một người phụ nữ đang đứng trên con phố đông đúc.",
    "4_B": "Một người phụ nữ đang lau cửa kính ô tô bằng khăn.",
    "4_C": "Một người phụ nữ đang vắt chiếc áo khoác trên tay.",
    "4_D": "Một người phụ nữ đang đỗ xe.",
    "5_A": "Anh ấy đang nói chuyện điện thoại.",
    "5_B": "Anh ấy đang gấp một tờ báo.",
    "5_C": "Anh ấy đang viết vào một biểu mẫu.",
    "5_D": "Anh ấy đang rời khỏi văn phòng.",
    "6_A": "Một người đàn ông đang mở một chiếc ngăn kéo.",
    "6_B": "Một người đàn ông đang lau quầy.",
    "6_C": "Một người đàn ông đang gọi món ăn.",
    "6_D": "Một người đàn ông đang rót đồ uống."
  };

  const DANG02_VI = {
    "1_A": "Một trong những người đàn ông đang sửa xe máy.",
    "1_B": "Một trong những người đàn ông đang lên thuyền.",
    "1_C": "Một trong những người đàn ông đang lái xe hơi.",
    "1_D": "Một trong những người đàn ông đang đi bộ dọc mép nước.",
    "2_A": "Họ đang ngồi trong khu vực chờ.",
    "2_B": "Họ đang đặt sách lên bàn.",
    "2_C": "Một trong những người phụ nữ đang di chuyển một chiếc ghế.",
    "2_D": "Một trong những người phụ nữ đang tưới cây.",
    "3_A": "Một trong những người phụ nữ đang quàng khăn.",
    "3_B": "Những người phụ nữ đang nói chuyện với nhau.",
    "3_C": "Người đàn ông đang rót cà phê vào cốc.",
    "3_D": "Mọi người đang gấp thực đơn lại.",
    "4_A": "Một thông báo đang được treo trên cột.",
    "4_B": "Những người phụ nữ đang đi về phía cửa ra vào.",
    "4_C": "Người đàn ông đang thay lốp xe đạp.",
    "4_D": "Một chiếc giỏ đang được lấy ra khỏi xe đẩy.",
    "5_A": "Một trong những người phụ nữ đang viết vào sổ tay.",
    "5_B": "Một trong những người phụ nữ đang xem một số tài liệu.",
    "5_C": "Những người phụ nữ đang ngồi tại bàn làm việc của họ.",
    "5_D": "Những người phụ nữ đang đối mặt với nhau.",
    "6_A": "Một số du khách đang ngồi trong khu vực chờ.",
    "6_B": "Một số công nhân đang dựng vách ngăn.",
    "6_C": "Một trong những người phụ nữ đang phát vé.",
    "6_D": "Một trong những người đàn ông đang tiến lại gần quầy.",
    "7_A": "Một số người đang ngồi trong xe hơi.",
    "7_B": "Một số người đang quay mặt vào nhau.",
    "7_C": "Một người phụ nữ đang mở túi xách.",
    "7_D": "Một người đàn ông đang cởi áo khoác.",
    "8_A": "Họ đang nhìn vào máy photocopy.",
    "8_B": "Họ đang dán thông báo lên bảng.",
    "8_C": "Họ đang bỏ một số giấy tờ vào bìa hồ sơ.",
    "8_D": "Họ đang di chuyển thiết bị ra khỏi phòng."
  };

  const DANG03_VI = {
    "1_A": "Những chiếc xe hơi đang được vận chuyển trên một chiếc xe tải.",
    "1_B": "Những chiếc xe hơi đang được sửa chữa.",
    "1_C": "Có nhiều người ở trong những chiếc xe hơi.",
    "1_D": "Có những chiếc xe hơi ở tầng trên của xe tải.",
    "2_A": "Đồ uống đang được rót vào ly.",
    "2_B": "Một số bông hoa đang được cắm vào bình.",
    "2_C": "Một người phụ nữ đang gấp khăn ăn.",
    "2_D": "Một người phụ nữ đang lau bàn.",
    "3_A": "Một số khách hàng đang rời khỏi cửa hàng.",
    "3_B": "Khu vực ngồi được trang trí bằng cây xanh.",
    "3_C": "Một công nhân đang sửa chữa một số thiết bị chiếu sáng.",
    "3_D": "Một chiếc ghế dài đang được di chuyển vào góc.",
    "4_A": "Máy bay đang đỗ tại sân bay.",
    "4_B": "Hành lý đang được chuyển lên máy bay.",
    "4_C": "Có nhiều người đang lên máy bay.",
    "4_D": "Có những nhân viên bảo trì đang sửa chữa máy bay.",
    "5_A": "Có những người dọn dẹp trong giảng đường.",
    "5_B": "Giảng đường đang có người sử dụng.",
    "5_C": "Có nhiều người trong giảng đường.",
    "5_D": "Giảng đường đang không có người.",
    "6_A": "Cô ấy đang mặc quần dài.",
    "6_B": "Cô ấy đang thanh toán hóa đơn.",
    "6_C": "Hình ảnh phản chiếu của cô ấy ở trong gương.",
    "6_D": "Cô ấy đang nhìn hình ảnh phản chiếu của mình.",
    "7_A": "Các khung tranh đang được treo lên tường.",
    "7_B": "Những người đàn ông đang nói chuyện với nhau qua điện thoại.",
    "7_C": "Tài liệu đã được trải ra trên bàn làm việc.",
    "7_D": "Một người đàn ông đang chỉ vào thứ gì đó trên bảng.",
    "8_A": "Một chiếc túi đã được đặt trên sàn nhà.",
    "8_B": "Người phụ nữ đang dán một mẩu ghi chú lên bảng thông báo.",
    "8_C": "Một tờ báo đã được trải ra trên tấm thảm.",
    "8_D": "Người phụ nữ đang sắp xếp những chiếc gối trên ghế sofa.",
    "9_A": "Có giấy tờ chất đống trên một chiếc ghế.",
    "9_B": "Có những chiếc tủ ở phía trên màn hình máy tính.",
    "9_C": "Người đàn ông đang mở cửa sổ.",
    "9_D": "Người đàn ông đang với tay lấy điện thoại.",
    "10_A": "Có một số bộ bàn ghế ở ngoài trời.",
    "10_B": "Có một số người đang ngồi tại các bàn.",
    "10_C": "Có những chiếc ô nhựa trên các bàn.",
    "10_D": "Có rất nhiều hoa trong vườn.",
    "11_A": "Một chiếc thuyền kayak đang được chèo xuôi dòng sông.",
    "11_B": "Một đống gạch đã bị bỏ lại trên lối đi.",
    "11_C": "Một số mái nhà đang được sửa chữa.",
    "11_D": "Một số chiếc ghế đã được đặt dọc theo con kênh.",
    "12_A": "Các xe ô tô đang xếp hàng tại trạm thu phí.",
    "12_B": "Một số biển báo giao thông đang treo trên trần nhà.",
    "12_C": "Một đường hầm đã bị đóng cửa để thi công.",
    "12_D": "Một số người đang đứng bên lề đường.",
    "13_A": "Một số phụ nữ đang băng qua đường.",
    "13_B": "Một số phụ nữ đang thanh toán tiền mua quần áo.",
    "13_C": "Một số quần áo đang được gấp lại.",
    "13_D": "Một số chiếc áo khoác đang được trưng bày.",
    "14_A": "Một số tấm rèm đã được trải ra trên sàn nhà.",
    "14_B": "Một số chậu cây đã được đặt ở ngoài trời.",
    "14_C": "Một số tác phẩm nghệ thuật đã được treo trên tường.",
    "14_D": "Một số chiếc ghế đã được cất trong tủ.",
    "15_A": "Một tấm biển đang treo trên cửa.",
    "15_B": "Một chiếc tủ đã được chất đầy đồ dùng.",
    "15_C": "Một số chiếc kệ đang được lắp ráp.",
    "15_D": "Một số dụng cụ nằm vương vãi trên mặt đất."
  };

  function stripHtmlAndOptionPrefix(str) {
    return (str || "")
      .replace(/<[^>]+>/g, "")
      .replace(/^\s*\([A-Da-d]\)\s*/, "")
      .replace(/^\s*[A-Da-d][\.\)]\s+/, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  const dictData = {
    dang_01: dang01Examples.slice(),
    dang_02: [],
    dang_03: []
  };

  if (Array.isArray(window.part01Data)) {
    window.part01Data.forEach(sec => {
      if (!sec || !sec.id) return;
      const secId = sec.id;

      // 1. Các bài luyện tập trong Dạng 01, Dạng 02, Dạng 03 (lấy toàn bộ 4 câu A, B, C, D mỗi bài)
      if (secId === "dang_01" || secId === "dang_02" || secId === "dang_03") {
        const viMap = secId === "dang_01" ? DANG01_VI : (secId === "dang_02" ? DANG02_VI : DANG03_VI);
        const practices = (sec.theory || []).filter(s => s && s.practice && Array.isArray(s.practice.options));
        practices.forEach((pSlide, idx) => {
          const qNum = idx + 1;
          const opts = pSlide.practice.options;
          ["A", "B", "C", "D"].forEach((letter, optIdx) => {
            const rawOpt = opts[optIdx] || "";
            const cleanSentence = stripHtmlAndOptionPrefix(rawOpt);
            if (!cleanSentence) return;
            const viText = viMap[`${qNum}_${letter}`] || "";
            const words = cleanSentence.split(" ");
            const audioFileName = secId.replace("_", "") + "_q" + qNum + "_" + letter + ".mp3";
            dictData[secId].push({
              id: dictData[secId].length + 1,
              sentence: cleanSentence,
              vi: viText,
              hint: words.slice(0, 2).join(" "),
              audio: "media/part01_dictation/" + audioFileName,
              useTTS: false,
              singleAudio: true,
              type: "practice"
            });
          });
        });
      }

      // 2. Các bài Test 1 -> Test 10 (lấy toàn bộ 4 câu A, B, C, D của cả 6 câu = 24 câu/test)
      if (secId.startsWith("test_")) {
        dictData[secId] = [];
        const tNum = parseInt(secId.split("_")[1], 10);
        const tStr = (tNum < 10 ? "0" + tNum : "" + tNum);
        (sec.practice_sets || []).forEach(pset => {
          const qObj = pset.questions && pset.questions[0];
          if (!qObj || !qObj.choices) return;
          const choices = qObj.choices;
          const viChoices = qObj.vietnamese_choices || {};
          const setStr = (pset.set_index < 10 ? "0" + pset.set_index : "" + pset.set_index);
          ["A", "B", "C", "D"].forEach(letter => {
            const cleanSentence = stripHtmlAndOptionPrefix(choices[letter]);
            if (!cleanSentence) return;
            const viText = stripHtmlAndOptionPrefix(viChoices[letter] || "");
            const words = cleanSentence.split(" ");
            const audioFileName = "t" + tStr + "_q" + setStr + "_" + letter + ".mp3";
            dictData[secId].push({
              id: dictData[secId].length + 1,
              sentence: cleanSentence,
              vi: viText,
              hint: words.slice(0, 2).join(" "),
              audio: "media/part01_dictation/" + audioFileName,
              useTTS: false,
              singleAudio: true,
              type: "test"
            });
          });
        });
      }
    });
  }

  window.part01DictationData = dictData;
})();
